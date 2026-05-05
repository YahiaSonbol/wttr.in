from __future__ import annotations

import importlib.metadata
import os
import shlex
import textwrap
from dataclasses import dataclass
from typing import Any, TypedDict

from .core import FuzzerConfig, TestResult, run_command
from .coverage_runner import coverage_excerpt
from .validator import IMMUTABLE_RULES, MUTABLE_RULES, immutable_rule_context, mutable_rule_context


DEFAULT_SYSTEM_PROMPT = textwrap.dedent(
    """
    You mutate an ANTLR4 grammar used for coverage-guided fuzzing of a local wttr.in instance.
    You may update only the explicitly allowed rule blocks.
    Never rewrite the whole grammar.
    Never change the fixed local target base URL rules.
    Return JSON only with this shape:
    {
      "rationale": "one short sentence",
      "updates": [
        {
          "rule": "query",
          "replacement": "query\\n    : ...\\n    ;"
        }
      ]
    }
    Replace only 1 to 3 existing mutable rules.
    Each replacement must be a complete rule block.
    """
).strip()


TARGET_HINTS = textwrap.dedent(
    """
    Useful wttr.in path and query patterns to consider:
    - `/moon` and `/moon@<location>`
    - `/<location>.png`
    - png-style names like `/Paris_200x_lang=ru.png`
    - `?format=j1`, `?format=j2`, `?format=v2`, `?format=v2n`, `?format=v2d`, `?format=p1`
    - one-letter query flags parsed by wttr.in: `A d n m M u I t T p q Q F 0 1 2 3`
    - static text pages such as `/:help`, `/:translation`, `/:bash.function`, `/:iterm2`
    Keep everything anchored to the existing `http://localhost:8002/`-style base URL.
    """
).strip()


@dataclass
class LLMCallResult:
    raw_response: str
    trace: dict[str, Any]


class _LLMState(TypedDict, total=False):
    prompt: str
    response: str


def _feedback_block(validation_feedback: str | None) -> str:
    if not validation_feedback:
        return ""
    return textwrap.dedent(
        f"""
        ## Fix The Last Attempt

        {validation_feedback}
        """
    ).strip()


def _escape_markdown_cell(value: str | None, limit: int = 200) -> str:
    if not value:
        return "-"
    single_line = " ".join(value.split())
    if len(single_line) > limit:
        single_line = single_line[: limit - 3] + "..."
    return single_line.replace("|", "\\|")


def _format_results(results: list[TestResult]) -> str:
    interesting = [result for result in results if result.status != "SUCCESS"]
    successful = [result for result in results if result.status == "SUCCESS"]
    chosen = interesting[:20]
    if not chosen:
        chosen = successful[:10]
    elif successful:
        chosen.extend(successful[:5])

    lines = [
        "| File | Status | Code | URL | Error |",
        "|---|---|---:|---|---|",
    ]
    for result in chosen:
        lines.append(
            "| {filename} | {status} | {code} | {url} | {error} |".format(
                filename=_escape_markdown_cell(result.filename, 80),
                status=result.status,
                code=result.status_code if result.status_code is not None else "-",
                url=_escape_markdown_cell(result.url, 140),
                error=_escape_markdown_cell(result.error_message, 120),
            )
        )

    omitted = len(results) - len(chosen)
    if omitted > 0:
        lines.append("")
        lines.append(f"{omitted} additional result rows were omitted.")
    return "\n".join(lines)


def _format_coverage(coverage_data: dict[str, Any], config: FuzzerConfig) -> str:
    excerpt = coverage_excerpt(coverage_data, config)
    totals = excerpt.get("totals", {})
    percent = totals.get("percent_covered")
    if percent is None:
        percent = totals.get("percent_covered_display", "unknown")

    lines = [f"Overall coverage: {percent}", ""]
    files = excerpt.get("files", {})
    if not files:
        lines.append("No missing-line hotspots were recorded.")
        return "\n".join(lines)

    for file_name, file_data in files.items():
        missing = ", ".join(str(line) for line in file_data.get("missing_lines", [])) or "none"
        executed = ", ".join(str(line) for line in file_data.get("executed_lines", [])[-10:]) or "none"
        lines.append(f"### {file_name}")
        lines.append(f"- Missing lines: {missing}")
        lines.append(f"- Recently executed lines: {executed}")
        lines.append("")
    return "\n".join(lines).rstrip()


def build_mutation_prompt(
    config: FuzzerConfig,
    current_grammar: str,
    results: list[TestResult],
    coverage_data: dict[str, Any],
    validation_feedback: str | None = None,
) -> str:
    allowed = ", ".join(MUTABLE_RULES)
    immutable = ", ".join(IMMUTABLE_RULES)

    prompt = f"""
    # Mutation Task

    Use the latest run output and coverage hotspots first, then make a small grammar change.

    ## Latest Run Output

    {_format_results(results)}

    ## Coverage Hotspots

    {_format_coverage(coverage_data, config)}

    ## Mutable Rules You May Edit

    {allowed}

    ## Immutable Rules

    {immutable}

    ## Immutable Base-Url Rules

    ```antlr
    {immutable_rule_context(current_grammar)}
    ```

    ## Current Mutable Rule Blocks

    ```antlr
    {mutable_rule_context(current_grammar)}
    ```

    ## Target Hints

    {TARGET_HINTS}

    {_feedback_block(validation_feedback)}

    ## Response Rules

    - Return JSON only. No markdown fences.
    - Replace only 1 to 3 rules.
    - Each `replacement` must be a complete rule block for an allowed rule.
    - Do not add new top-level rules.
    - Do not touch protocol, host, or port behavior.
    - Preserve the grammar name `url`.
    """

    return textwrap.dedent(prompt).strip()


def _response_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    return str(content)


def _build_chat_model(config: FuzzerConfig):
    from langchain_openai import ChatOpenAI

    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            f"Missing OPENROUTER_API_KEY or OPENAI_API_KEY. Put it in `{config.env_file}` or export it first."
        )

    common_kwargs = {
        "model": config.llm_model,
        "temperature": 0.2,
        "max_tokens": 1200,
        "max_retries": 0,
    }
    client_variants = [
        {
            "api_key": api_key,
            "base_url": config.llm_base_url,
            "timeout": config.llm_timeout,
        },
        {
            "openai_api_key": api_key,
            "openai_api_base": config.llm_base_url,
            "request_timeout": config.llm_timeout,
        },
    ]

    last_error: Exception | None = None
    for client_kwargs in client_variants:
        try:
            return ChatOpenAI(**common_kwargs, **client_kwargs)
        except TypeError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise RuntimeError("Could not initialize ChatOpenAI.")


def _version_info(packages: list[str]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "missing"
    return versions


def call_llm(config: FuzzerConfig, prompt: str) -> LLMCallResult:
    custom_command = os.environ.get("FUZZER_LLM_COMMAND")
    if custom_command:
        result = run_command(
            shlex.split(custom_command),
            cwd=config.repo_root,
            input_text=prompt,
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
            },
        )

    try:
        from langchain_core.messages import HumanMessage, SystemMessage
        from langgraph.graph import StateGraph
    except ImportError as exc:
        versions = _version_info(["langgraph", "langchain-core", "langchain-openai"])
        raise RuntimeError(
            "A compatible LangGraph stack is required. Reinstall `my_fuzzer/requirements-fuzzer.txt` "
            f"if needed. Installed versions: {versions}"
        ) from exc

    chat = _build_chat_model(config)

    def invoke_model(state: _LLMState) -> _LLMState:
        response = chat.invoke(
            [
                SystemMessage(content=DEFAULT_SYSTEM_PROMPT),
                HumanMessage(content=state["prompt"]),
            ]
        )
        return {"response": _response_text(response.content).strip()}

    workflow = StateGraph(_LLMState)
    workflow.add_node("llm", invoke_model)
    workflow.set_entry_point("llm")
    workflow.set_finish_point("llm")
    app = workflow.compile()
    response_state = app.invoke({"prompt": prompt})

    raw_response = (response_state.get("response") or "").strip()
    if not raw_response:
        raise RuntimeError("LangGraph returned an empty response.")

    return LLMCallResult(
        raw_response=raw_response,
        trace={
            "mode": "langgraph_simple",
            "model": config.llm_model,
        },
    )
