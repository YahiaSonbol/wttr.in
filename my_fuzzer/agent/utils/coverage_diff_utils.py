from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from .report_utils import write_markdown


def load_coverage_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def _summary_value(coverage_data: dict[str, Any], key: str) -> float:
    totals = coverage_data.get("totals", {})
    value = totals.get(key)
    if value is None and key == "percent_covered":
        value = totals.get("percent_covered_display")
    return float(value or 0.0)


def _line_diff(
    old_cov: dict[str, Any],
    new_cov: dict[str, Any],
    *,
    max_files: int,
    max_lines_per_file: int,
) -> dict[str, Any]:
    old_files = old_cov.get("files", {})
    new_files = new_cov.get("files", {})
    all_files = sorted(set(old_files) | set(new_files))

    newly_covered_by_file: dict[str, list[int]] = {}
    no_longer_covered_by_file: dict[str, list[int]] = {}
    newly_missing_by_file: dict[str, list[int]] = {}
    no_longer_missing_by_file: dict[str, list[int]] = {}
    file_scores: dict[str, int] = {}

    for file_name in all_files:
        old_file = old_files.get(file_name, {})
        new_file = new_files.get(file_name, {})

        old_executed = set(old_file.get("executed_lines", []))
        new_executed = set(new_file.get("executed_lines", []))
        old_missing = set(old_file.get("missing_lines", []))
        new_missing = set(new_file.get("missing_lines", []))

        newly_covered = sorted(new_executed - old_executed)
        no_longer_covered = sorted(old_executed - new_executed)
        newly_missing = sorted(new_missing - old_missing)
        no_longer_missing = sorted(old_missing - new_missing)

        change_score = (
            len(newly_covered)
            + len(no_longer_covered)
            + len(newly_missing)
            + len(no_longer_missing)
        )
        if change_score == 0:
            continue

        file_scores[file_name] = change_score
        if newly_covered:
            newly_covered_by_file[file_name] = newly_covered[:max_lines_per_file]
        if no_longer_covered:
            no_longer_covered_by_file[file_name] = no_longer_covered[:max_lines_per_file]
        if newly_missing:
            newly_missing_by_file[file_name] = newly_missing[:max_lines_per_file]
        if no_longer_missing:
            no_longer_missing_by_file[file_name] = no_longer_missing[:max_lines_per_file]

    prioritized_files = [
        file_name
        for file_name, _ in sorted(file_scores.items(), key=lambda item: (-item[1], item[0]))[:max_files]
    ]

    def trim(data: dict[str, list[int]]) -> dict[str, list[int]]:
        return {file_name: data[file_name] for file_name in prioritized_files if file_name in data}

    return {
        "files_with_any_change": prioritized_files,
        "newly_covered_lines_by_file": trim(newly_covered_by_file),
        "no_longer_covered_lines_by_file": trim(no_longer_covered_by_file),
        "newly_missing_lines_by_file": trim(newly_missing_by_file),
        "no_longer_missing_lines_by_file": trim(no_longer_missing_by_file),
        "files_with_new_coverage": len(newly_covered_by_file),
        "files_with_new_missing": len(newly_missing_by_file),
    }


def compute_coverage_diff(
    old_cov: dict[str, Any],
    new_cov: dict[str, Any],
    *,
    max_files: int,
    max_lines_per_file: int,
) -> dict[str, Any]:
    old_percent = _summary_value(old_cov, "percent_covered")
    new_percent = _summary_value(new_cov, "percent_covered")
    old_covered = int(_summary_value(old_cov, "covered_lines"))
    new_covered = int(_summary_value(new_cov, "covered_lines"))
    old_missing = int(_summary_value(old_cov, "missing_lines"))
    new_missing = int(_summary_value(new_cov, "missing_lines"))
    old_statements = int(_summary_value(old_cov, "num_statements"))
    new_statements = int(_summary_value(new_cov, "num_statements"))

    diff = _line_diff(
        old_cov,
        new_cov,
        max_files=max_files,
        max_lines_per_file=max_lines_per_file,
    )
    diff.update(
        {
            "coverage_percent_old": old_percent,
            "coverage_percent_new": new_percent,
            "coverage_percent_delta": new_percent - old_percent,
            "covered_lines_old": old_covered,
            "covered_lines_new": new_covered,
            "covered_lines_delta": new_covered - old_covered,
            "missing_lines_old": old_missing,
            "missing_lines_new": new_missing,
            "missing_lines_delta": new_missing - old_missing,
            "num_statements_old": old_statements,
            "num_statements_new": new_statements,
            "num_statements_delta": new_statements - old_statements,
        }
    )
    return diff


def _append_line_section(lines: list[str], title: str, data: dict[str, list[int]]) -> None:
    lines.extend(["", f"## {title}", ""])
    if not data:
        lines.append("No changes.")
        return

    for file_name, values in data.items():
        lines.append(f"- `{file_name}`: {values}")


def write_coverage_diff_report(
    path: Path,
    *,
    iteration: int,
    from_label: str,
    to_label: str,
    diff_data: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> Path:
    lines = [
        "# Coverage Diff Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Iteration | {iteration} |",
        f"| From | {from_label} |",
        f"| To | {to_label} |",
        f"| Old Coverage | {diff_data['coverage_percent_old']:.2f}% |",
        f"| New Coverage | {diff_data['coverage_percent_new']:.2f}% |",
        f"| Coverage Delta | {diff_data['coverage_percent_delta']:+.2f} |",
        f"| Old Covered Lines | {diff_data['covered_lines_old']} |",
        f"| New Covered Lines | {diff_data['covered_lines_new']} |",
        f"| Covered Line Delta | {diff_data['covered_lines_delta']:+d} |",
        f"| Old Missing Lines | {diff_data['missing_lines_old']} |",
        f"| New Missing Lines | {diff_data['missing_lines_new']} |",
        f"| Missing Line Delta | {diff_data['missing_lines_delta']:+d} |",
        f"| Files With New Coverage | {diff_data['files_with_new_coverage']} |",
        f"| Files With New Missing | {diff_data['files_with_new_missing']} |",
    ]

    if metadata:
        for key, value in metadata.items():
            lines.append(f"| {key} | {_stringify(value)} |")

    _append_line_section(lines, "Newly Covered Lines", diff_data["newly_covered_lines_by_file"])
    _append_line_section(lines, "No Longer Covered Lines", diff_data["no_longer_covered_lines_by_file"])
    _append_line_section(lines, "Newly Missing Lines", diff_data["newly_missing_lines_by_file"])
    _append_line_section(lines, "No Longer Missing Lines", diff_data["no_longer_missing_lines_by_file"])

    return write_markdown(path, lines)


def aggregate_coverages(
    coverage_items: list[dict[str, Any]],
    *,
    max_files: int,
    max_lines_per_file: int,
) -> dict[str, Any]:
    aggregate_files: dict[str, dict[str, set[int]]] = {}

    for item in coverage_items:
        coverage_data = item["coverage_data"]
        for file_name, file_data in coverage_data.get("files", {}).items():
            file_state = aggregate_files.setdefault(
                file_name,
                {"executed_lines": set(), "executable_lines": set()},
            )
            executed_lines = set(file_data.get("executed_lines", []))
            missing_lines = set(file_data.get("missing_lines", []))
            file_state["executed_lines"].update(executed_lines)
            file_state["executable_lines"].update(executed_lines | missing_lines)

    summarized_files: dict[str, dict[str, Any]] = {}
    prioritized_files: list[tuple[str, int, int]] = []
    total_covered = 0
    total_executable = 0

    for file_name, file_state in aggregate_files.items():
        executed_lines = sorted(file_state["executed_lines"])
        executable_lines = sorted(file_state["executable_lines"])
        missing_lines = sorted(set(executable_lines) - set(executed_lines))
        covered_count = len(executed_lines)
        executable_count = len(executable_lines)
        missing_count = len(missing_lines)

        total_covered += covered_count
        total_executable += executable_count
        prioritized_files.append((file_name, missing_count, covered_count))
        summarized_files[file_name] = {
            "executed_lines": executed_lines,
            "executable_lines": executable_lines,
            "missing_lines": missing_lines,
            "summary": {
                "covered_lines": covered_count,
                "missing_lines": missing_count,
                "num_statements": executable_count,
                "percent_covered": (covered_count / executable_count * 100.0) if executable_count else 0.0,
            },
        }

    prioritized_files.sort(key=lambda item: (-item[1], -item[2], item[0]))
    trimmed_missing: dict[str, list[int]] = {}
    trimmed_covered: dict[str, list[int]] = {}

    for file_name, _, _ in prioritized_files[:max_files]:
        file_data = summarized_files[file_name]
        if file_data["missing_lines"]:
            trimmed_missing[file_name] = file_data["missing_lines"][:max_lines_per_file]
        if file_data["executed_lines"]:
            trimmed_covered[file_name] = file_data["executed_lines"][:max_lines_per_file]

    total_missing = total_executable - total_covered
    aggregate_percent = (total_covered / total_executable * 100.0) if total_executable else 0.0

    return {
        "source_count": len(coverage_items),
        "source_labels": [item["label"] for item in coverage_items],
        "totals": {
            "percent_covered": aggregate_percent,
            "covered_lines": total_covered,
            "missing_lines": total_missing,
            "num_statements": total_executable,
        },
        "files": summarized_files,
        "top_missing_lines_by_file": trimmed_missing,
        "top_covered_lines_by_file": trimmed_covered,
    }


def write_aggregate_coverage_report(
    path: Path,
    *,
    aggregate_data: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> Path:
    totals = aggregate_data["totals"]
    lines = [
        "# Cycle Aggregate Coverage Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Included Coverage Artifacts | {aggregate_data['source_count']} |",
        f"| Aggregate Coverage | {totals['percent_covered']:.2f}% |",
        f"| Aggregate Covered Lines | {totals['covered_lines']} |",
        f"| Aggregate Missing Lines | {totals['missing_lines']} |",
        f"| Aggregate Executable Lines | {totals['num_statements']} |",
    ]

    if metadata:
        for key, value in metadata.items():
            lines.append(f"| {key} | {_stringify(value)} |")

    lines.extend(["", "## Included Artifacts", ""])
    if aggregate_data["source_labels"]:
        for label in aggregate_data["source_labels"]:
            lines.append(f"- {label}")
    else:
        lines.append("No coverage artifacts were included.")

    _append_line_section(lines, "Top Missing Lines By File", aggregate_data["top_missing_lines_by_file"])
    _append_line_section(lines, "Top Covered Lines By File", aggregate_data["top_covered_lines_by_file"])

    return write_markdown(path, lines)
