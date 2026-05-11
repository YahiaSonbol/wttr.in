from __future__ import annotations

import textwrap
from pathlib import Path
from string import Formatter


_PROMPTS_DIR = Path(__file__).resolve().parent


WTTR_DESCRIPTION = textwrap.dedent(
    """
    wttr.in is a URL-driven weather service. The input is an HTTP GET URL sent to the local server at
    `http://localhost:8002/`. The path and query string determine what the server renders.

    For this fuzzing loop, the scoring focus is intentionally narrow:
    - plain city routes such as `/<city>`;
    - city routes with supported format queries such as `/<city>?format=j1`;
    - plain PNG city routes such as `/<city>.png`.

    The main coverage objective is to increase the executed and successful coverage of normalized
    `base URL + city name + format type` combinations. Ignore non-scored families such as moon routes,
    special `~` lookups, domain lookups, and multi-location paths unless they are unavoidable side effects.
    Keep the local base URL fixed, and preserve reachability for every scored city and scored format even
    when you bias the grammar toward a smaller hot subset.
    """
).strip()


RESPONSE_CONTRACT = textwrap.dedent(
    """\
    Return JSON only. No markdown fences. Use this exact shape:
    {
      "rationale": "one short sentence",
      "updates": [
        {
          "rule": "existingRuleName",
          "replacement": "existingRuleName\\n    : ...\\n    ;"
        }
      ]
    }
    Replace only 1 to 3 existing rules.
    Each replacement must be a complete rule block."""
).strip()


def load_prompt(filename: str) -> str:
    """Load a markdown prompt file from the prompts directory.

    Raises ``FileNotFoundError`` if the file does not exist or
    ``ValueError`` if the file is empty.
    """
    filepath = _PROMPTS_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    content = filepath.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Prompt file is empty: {filepath}")
    return content


def _safe_format(template: str, **kwargs: str) -> str:
    """Format a template string, replacing only known placeholders.

    This avoids crashing on literal curly braces in the prompt (e.g. JSON
    examples) by only substituting placeholders that match provided kwargs.
    """
    result = template
    for key, value in kwargs.items():
        result = result.replace("{" + key + "}", value)
    return result


def format_planner_prompt(**kwargs: str) -> str:
    """Load and format the planner system prompt with runtime variables.

    Expected kwargs:
        wttr_description, current_grammar, grammar_declaration,
        protected_rules, protected_rule_context, editable_rules,
        results_summary, coverage_summary, feature_coverage_summary, missing_hotspots,
        validation_feedback, iteration_history,
        host_profiles, ua_profiles, accept_language_profiles, ip_profiles
    """
    template = load_prompt("planner_agent.md")
    return _safe_format(template, **kwargs)


def format_rewriter_prompt(**kwargs: str) -> str:
    """Load and format the rewriter system prompt with runtime variables.

    Expected kwargs:
        wttr_description, current_grammar, planner_output,
        grammar_declaration, protected_rules, protected_rule_context,
        editable_rules, response_contract
    """
    template = load_prompt("coder_agent.md")
    return _safe_format(template, **kwargs)
