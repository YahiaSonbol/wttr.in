from __future__ import annotations

import json
import os
import shlex
import time
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

from .validator import PROTECTED_RULES, editable_rule_names, grammar_declaration, protected_rule_context
from .models import GraphState, LLMCallResult, PlannerOutput, TestResult
from .core.config import FuzzerConfig
from .core.llm_client import get_chat_client
from .profiles import profile_names_summary
from .prompts.prompt import (
    WTTR_DESCRIPTION,
    RESPONSE_CONTRACT,
    format_planner_prompt,
    format_rewriter_prompt,
)
from .utils.cli_utils import run_command
from .utils.llm_utils import (
    codebase_reachability_guide_formatter,
    feedback_block_formatter,
    results_formatter,
    coverage_data_formatter,
    missing_hotspots_formatter,
    missing_line_context_formatter,
    iteration_history_formatter,
    response_text_formatter,
)


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def _profile_list_text(names: list[str]) -> str:
    """Format a list of profile names for prompt injection."""
    if not names:
        return "None available."
    return ", ".join(f"`{n}`" for n in names)


def build_planner_prompt(
    config: FuzzerConfig,
    current_grammar: str,
    results: list[TestResult],
    coverage_data: dict[str, Any],
    validation_feedback: str | None = None,
    iteration_history: str | None = None,
) -> str:
    """Render the analysis-planner prompt with all runtime variables."""
    profiles = profile_names_summary()
    return format_planner_prompt(
        wttr_description=WTTR_DESCRIPTION,
        current_grammar=current_grammar.rstrip(),
        grammar_declaration=grammar_declaration(current_grammar),
        protected_rules=", ".join(PROTECTED_RULES),
        protected_rule_context=protected_rule_context(current_grammar),
        editable_rules=", ".join(editable_rule_names(current_grammar)),
        codebase_reachability_guide=codebase_reachability_guide_formatter(),
        results_summary=results_formatter(results),
        coverage_summary=coverage_data_formatter(coverage_data, config),
        missing_hotspots=missing_hotspots_formatter(coverage_data, config),
        missing_line_context=missing_line_context_formatter(coverage_data, config),
        validation_feedback=feedback_block_formatter(validation_feedback),
        iteration_history=iteration_history or "No previous iterations.",
        host_profiles=_profile_list_text(profiles["host_profiles"]),
        ua_profiles=_profile_list_text(profiles["ua_profiles"]),
        accept_language_profiles=_profile_list_text(profiles["accept_language_profiles"]),
        ip_profiles=_profile_list_text(profiles["ip_profiles"]),
    )


def build_rewriter_prompt(
    config: FuzzerConfig,
    current_grammar: str,
    planner_output: str,
) -> str:
    """Render the grammar-rewriter prompt with the planner's analysis."""
    return format_rewriter_prompt(
        wttr_description=WTTR_DESCRIPTION,
        current_grammar=current_grammar.rstrip(),
        grammar_declaration=grammar_declaration(current_grammar),
        protected_rules=", ".join(PROTECTED_RULES),
        protected_rule_context=protected_rule_context(current_grammar),
        editable_rules=", ".join(editable_rule_names(current_grammar)),
        codebase_reachability_guide=codebase_reachability_guide_formatter(),
        planner_output=planner_output,
        response_contract=RESPONSE_CONTRACT,
    )


# ---------------------------------------------------------------------------
# Raw LLM call (shared by both nodes)
# ---------------------------------------------------------------------------

def call_llm(config: FuzzerConfig, system_prompt: str, user_prompt: str, node_name: str = "") -> LLMCallResult:
    """Invoke the LLM with a system+user message pair."""
    custom_command = os.environ.get("FUZZER_LLM_COMMAND")
    if custom_command:
        full_prompt = f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}"
        result = run_command(
            shlex.split(custom_command),
            cwd=config.repo_root,
            input_text=full_prompt,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Custom LLM command failed:\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        return LLMCallResult(
            raw_response=result.stdout.strip(),
            trace={
                "mode": "custom_command",
                "command": custom_command,
                "returncode": result.returncode,
                "node": node_name,
            },
            node_name=node_name,
        )

    chat = get_chat_client(config)
    response = chat.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ])
    raw_response = response_text_formatter(response.content).strip()
    if not raw_response:
        raise RuntimeError(f"LLM client returned an empty response for node '{node_name}'.")

    return LLMCallResult(
        raw_response=raw_response,
        trace={
            "mode": "shared_client",
            "model": config.llm_model,
            "node": node_name,
        },
        node_name=node_name,
    )


# ---------------------------------------------------------------------------
# LangGraph nodes
# ---------------------------------------------------------------------------

def _make_planner_node(config: FuzzerConfig):
    """Return the analysis_planner node function."""

    def analysis_planner(state: GraphState) -> GraphState:
        print("[graph] ┌── analysis_planner: building prompt...")
        t0 = time.perf_counter()
        planner_system = build_planner_prompt(
            config,
            state["current_grammar"],
            state.get("results", []),
            state.get("coverage_data", {}),
            validation_feedback=state.get("validation_feedback"),
            iteration_history=state.get("iteration_history"),
        )
        user_msg = "Analyze the data above and produce the structured mutation plan as JSON."
        state["planner_prompt"] = planner_system
        prompt_len = len(planner_system)
        print(f"[graph] │   prompt built ({prompt_len:,} chars). Calling LLM...")

        t_llm = time.perf_counter()
        result = call_llm(config, planner_system, user_msg, node_name="analysis_planner")
        llm_elapsed = time.perf_counter() - t_llm
        state["planner_output"] = result.raw_response
        resp_len = len(result.raw_response)
        print(f"[graph] │   LLM responded ({resp_len:,} chars, {llm_elapsed:.1f}s)")

        # Try to parse the planner output for downstream use
        try:
            parsed = json.loads(_extract_json_object(result.raw_response))
            state["planner_parsed"] = parsed
            state.setdefault("request_profiles", parsed.get("request_space_recommendations", {}))
            n_rules = len(parsed.get("recommended_rule_edits", []))
            analysis_preview = parsed.get("analysis", "")[:120]
            print(f"[graph] │   planner recommends {n_rules} rule edit(s)")
            print(f"[graph] │   analysis: {analysis_preview}")
        except (json.JSONDecodeError, ValueError):
            state["planner_parsed"] = {}
            print("[graph] │   ⚠ could not parse planner JSON")

        total_elapsed = time.perf_counter() - t0
        trace_entry = {"node": "analysis_planner", "elapsed_s": round(total_elapsed, 2), **result.trace}
        state.setdefault("trace", []).append(trace_entry)
        print(f"[graph] └── analysis_planner done ({total_elapsed:.1f}s)")
        return state

    return analysis_planner


def _make_rewriter_node(config: FuzzerConfig):
    """Return the grammar_rewriter node function."""

    def grammar_rewriter(state: GraphState) -> GraphState:
        print("[graph] ┌── grammar_rewriter: building prompt...")
        t0 = time.perf_counter()
        planner_output = state.get("planner_output", "")
        rewriter_system = build_rewriter_prompt(
            config,
            state["current_grammar"],
            planner_output,
        )
        user_msg = "Rewrite the grammar following the planner's instructions. Return JSON only."
        state["rewriter_prompt"] = rewriter_system
        prompt_len = len(rewriter_system)
        print(f"[graph] │   prompt built ({prompt_len:,} chars). Calling LLM...")

        t_llm = time.perf_counter()
        result = call_llm(config, rewriter_system, user_msg, node_name="grammar_rewriter")
        llm_elapsed = time.perf_counter() - t_llm
        state["rewriter_output"] = result.raw_response
        state["final_raw_response"] = result.raw_response
        resp_len = len(result.raw_response)
        print(f"[graph] │   LLM responded ({resp_len:,} chars, {llm_elapsed:.1f}s)")

        total_elapsed = time.perf_counter() - t0
        trace_entry = {"node": "grammar_rewriter", "elapsed_s": round(total_elapsed, 2), **result.trace}
        state.setdefault("trace", []).append(trace_entry)
        print(f"[graph] └── grammar_rewriter done ({total_elapsed:.1f}s)")
        return state

    return grammar_rewriter


def _extract_json_object(text: str) -> str:
    """Extract the first top-level JSON object from text."""
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON object found in text.")
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise ValueError("JSON object was not closed.")


# ---------------------------------------------------------------------------
# Public API — build and run the mutation graph
# ---------------------------------------------------------------------------

def build_mutation_graph(config: FuzzerConfig) -> StateGraph:
    """Construct the two-node LangGraph workflow."""
    graph = StateGraph(GraphState)
    graph.add_node("analysis_planner", _make_planner_node(config))
    graph.add_node("grammar_rewriter", _make_rewriter_node(config))
    graph.add_edge(START, "analysis_planner")
    graph.add_edge("analysis_planner", "grammar_rewriter")
    graph.add_edge("grammar_rewriter", END)
    return graph


def run_mutation_graph(
    config: FuzzerConfig,
    current_grammar: str,
    results: list[TestResult],
    coverage_data: dict[str, Any],
    validation_feedback: str | None = None,
    iteration_history: str | None = None,
) -> GraphState:
    """Run the full planner→rewriter pipeline and return the final state."""
    print("[graph] ═══ Starting mutation graph (planner → rewriter) ═══")
    t0 = time.perf_counter()
    graph = build_mutation_graph(config)
    compiled = graph.compile()

    initial_state: GraphState = {
        "current_grammar": current_grammar,
        "results": results,
        "coverage_data": coverage_data,
        "validation_feedback": validation_feedback or "",
        "iteration_history": iteration_history or "",
        "trace": [],
    }

    final_state = compiled.invoke(initial_state)
    total_elapsed = time.perf_counter() - t0
    print(f"[graph] ═══ Mutation graph complete ({total_elapsed:.1f}s total) ═══")
    return final_state
