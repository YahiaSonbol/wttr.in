from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from ..models import TestResult
from .cli_utils import ensure_dirs
from .feature_coverage import compact_feature_label, feature_delta


def ensure_report_dirs(config) -> None:
    ensure_dirs(config.logs_dir, config.raw_dir, config.reports_dir)


def _as_result_dict(item: TestResult | dict[str, Any]) -> dict[str, Any]:
    if isinstance(item, dict):
        return item
    return {
        "filename": item.filename,
        "url": item.url,
        "status": item.status,
        "status_code": item.status_code,
        "error_message": item.error_message,
        "response_time_ms": item.response_time_ms,
        "headers": item.headers,
        "feature_scored": item.feature_scored,
        "base_url": item.base_url,
        "city_name": item.city_name,
        "format_type": item.format_type,
        "feature_key": item.feature_key,
        "ignored_reason": item.ignored_reason,
    }


def _preview(text: str | None, limit: int = 160) -> str:
    if not text:
        return "-"
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _coverage_line_sets(coverage_data: dict[str, Any] | None) -> dict[str, set[int]]:
    if not coverage_data:
        return {}
    return {
        file_name: set(file_data.get("executed_lines", []))
        for file_name, file_data in coverage_data.get("files", {}).items()
    }


def _line_coverage_diff(
    old_coverage: dict[str, Any] | None,
    new_coverage: dict[str, Any] | None,
) -> dict[str, Any]:
    old_sets = _coverage_line_sets(old_coverage)
    new_sets = _coverage_line_sets(new_coverage)
    all_files = sorted(set(old_sets) | set(new_sets))

    new_lines_by_file: dict[str, list[int]] = {}
    lost_lines_by_file: dict[str, list[int]] = {}
    file_deltas: list[tuple[str, int, int]] = []

    for file_name in all_files:
        new_lines = sorted(new_sets.get(file_name, set()) - old_sets.get(file_name, set()))
        lost_lines = sorted(old_sets.get(file_name, set()) - new_sets.get(file_name, set()))
        if new_lines:
            new_lines_by_file[file_name] = new_lines
        if lost_lines:
            lost_lines_by_file[file_name] = lost_lines
        if new_lines or lost_lines:
            file_deltas.append((file_name, len(new_lines), len(lost_lines)))

    old_totals = (old_coverage or {}).get("totals", {})
    new_totals = (new_coverage or {}).get("totals", {})
    old_percent = float(old_totals.get("percent_covered") or old_totals.get("percent_covered_display") or 0.0)
    new_percent = float(new_totals.get("percent_covered") or new_totals.get("percent_covered_display") or 0.0)
    old_covered = int(old_totals.get("covered_lines") or 0)
    new_covered = int(new_totals.get("covered_lines") or 0)

    return {
        "old_percent": round(old_percent, 2),
        "new_percent": round(new_percent, 2),
        "percent_delta": round(new_percent - old_percent, 2),
        "old_covered_lines": old_covered,
        "new_covered_lines": new_covered,
        "covered_lines_delta": new_covered - old_covered,
        "new_lines_by_file": new_lines_by_file,
        "lost_lines_by_file": lost_lines_by_file,
        "file_deltas": sorted(file_deltas, key=lambda item: (item[1] + item[2], item[0]), reverse=True),
    }


def _feature_key_examples(summary: dict[str, Any] | None, keys: Iterable[str], limit: int = 8) -> list[str]:
    if not summary:
        return []
    examples = summary.get("feature_examples", {})
    lines: list[str] = []
    for key in list(keys)[:limit]:
        url = examples.get(key, "-")
        lines.append(f"- `{compact_feature_label(key)}` -> `{url}`")
    return lines


def write_coverage_diff_report(
    config,
    iteration: int,
    previous_baseline_coverage: dict[str, Any] | None,
    previous_baseline_feature: dict[str, Any] | None,
    baseline_coverage: dict[str, Any],
    baseline_feature: dict[str, Any],
    candidate_coverage: dict[str, Any] | None = None,
    candidate_feature: dict[str, Any] | None = None,
) -> tuple[Path, dict[str, Any]]:
    ensure_report_dirs(config)
    path = config.reports_dir / f"iteration_{iteration:03d}_coverage_diff.md"

    baseline_line_diff = _line_coverage_diff(previous_baseline_coverage, baseline_coverage)
    baseline_feature_diff = feature_delta(previous_baseline_feature, baseline_feature)

    lines: list[str] = [
        f"# Iteration {iteration} Coverage Diff",
        "",
        "## Previous Baseline -> Current Baseline",
        "",
        f"- Line coverage: {baseline_line_diff['old_percent']:.2f}% -> {baseline_line_diff['new_percent']:.2f}% ({baseline_line_diff['percent_delta']:+.2f})",
        f"- Covered lines: {baseline_line_diff['old_covered_lines']} -> {baseline_line_diff['new_covered_lines']} ({baseline_line_diff['covered_lines_delta']:+d})",
        f"- Executed feature coverage: {(previous_baseline_feature or {}).get('feature_coverage_percent', 0.0):.2f}% -> {baseline_feature.get('feature_coverage_percent', 0.0):.2f}% ({baseline_feature_diff['feature_coverage_delta']:+.2f})",
        f"- Successful feature coverage: {(previous_baseline_feature or {}).get('successful_feature_coverage_percent', 0.0):.2f}% -> {baseline_feature.get('successful_feature_coverage_percent', 0.0):.2f}% ({baseline_feature_diff['successful_feature_coverage_delta']:+.2f})",
        "",
        "### New City+Format Combinations",
        "",
    ]

    new_keys = baseline_feature_diff["new_hit_feature_keys"]
    lines.extend(_feature_key_examples(baseline_feature, new_keys) or ["- None"])
    lines.extend(["", "### Lost City+Format Combinations", ""])
    lost_keys = baseline_feature_diff["lost_hit_feature_keys"]
    lines.extend([f"- `{compact_feature_label(key)}`" for key in lost_keys[:8]] or ["- None"])
    lines.extend(["", "### Newly Covered Lines", ""])
    for file_name, new_lines in list(baseline_line_diff["new_lines_by_file"].items())[:8]:
        preview = ", ".join(str(line) for line in new_lines[:12])
        if len(new_lines) > 12:
            preview += f" ... (+{len(new_lines) - 12} more)"
        lines.append(f"- `{file_name}`: {preview}")
    if not baseline_line_diff["new_lines_by_file"]:
        lines.append("- None")

    lines.extend(["", "### No Longer Covered Lines", ""])
    for file_name, lost_lines in list(baseline_line_diff["lost_lines_by_file"].items())[:8]:
        preview = ", ".join(str(line) for line in lost_lines[:12])
        if len(lost_lines) > 12:
            preview += f" ... (+{len(lost_lines) - 12} more)"
        lines.append(f"- `{file_name}`: {preview}")
    if not baseline_line_diff["lost_lines_by_file"]:
        lines.append("- None")

    candidate_section: dict[str, Any] | None = None
    if candidate_coverage and candidate_feature:
        candidate_line_diff = _line_coverage_diff(baseline_coverage, candidate_coverage)
        candidate_feature_diff = feature_delta(baseline_feature, candidate_feature)
        candidate_section = {
            "line": candidate_line_diff,
            "feature": candidate_feature_diff,
        }
        lines.extend(
            [
                "",
                "## Current Baseline -> Current Candidate",
                "",
                f"- Line coverage: {candidate_line_diff['old_percent']:.2f}% -> {candidate_line_diff['new_percent']:.2f}% ({candidate_line_diff['percent_delta']:+.2f})",
                f"- Covered lines: {candidate_line_diff['old_covered_lines']} -> {candidate_line_diff['new_covered_lines']} ({candidate_line_diff['covered_lines_delta']:+d})",
                f"- Executed feature coverage: {baseline_feature.get('feature_coverage_percent', 0.0):.2f}% -> {candidate_feature.get('feature_coverage_percent', 0.0):.2f}% ({candidate_feature_diff['feature_coverage_delta']:+.2f})",
                f"- Successful feature coverage: {baseline_feature.get('successful_feature_coverage_percent', 0.0):.2f}% -> {candidate_feature.get('successful_feature_coverage_percent', 0.0):.2f}% ({candidate_feature_diff['successful_feature_coverage_delta']:+.2f})",
                "",
                "### New Candidate Combinations",
                "",
            ]
        )
        lines.extend(_feature_key_examples(candidate_feature, candidate_feature_diff["new_hit_feature_keys"]) or ["- None"])
        lines.extend(["", "### Candidate Lost Combinations", ""])
        lines.extend([f"- `{compact_feature_label(key)}`" for key in candidate_feature_diff["lost_hit_feature_keys"][:8]] or ["- None"])

    content = "\n".join(lines) + "\n"
    path.write_text(content, encoding="utf-8")
    return path, {
        "previous_to_baseline": {
            "line": baseline_line_diff,
            "feature": baseline_feature_diff,
        },
        "baseline_to_candidate": candidate_section,
    }


def _url_set(results: list[TestResult] | list[dict[str, Any]]) -> set[str]:
    return {
        _as_result_dict(item).get("url", "")
        for item in results
        if _as_result_dict(item).get("url")
    }


def _feature_key_set(results: list[TestResult] | list[dict[str, Any]]) -> set[str]:
    return {
        _as_result_dict(item).get("feature_key", "")
        for item in results
        if _as_result_dict(item).get("feature_scored") and _as_result_dict(item).get("feature_key")
    }


def _ignored_examples(results: list[TestResult] | list[dict[str, Any]], limit: int = 8) -> list[str]:
    lines: list[str] = []
    for item in results:
        result = _as_result_dict(item)
        if result.get("feature_scored"):
            continue
        reason = result.get("ignored_reason") or "unknown"
        url = result.get("url") or "-"
        lines.append(f"- `{reason}` -> `{url}`")
        if len(lines) >= limit:
            break
    return lines


def write_url_diff_report(
    config,
    iteration: int,
    previous_baseline_results: list[TestResult] | None,
    baseline_results: list[TestResult],
    candidate_results: list[TestResult] | None = None,
) -> Path:
    ensure_report_dirs(config)
    path = config.reports_dir / f"iteration_{iteration:03d}_url_diff.md"

    previous_urls = _url_set(previous_baseline_results or [])
    baseline_urls = _url_set(baseline_results)
    previous_keys = _feature_key_set(previous_baseline_results or [])
    baseline_keys = _feature_key_set(baseline_results)

    lines: list[str] = [
        f"# Iteration {iteration} URL Diff",
        "",
        "## Previous Baseline -> Current Baseline",
        "",
        f"- Raw URLs: {len(previous_urls)} -> {len(baseline_urls)} ({len(baseline_urls - previous_urls):+d} new, {len(previous_urls - baseline_urls):+d} removed)",
        f"- Scored city+format keys: {len(previous_keys)} -> {len(baseline_keys)} ({len(baseline_keys - previous_keys):+d} new, {len(previous_keys - baseline_keys):+d} removed)",
        "",
        "### New Scored Keys",
        "",
    ]
    lines.extend([f"- `{compact_feature_label(key)}`" for key in sorted(baseline_keys - previous_keys)[:12]] or ["- None"])
    lines.extend(["", "### Removed Scored Keys", ""])
    lines.extend([f"- `{compact_feature_label(key)}`" for key in sorted(previous_keys - baseline_keys)[:12]] or ["- None"])
    lines.extend(["", "### Ignored Request Examples", ""])
    lines.extend(_ignored_examples(baseline_results) or ["- None"])

    if candidate_results:
        baseline_candidate_urls = _url_set(candidate_results)
        candidate_keys = _feature_key_set(candidate_results)
        lines.extend(
            [
                "",
                "## Current Baseline -> Current Candidate",
                "",
                f"- Raw URLs: {len(baseline_urls)} -> {len(baseline_candidate_urls)} ({len(baseline_candidate_urls - baseline_urls):+d} new, {len(baseline_urls - baseline_candidate_urls):+d} removed)",
                f"- Scored city+format keys: {len(baseline_keys)} -> {len(candidate_keys)} ({len(candidate_keys - baseline_keys):+d} new, {len(baseline_keys - candidate_keys):+d} removed)",
                "",
                "### New Candidate Scored Keys",
                "",
            ]
        )
        lines.extend([f"- `{compact_feature_label(key)}`" for key in sorted(candidate_keys - baseline_keys)[:12]] or ["- None"])
        lines.extend(["", "### Candidate Ignored Request Examples", ""])
        lines.extend(_ignored_examples(candidate_results) or ["- None"])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_iteration_report(config, iteration_record: dict[str, Any]) -> Path:
    ensure_report_dirs(config)
    iteration = iteration_record["iteration"]
    path = config.reports_dir / f"iteration_{iteration:03d}_report.md"
    baseline_feature = iteration_record.get("feature_summary", {})
    candidate_feature = iteration_record.get("candidate_feature_summary", {})
    cumulative_feature = iteration_record.get("cumulative_feature_summary", {})
    cumulative_delta = iteration_record.get("cumulative_feature_delta", {})
    diff_summary = iteration_record.get("diff_summary", {})
    previous_to_baseline = diff_summary.get("previous_to_baseline", {})
    baseline_to_candidate = diff_summary.get("baseline_to_candidate", {})
    generation = iteration_record.get("generation", {})

    lines: list[str] = [
        f"# Iteration {iteration} Report",
        "",
        "## Overview",
        "",
        f"- Decision: {iteration_record.get('decision', '-')}",
        f"- Mutation status: {iteration_record.get('mutation_status', '-')}",
        f"- Tests run: {iteration_record.get('tests_run', 0)}",
        f"- Baseline line coverage: {iteration_record.get('coverage_percent', 0.0):.2f}%",
        f"- Baseline executed feature coverage: {baseline_feature.get('feature_coverage_percent', 0.0):.2f}%",
        f"- Baseline successful feature coverage: {baseline_feature.get('successful_feature_coverage_percent', 0.0):.2f}%",
        f"- Cycle cumulative executed feature coverage: {cumulative_feature.get('feature_coverage_percent', 0.0):.2f}%",
        f"- Cycle cumulative successful feature coverage: {cumulative_feature.get('successful_feature_coverage_percent', 0.0):.2f}%",
        f"- Container exit code: {iteration_record.get('container_exit_code')}",
    ]
    if generation:
        lines.append(f"- Generated payloads before filtering: {generation.get('generated_payload_count', 0)}")
        lines.append(f"- Selected unique request keys: {generation.get('selected_unique_request_count', 0)}")
    if iteration_record.get("candidate_coverage_percent") is not None:
        lines.append(f"- Candidate line coverage: {iteration_record['candidate_coverage_percent']:.2f}%")
    if candidate_feature:
        lines.append(f"- Candidate executed feature coverage: {candidate_feature.get('feature_coverage_percent', 0.0):.2f}%")
        lines.append(f"- Candidate successful feature coverage: {candidate_feature.get('successful_feature_coverage_percent', 0.0):.2f}%")
    if iteration_record.get("mutation_rationale"):
        lines.append(f"- Mutation rationale: {iteration_record['mutation_rationale']}")

    lines.extend(["", "## Feature Coverage", ""])
    lines.append(
        f"- Hit combinations: {baseline_feature.get('feature_hit', 0)}/{baseline_feature.get('feature_total', 0)}"
    )
    lines.append(
        f"- Successful combinations: {baseline_feature.get('successful_feature_hit', 0)}/{baseline_feature.get('feature_total', 0)}"
    )
    if cumulative_feature:
        lines.append(
            f"- Cycle cumulative combinations: {cumulative_feature.get('feature_hit', 0)}/{cumulative_feature.get('feature_total', 0)}"
        )
    missing_keys = baseline_feature.get("missing_feature_keys", [])[:10]
    if missing_keys:
        lines.append("- Missing combinations: " + ", ".join(compact_feature_label(key) for key in missing_keys))
    city_counts = baseline_feature.get("city_counts", {})
    if city_counts:
        lines.append("- City counts: " + ", ".join(f"{city}×{count}" for city, count in city_counts.items()))
    format_counts = baseline_feature.get("format_counts", {})
    if format_counts:
        lines.append("- Format counts: " + ", ".join(f"{fmt}×{count}" for fmt, count in format_counts.items()))
    ignored = baseline_feature.get("ignored_request_reasons", {})
    if ignored:
        lines.append("- Ignored requests: " + ", ".join(f"{reason}×{count}" for reason, count in ignored.items()))

    lines.extend(["", "## Diff Summary", ""])
    feature_diff = previous_to_baseline.get("feature", {})
    if feature_diff:
        lines.append(
            f"- Previous -> baseline executed feature delta: {feature_diff.get('feature_coverage_delta', 0.0):+.2f}"
        )
        lines.append(
            f"- Previous -> baseline successful feature delta: {feature_diff.get('successful_feature_coverage_delta', 0.0):+.2f}"
        )
        new_keys = feature_diff.get("new_hit_feature_keys", [])[:8]
        if new_keys:
            lines.append("- Newly reached combinations: " + ", ".join(compact_feature_label(key) for key in new_keys))
    if cumulative_delta:
        lines.append(
            f"- Cycle cumulative executed feature delta: {cumulative_delta.get('feature_coverage_delta', 0.0):+.2f}"
        )
        new_cycle_keys = cumulative_delta.get("new_hit_feature_keys", [])[:8]
        if new_cycle_keys:
            lines.append("- New cycle combinations: " + ", ".join(compact_feature_label(key) for key in new_cycle_keys))
    if baseline_to_candidate:
        candidate_feature_diff = baseline_to_candidate.get("feature", {})
        if candidate_feature_diff:
            lines.append(
                f"- Baseline -> candidate executed feature delta: {candidate_feature_diff.get('feature_coverage_delta', 0.0):+.2f}"
            )
            lines.append(
                f"- Baseline -> candidate successful feature delta: {candidate_feature_diff.get('successful_feature_coverage_delta', 0.0):+.2f}"
            )

    lines.extend(["", "## Artifacts", ""])
    if iteration_record.get("coverage_diff_report"):
        lines.append(f"- Coverage diff: [{Path(iteration_record['coverage_diff_report']).name}]({iteration_record['coverage_diff_report']})")
    if iteration_record.get("url_diff_report"):
        lines.append(f"- URL diff: [{Path(iteration_record['url_diff_report']).name}]({iteration_record['url_diff_report']})")
    if iteration_record.get("results_json"):
        lines.append(f"- Baseline raw results: [{Path(iteration_record['results_json']).name}]({iteration_record['results_json']})")
    if iteration_record.get("candidate_results_json"):
        lines.append(f"- Candidate raw results: [{Path(iteration_record['candidate_results_json']).name}]({iteration_record['candidate_results_json']})")
    if iteration_record.get("baseline_feature_json"):
        lines.append(f"- Baseline feature summary: [{Path(iteration_record['baseline_feature_json']).name}]({iteration_record['baseline_feature_json']})")
    if iteration_record.get("candidate_feature_json"):
        lines.append(f"- Candidate feature summary: [{Path(iteration_record['candidate_feature_json']).name}]({iteration_record['candidate_feature_json']})")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_cycle_report(config, report: dict[str, Any]) -> Path:
    ensure_report_dirs(config)
    started_at = report["started_at"].replace(":", "").replace("-", "").replace("T", "_").replace("Z", "")
    report_path = config.reports_dir / f"cycle_report_{started_at}.md"
    latest_report_path = config.reports_dir / "latest_cycle_report.md"

    lines: list[str] = [
        "# Fuzzer Cycle Report",
        "",
        "## Overview",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Status | {report['status']} |",
        f"| Started At | {report['started_at']} |",
        f"| Finished At | {report['finished_at']} |",
        f"| Duration Seconds | {report['duration_seconds']:.2f} |",
        f"| Configured Iterations | {report['config']['iterations']} |",
        f"| Completed Iterations | {report['completed_iterations']} |",
        f"| Tests Per Batch | {report['config']['case_count']} |",
        f"| Base URL | {report['config']['base_url']} |",
        f"| Champion Feature Coverage | {report['champion_feature_coverage']:.2f}% |",
        f"| Champion Successful Feature Coverage | {report['champion_successful_feature_coverage']:.2f}% |",
        f"| Cumulative Feature Coverage | {report.get('cumulative_feature_coverage', 0.0):.2f}% |",
        f"| Cumulative Successful Feature Coverage | {report.get('cumulative_successful_feature_coverage', 0.0):.2f}% |",
        f"| Champion Line Coverage | {report['champion_line_coverage']:.2f}% |",
        f"| Final Grammar | {report['final_grammar']} |",
    ]
    if report.get("error"):
        lines.append(f"| Error | {report['error']} |")

    lines.extend(
        [
            "",
            "## Iteration Summary",
            "",
            "| Iteration | Tests | Baseline Line | Baseline Feature | Cycle Cum Feature | Candidate Feature | Success | Warning | Crash | Error | Decision |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for item in report["iterations"]:
        http_counts = item.get("http_counts", {})
        baseline_feature = item.get("feature_summary", {})
        candidate_feature = item.get("candidate_feature_summary", {})
        cumulative_feature = item.get("cumulative_feature_summary", {})
        candidate_value = (
            f"{candidate_feature.get('feature_coverage_percent', 0.0):.2f}%"
            if candidate_feature
            else "-"
        )
        lines.append(
            "| {iteration} | {tests} | {line_cov:.2f}% | {feature_cov:.2f}% | {cumulative_feature_cov:.2f}% | {candidate_feature_cov} | {success} | {warning} | {crash} | {error} | {decision} |".format(
                iteration=item["iteration"],
                tests=item.get("tests_run", 0),
                line_cov=item.get("coverage_percent", 0.0),
                feature_cov=baseline_feature.get("feature_coverage_percent", 0.0),
                cumulative_feature_cov=cumulative_feature.get("feature_coverage_percent", 0.0),
                candidate_feature_cov=candidate_value,
                success=http_counts.get("SUCCESS", 0),
                warning=http_counts.get("WARNING", 0),
                crash=http_counts.get("CRASH", 0),
                error=http_counts.get("ERROR", 0),
                decision=item.get("decision", "-"),
            )
        )

    lines.extend(["", "## Diff Summary", ""])
    for item in report["iterations"]:
        baseline_feature = item.get("feature_summary", {})
        cumulative_feature = item.get("cumulative_feature_summary", {})
        cumulative_delta = item.get("cumulative_feature_delta", {})
        diff_summary = item.get("diff_summary", {})
        prev_to_base = diff_summary.get("previous_to_baseline", {})
        base_to_candidate = diff_summary.get("baseline_to_candidate", {})
        lines.append(f"### Iteration {item['iteration']}")
        lines.append("")
        lines.append(
            f"- Baseline feature coverage: {baseline_feature.get('feature_coverage_percent', 0.0):.2f}%"
        )
        lines.append(
            f"- Cycle cumulative feature coverage: {cumulative_feature.get('feature_coverage_percent', 0.0):.2f}%"
        )
        new_cycle_keys = cumulative_delta.get("new_hit_feature_keys", [])[:6]
        if new_cycle_keys:
            lines.append(
                "- New cycle combinations: " + ", ".join(compact_feature_label(key) for key in new_cycle_keys)
            )
        if prev_to_base:
            feature_diff = prev_to_base.get("feature", {})
            if feature_diff:
                lines.append(
                    f"- Previous -> baseline delta: {feature_diff.get('feature_coverage_delta', 0.0):+.2f}"
                )
                new_keys = feature_diff.get("new_hit_feature_keys", [])[:6]
                if new_keys:
                    lines.append(
                        "- New combinations: " + ", ".join(compact_feature_label(key) for key in new_keys)
                    )
        if base_to_candidate:
            candidate_feature_diff = base_to_candidate.get("feature", {})
            if candidate_feature_diff:
                lines.append(
                    f"- Baseline -> candidate delta: {candidate_feature_diff.get('feature_coverage_delta', 0.0):+.2f}"
                )
        if item.get("iteration_report"):
            lines.append(f"- Iteration report: [{Path(item['iteration_report']).name}]({item['iteration_report']})")
        lines.append("")

    content = "\n".join(lines)
    report_path.write_text(content, encoding="utf-8")
    latest_report_path.write_text(content, encoding="utf-8")
    return report_path
