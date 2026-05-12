from __future__ import annotations

from difflib import unified_diff
from pathlib import Path
from typing import Any

from .report_utils import write_markdown


def _stringify(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value) or "-"
    if isinstance(value, dict):
        return ", ".join(f"{key}={item}" for key, item in sorted(value.items())) or "-"
    return str(value)


def build_grammar_diff(old_text: str, new_text: str, from_label: str, to_label: str) -> str:
    diff_lines = list(
        unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile=from_label,
            tofile=to_label,
            lineterm="",
        )
    )
    if not diff_lines:
        return "(no grammar changes)"
    return "\n".join(diff_lines)


def write_grammar_diff_report(
    path: Path,
    *,
    iteration: int,
    from_label: str,
    to_label: str,
    decision: str,
    mutation_status: str,
    old_text: str,
    new_text: str,
    metadata: dict[str, Any] | None = None,
) -> Path:
    diff_text = build_grammar_diff(old_text, new_text, from_label, to_label)
    lines = [
        "# Grammar Diff Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Iteration | {iteration} |",
        f"| From | {from_label} |",
        f"| To | {to_label} |",
        f"| Decision | {decision} |",
        f"| Mutation Status | {mutation_status} |",
    ]

    if metadata:
        for key, value in metadata.items():
            lines.append(f"| {key} | {_stringify(value)} |")

    lines.extend(["", "## Diff", "", "```diff", diff_text, "```"])
    return write_markdown(path, lines)
