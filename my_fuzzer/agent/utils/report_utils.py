from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.config import FuzzerConfig
from .cli_utils import ensure_dirs


def make_run_report_slug(started_at: str) -> str:
    compact = started_at.replace("-", "").replace(":", "")
    compact = compact.replace("T", "_").replace("+00:00", "Z")
    return f"run_{compact}"


def ensure_run_report_dirs(config: FuzzerConfig, run_slug: str) -> dict[str, Path]:
    run_reports_dir = config.reports_dir / run_slug
    grammar_dir = run_reports_dir / "grammar"
    coverage_dir = run_reports_dir / "coverage"
    summary_dir = run_reports_dir / "summary"
    ensure_dirs(config.reports_dir, run_reports_dir, grammar_dir, coverage_dir, summary_dir)
    return {
        "run_reports_dir": run_reports_dir,
        "grammar_dir": grammar_dir,
        "coverage_dir": coverage_dir,
        "summary_dir": summary_dir,
    }


def _stringify(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ", ".join(_stringify(item) for item in value) or "-"
    if isinstance(value, dict):
        return ", ".join(f"{key}={_stringify(item)}" for key, item in sorted(value.items())) or "-"
    return str(value)


def write_markdown(path: Path, lines: list[str]) -> Path:
    ensure_dirs(path.parent)
    content = "\n".join(lines).rstrip() + "\n"
    path.write_text(content, encoding="utf-8")
    return path


def write_unavailable_report(
    path: Path,
    title: str,
    reason: str,
    metadata: dict[str, Any] | None = None,
) -> Path:
    lines = [f"# {title}", "", f"Status: not available", "", f"Reason: {reason}"]

    if metadata:
        lines.extend(["", "## Metadata", "", "| Field | Value |", "|---|---|"])
        for key, value in metadata.items():
            lines.append(f"| {key} | {_stringify(value)} |")

    return write_markdown(path, lines)
