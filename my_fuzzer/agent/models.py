from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict
import re


# ---------------------------------------------------------------------------
# Test result
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    filename: str
    url: str
    status: str
    status_code: int | None
    error_message: str | None
    response_time_ms: int | None
    headers: dict[str, str] | None = None
    feature_scored: bool = False
    base_url: str | None = None
    city_name: str | None = None
    format_type: str | None = None
    feature_key: str | None = None
    ignored_reason: str | None = None


# ---------------------------------------------------------------------------
# Request spec — the expanded input model (URL + headers)
# ---------------------------------------------------------------------------

@dataclass
class RequestSpec:
    """A single HTTP request the fuzzer will execute."""
    url: str
    headers: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# LLM call result
# ---------------------------------------------------------------------------

@dataclass
class LLMCallResult:
    raw_response: str
    trace: dict[str, Any]
    node_name: str = ""


# ---------------------------------------------------------------------------
# LangGraph state
# ---------------------------------------------------------------------------

class GraphState(TypedDict, total=False):
    """State flowing through the two-node LangGraph."""
    current_grammar: str
    results: list[dict[str, Any]]
    coverage_data: dict[str, Any]
    feature_summary: dict[str, Any]
    validation_feedback: str
    iteration_history: str

    # Planner
    planner_prompt: str
    planner_output: str
    planner_parsed: dict[str, Any]

    # Rewriter
    rewriter_prompt: str
    rewriter_output: str

    # Final
    final_raw_response: str
    trace: list[dict[str, Any]]

    # Request profiles recommended by the planner
    request_profiles: dict[str, list[str]]


# ---------------------------------------------------------------------------
# Planner output schema
# ---------------------------------------------------------------------------

@dataclass
class PlannerOutput:
    """Parsed output from the analysis-planner node."""
    analysis: str = ""
    overrepresented_responses: list[str] = field(default_factory=list)
    underexplored_url_families: list[str] = field(default_factory=list)
    reachable_by_grammar: list[str] = field(default_factory=list)
    reachable_by_headers_only: list[str] = field(default_factory=list)
    unreachable_harness_limits: list[str] = field(default_factory=list)
    recommended_rule_edits: list[dict[str, str]] = field(default_factory=list)
    request_space_recommendations: dict[str, list[str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Mutation plan (grammar rewriter output)
# ---------------------------------------------------------------------------

PROTECTED_RULES = (
    "protocol",
    "host",
    "port",
    "PROTOCOL",
    "HOSTNAME",
    "PORTS",
)

RULE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass
class RuleUpdate:
    rule: str
    replacement: str


@dataclass
class MutationPlan:
    updates: list[RuleUpdate]
    rationale: str = ""


# ---------------------------------------------------------------------------
# Legacy shim — kept for backward compatibility in LLMState references
# ---------------------------------------------------------------------------

class LLMState(TypedDict, total=False):
    prompt: str
    response: str
