from __future__ import annotations

import textwrap
from pathlib import Path
from string import Formatter


_PROMPTS_DIR = Path(__file__).resolve().parent


WTTR_DESCRIPTION = textwrap.dedent(
    """
    wttr.in is a URL-driven weather service. The input is an HTTP GET URL sent to the local server at
    `http://localhost:8002/`. The path and query string determine what the server renders.

    Expected input patterns include:
    - `/` for the default location weather report.
    - `/<location>` for city, airport, or place lookups.
    - `/moon` and `/moon@<location>` for moon-related pages.
    - special routes such as `/:help`, `/:translation`, `/:bash.function`, and `/:iterm2`.
    - PNG paths such as `/<location>.png` and `/<location>_200x_lang=<lang>.png`.
    - query parameters and flags such as `?format=...`, `?lang=...`, and one-letter flags combined with `&`.

    Expected outputs include successful HTTP responses that may render terminal text, plain text, HTML, PNG,
    JSON-like data endpoints, or other wttr.in response variants depending on the request shape. Invalid or unusual
    inputs may return warnings, errors, or server failures. Your job is to improve the grammar so it produces more
    interesting requests and reaches new code paths, while keeping the local base URL fixed.
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
        protected_rules, protected_rule_context, editable_rules, codebase_reachability_guide,
        results_summary, coverage_summary, missing_hotspots, missing_line_context,
        validation_feedback, iteration_history,
        host_profiles, ua_profiles, accept_language_profiles, ip_profiles
    """
    template = load_prompt("planner_agent.md")
    return _safe_format(template, **kwargs)


def format_rewriter_prompt(**kwargs: str) -> str:
    """Load and format the rewriter system prompt with runtime variables.

    Expected kwargs:
        wttr_description, current_grammar, planner_output, codebase_reachability_guide,
        grammar_declaration, protected_rules, protected_rule_context,
        editable_rules, response_contract
    """
    template = load_prompt("coder_agent.md")
    return _safe_format(template, **kwargs)
