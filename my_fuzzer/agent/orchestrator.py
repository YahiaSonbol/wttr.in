from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import docker
import json
import time

from .utils.cli_utils import (
    ensure_dirs,
    remove_if_exists,
    write_json,
)
from .core.config import (
    make_config,
    parse_args,
)
from .utils.docker_utils import (
    build_image,
)
from .utils.coverage_utils import (
    save_finding,
    save_grammar_snapshot,
    append_iteration_log,
    load_latest_baseline_snapshot,
    save_latest_baseline_snapshot,
)
from .utils.coverage_diff_utils import (
    aggregate_coverages,
    compute_coverage_diff,
    load_coverage_json,
    write_aggregate_coverage_report,
    write_coverage_diff_report,
)
from .utils.grammar_diff_utils import (
    write_grammar_diff_report,
)
from .utils.report_utils import (
    ensure_run_report_dirs,
    make_run_report_slug,
    write_markdown,
    write_unavailable_report,
)
from .test_runner import (
    run_testing_batch,
)
from .llm import (
    run_mutation_graph,
)
from .validator import (
    apply_mutation_plan,
    parse_mutation_plan,
    parse_planner_output,
    validate_planner_rewriter_consistency,
    validate_candidate_grammar,
)
from .utils.llm_utils import iteration_history_formatter


# ---------------------------------------------------------------------------
# Artifact logging helpers
# ---------------------------------------------------------------------------

def _write_attempt_artifacts(config, iteration: int, attempt: int, state: dict) -> dict:
    """Write separate planner/rewriter prompt+output files for one attempt."""
    prefix = f"iteration_{iteration:03d}_llm_attempt_{attempt:02d}"
    files: dict[str, str] = {}

    for key, suffix in [
        ("planner_prompt", "planner_prompt.md"),
        ("planner_output", "planner_output.json"),
        ("rewriter_prompt", "rewriter_prompt.md"),
        ("rewriter_output", "rewriter_output.json"),
    ]:
        content = state.get(key, "")
        if content:
            path = config.logs_dir / f"{prefix}_{suffix}"
            path.write_text(content if isinstance(content, str) else json.dumps(content, indent=2), encoding="utf-8")
            files[suffix] = str(path)

    trace = state.get("trace", [])
    if trace:
        trace_path = config.logs_dir / f"{prefix}_trace.json"
        write_json(trace, trace_path)
        files["trace"] = str(trace_path)

    return files


def _write_attempt_trace(config, iteration: int, attempt: int, payload: dict) -> None:
    trace_file = config.logs_dir / f"iteration_{iteration:03d}_llm_attempt_{attempt:02d}.json"
    write_json(payload, trace_file)


def _preview_text(text: str | None, limit: int = 240) -> str:
    if not text:
        return ""
    single_line = " ".join(text.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3] + "..."


def _initialize_run_reporting(config, run_started_at: str) -> None:
    run_slug = make_run_report_slug(run_started_at)
    run_paths = ensure_run_report_dirs(config, run_slug)
    config.run_slug = run_slug
    config.run_reports_dir = run_paths["run_reports_dir"]
    config.run_grammar_reports_dir = run_paths["grammar_dir"]
    config.run_coverage_reports_dir = run_paths["coverage_dir"]
    config.run_summary_reports_dir = run_paths["summary_dir"]


def _baseline_labels(snapshot: dict | None, fallback_grammar_label: str) -> tuple[str, str]:
    if not snapshot:
        return "no_previous_baseline", fallback_grammar_label

    metadata = snapshot.get("metadata", {})
    prior_label = metadata.get("label", "latest_saved_baseline")
    current_label = fallback_grammar_label
    return prior_label, current_label


def _write_baseline_comparison_reports(
    config,
    iteration: int,
    current_grammar: str,
    coverage_data: dict,
    coverage_percent: float,
) -> dict[str, str]:
    grammar_report = config.run_grammar_reports_dir / f"iteration_{iteration:03d}_baseline_vs_latest_saved_baseline.md"
    coverage_report = config.run_coverage_reports_dir / f"iteration_{iteration:03d}_baseline_vs_latest_saved_baseline.md"
    previous_baseline = load_latest_baseline_snapshot(config)
    current_label = f"{config.run_slug}_baseline_iteration_{iteration:03d}"

    if previous_baseline is None:
        grammar_path = write_unavailable_report(
            grammar_report,
            "Grammar Diff Report",
            "No previous saved baseline is available yet.",
            {"Iteration": iteration, "Current Baseline": current_label},
        )
        coverage_path = write_unavailable_report(
            coverage_report,
            "Coverage Diff Report",
            "No previous saved baseline is available yet.",
            {"Iteration": iteration, "Current Baseline": current_label},
        )
        status = "no_previous_baseline"
        baseline_reference = "none"
    else:
        previous_label, current_label = _baseline_labels(previous_baseline, current_label)
        grammar_path = write_grammar_diff_report(
            grammar_report,
            iteration=iteration,
            from_label=previous_label,
            to_label=current_label,
            decision="baseline_comparison",
            mutation_status="baseline",
            old_text=previous_baseline["grammar_text"],
            new_text=current_grammar,
            metadata={"Baseline Reference": previous_label},
        )
        coverage_diff = compute_coverage_diff(
            previous_baseline["coverage_data"],
            coverage_data,
            max_files=config.max_missing_files,
            max_lines_per_file=config.max_missing_lines_per_file,
        )
        coverage_path = write_coverage_diff_report(
            coverage_report,
            iteration=iteration,
            from_label=previous_label,
            to_label=current_label,
            diff_data=coverage_diff,
            metadata={"Baseline Reference": previous_label},
        )
        status = "available"
        baseline_reference = previous_label

    save_latest_baseline_snapshot(
        config,
        grammar_text=current_grammar,
        coverage_data=coverage_data,
        metadata={
            "label": current_label,
            "iteration": iteration,
            "run_slug": config.run_slug,
            "coverage_percent": coverage_percent,
            "saved_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        },
    )
    return {
        "baseline_reference": baseline_reference,
        "baseline_grammar_diff_report": str(grammar_path),
        "baseline_coverage_diff_report": str(coverage_path),
        "baseline_coverage_diff_status": status,
    }


def _write_candidate_comparison_reports(
    config,
    iteration: int,
    current_grammar: str,
    candidate_grammar: str | None,
    decision: str,
    mutation_status: str,
    *,
    candidate_coverage_data: dict | None,
    coverage_unavailable_reason: str | None = None,
    metadata: dict | None = None,
) -> dict[str, str]:
    grammar_report = config.run_grammar_reports_dir / f"iteration_{iteration:03d}_current_vs_candidate.md"
    coverage_report = config.run_coverage_reports_dir / f"iteration_{iteration:03d}_candidate_vs_latest_saved_baseline.md"
    baseline_label = f"{config.run_slug}_baseline_iteration_{iteration:03d}"
    candidate_label = f"{config.run_slug}_candidate_iteration_{iteration:03d}"
    if candidate_grammar is None:
        grammar_path = write_unavailable_report(
            grammar_report,
            "Grammar Diff Report",
            "Candidate grammar text is not available.",
            {
                "Iteration": iteration,
                "Decision": decision,
                "Mutation Status": mutation_status,
            },
        )
    else:
        grammar_path = write_grammar_diff_report(
            grammar_report,
            iteration=iteration,
            from_label=baseline_label,
            to_label=candidate_label,
            decision=decision,
            mutation_status=mutation_status,
            old_text=current_grammar,
            new_text=candidate_grammar,
            metadata=metadata or {},
        )

    latest_baseline = load_latest_baseline_snapshot(config)
    if candidate_coverage_data is None:
        coverage_path = write_unavailable_report(
            coverage_report,
            "Coverage Diff Report",
            coverage_unavailable_reason or "Candidate coverage data is not available.",
            {
                "Iteration": iteration,
                "Decision": decision,
                "Mutation Status": mutation_status,
            },
        )
        status = "not_available"
    elif latest_baseline is None:
        coverage_path = write_unavailable_report(
            coverage_report,
            "Coverage Diff Report",
            "No saved baseline coverage is available for comparison.",
            {"Iteration": iteration, "Decision": decision},
        )
        status = "missing_baseline"
    else:
        baseline_label = latest_baseline.get("metadata", {}).get("label", "latest_saved_baseline")
        coverage_diff = compute_coverage_diff(
            latest_baseline["coverage_data"],
            candidate_coverage_data,
            max_files=config.max_missing_files,
            max_lines_per_file=config.max_missing_lines_per_file,
        )
        coverage_path = write_coverage_diff_report(
            coverage_report,
            iteration=iteration,
            from_label=baseline_label,
            to_label=candidate_label,
            diff_data=coverage_diff,
            metadata={"Baseline Reference": baseline_label},
        )
        status = "available"

    return {
        "candidate_grammar_diff_report": str(grammar_path),
        "candidate_coverage_diff_report": str(coverage_path),
        "candidate_coverage_diff_status": status,
    }


def _write_cycle_aggregate_coverage_report(config, iterations: list[dict]) -> dict[str, Any] | None:
    coverage_items: list[dict[str, Any]] = []

    for item in iterations:
        iteration = item.get("iteration")

        baseline_coverage_json = item.get("coverage_json")
        if baseline_coverage_json and Path(baseline_coverage_json).exists():
            coverage_items.append(
                {
                    "label": f"iteration_{iteration:03d}_baseline",
                    "coverage_data": load_coverage_json(Path(baseline_coverage_json)),
                }
            )

        candidate_coverage_json = item.get("candidate_coverage_json")
        if candidate_coverage_json and Path(candidate_coverage_json).exists():
            coverage_items.append(
                {
                    "label": f"iteration_{iteration:03d}_candidate",
                    "coverage_data": load_coverage_json(Path(candidate_coverage_json)),
                }
            )

    if not coverage_items:
        return None

    aggregate_data = aggregate_coverages(
        coverage_items,
        max_files=config.max_missing_files,
        max_lines_per_file=config.max_missing_lines_per_file,
    )
    aggregate_report_path = config.run_summary_reports_dir / "cycle_aggregate_coverage.md"
    write_aggregate_coverage_report(
        aggregate_report_path,
        aggregate_data=aggregate_data,
        metadata={"Run Slug": config.run_slug},
    )
    return {
        "aggregate_coverage_report": str(aggregate_report_path),
        "aggregate_coverage_percent": aggregate_data["totals"]["percent_covered"],
        "aggregate_covered_lines": aggregate_data["totals"]["covered_lines"],
        "aggregate_missing_lines": aggregate_data["totals"]["missing_lines"],
        "aggregate_num_statements": aggregate_data["totals"]["num_statements"],
        "aggregate_source_count": aggregate_data["source_count"],
    }


def _write_run_report(config, report: dict) -> Path:
    started_at = report["started_at"].replace(":", "").replace("-", "")
    started_at = started_at.replace("T", "_").replace("Z", "")
    report_path = config.logs_dir / f"run_report_{started_at}.md"
    latest_report_path = config.logs_dir / "latest_run_report.md"
    summary_report_path = None
    if config.run_summary_reports_dir is not None:
        summary_report_path = config.run_summary_reports_dir / "run_summary.md"

    lines: list[str] = []
    lines.append("# Fuzzer Loop Run Report")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    overview_rows = [
        ("Status", report["status"]),
        ("Started At", report["started_at"]),
        ("Finished At", report["finished_at"]),
        ("Duration Seconds", f"{report['duration_seconds']:.2f}"),
        ("Configured Iterations", str(report["config"]["iterations"])),
        ("Completed Iterations", str(report["completed_iterations"])),
        ("Tests Per Batch", str(report["config"]["case_count"])),
        ("Generation Depth", str(report["config"]["generation_depth"])),
        ("Image", report["config"]["image"]),
        ("Base URL", report["config"]["base_url"]),
        ("LLM Model", report["config"]["llm_model"]),
        ("Champion Coverage", f"{report['champion_coverage']:.2f}%"),
        (
            "Aggregate Coverage",
            (
                f"{report['aggregate_coverage_percent']:.2f}%"
                if report.get("aggregate_coverage_percent") is not None
                else "-"
            ),
        ),
        ("Final Grammar", report["final_grammar"]),
        ("Findings Count", str(report["findings_count"])),
    ]
    if report.get("error"):
        overview_rows.append(("Error", report["error"]))
    for key, value in overview_rows:
        lines.append(f"| {key} | {value} |")

    lines.append("")
    lines.append("## Iteration Summary")
    lines.append("")
    lines.append("| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|")
    for item in report["iterations"]:
        http_counts = item.get("http_counts", {})
        lines.append(
            "| {iteration} | {tests} | {coverage:.2f}% | {success} | {warning} | {crash} | {error} | {attempts} | {mutation} | {candidate_cov} | {decision} |".format(
                iteration=item["iteration"],
                tests=item.get("tests_run", 0),
                coverage=item.get("coverage_percent", 0.0),
                success=http_counts.get("SUCCESS", 0),
                warning=http_counts.get("WARNING", 0),
                crash=http_counts.get("CRASH", 0),
                error=http_counts.get("ERROR", 0),
                attempts=item.get("llm_attempts", 0),
                mutation=item.get("mutation_status", "-"),
                candidate_cov=(
                    f"{item['candidate_coverage_percent']:.2f}%"
                    if item.get("candidate_coverage_percent") is not None
                    else "-"
                ),
                decision=item.get("decision", "-"),
            )
        )

    if report.get("aggregate_coverage_percent") is not None:
        lines.append("## Aggregate Coverage")
        lines.append("")
        lines.append(f"- Coverage across all included iterations: {report['aggregate_coverage_percent']:.2f}%")
        lines.append(f"- Covered lines: {report['aggregate_covered_lines']}")
        lines.append(f"- Missing lines: {report['aggregate_missing_lines']}")
        lines.append(f"- Executable lines: {report['aggregate_num_statements']}")
        lines.append(f"- Included coverage artifacts: {report['aggregate_source_count']}")
        if report.get("aggregate_coverage_report"):
            lines.append(
                f"- Aggregate report: [{Path(report['aggregate_coverage_report']).name}]({report['aggregate_coverage_report']})"
            )
        lines.append("")

    lines.append("")
    lines.append("## Iteration Details")
    lines.append("")
    for item in report["iterations"]:
        lines.append(f"### Iteration {item['iteration']}")
        lines.append("")
        lines.append(f"- Tests run: {item.get('tests_run', 0)}")
        lines.append(f"- Baseline coverage: {item.get('coverage_percent', 0.0):.2f}%")
        lines.append(f"- Container exit code: {item.get('container_exit_code')}")
        lines.append(f"- Mutation status: {item.get('mutation_status', '-')}")
        lines.append(f"- Decision: {item.get('decision', '-')}")
        if item.get("candidate_coverage_percent") is not None:
            lines.append(f"- Candidate coverage: {item['candidate_coverage_percent']:.2f}%")
        if item.get("coverage_delta") is not None:
            lines.append(f"- Candidate delta vs champion: {item['coverage_delta']:+.2f}")
        if item.get("mutation_rationale"):
            lines.append(f"- Mutation rationale: {item['mutation_rationale']}")
        if item.get("proposed_rules"):
            lines.append(f"- Proposed rules: {', '.join(item['proposed_rules'])}")
        if item.get("validation_output"):
            lines.append(f"- Validation summary: `{_preview_text(item['validation_output'], 500)}`")
        if item.get("planner_analysis"):
            lines.append(f"- Planner analysis: {_preview_text(item['planner_analysis'], 300)}")
        if item.get("reachability"):
            reach = item["reachability"]
            lines.append(f"- Reachable by grammar: {len(reach.get('grammar', []))} items")
            lines.append(f"- Reachable by headers only: {len(reach.get('headers', []))} items")
            lines.append(f"- Unreachable (harness): {len(reach.get('harness', []))} items")
        if item.get("line_target_hints"):
            lines.append(f"- Line target hints: {len(item['line_target_hints'])} items")
        if item.get("results_json"):
            lines.append(f"- Baseline results: [{Path(item['results_json']).name}]({item['results_json']})")
        if item.get("coverage_json"):
            lines.append(f"- Baseline coverage JSON: [{Path(item['coverage_json']).name}]({item['coverage_json']})")
        if item.get("candidate_results_json"):
            lines.append(
                f"- Candidate results: [{Path(item['candidate_results_json']).name}]({item['candidate_results_json']})"
            )
        if item.get("candidate_coverage_json"):
            lines.append(
                f"- Candidate coverage JSON: [{Path(item['candidate_coverage_json']).name}]({item['candidate_coverage_json']})"
            )
        if item.get("baseline_grammar_diff_report"):
            lines.append(
                f"- Baseline grammar diff: [{Path(item['baseline_grammar_diff_report']).name}]({item['baseline_grammar_diff_report']})"
            )
        if item.get("baseline_coverage_diff_report"):
            lines.append(
                f"- Baseline coverage diff ({item.get('baseline_coverage_diff_status', 'unknown')}): "
                f"[{Path(item['baseline_coverage_diff_report']).name}]({item['baseline_coverage_diff_report']})"
            )
        if item.get("candidate_grammar_diff_report"):
            lines.append(
                f"- Candidate grammar diff: [{Path(item['candidate_grammar_diff_report']).name}]({item['candidate_grammar_diff_report']})"
            )
        if item.get("candidate_coverage_diff_report"):
            lines.append(
                f"- Candidate coverage diff ({item.get('candidate_coverage_diff_status', 'unknown')}): "
                f"[{Path(item['candidate_coverage_diff_report']).name}]({item['candidate_coverage_diff_report']})"
            )
        if item.get("artifact_files"):
            artifact_names = ", ".join(Path(p).name for p in item["artifact_files"].values())
            lines.append(f"- LLM artifacts: {artifact_names}")
        lines.append("")

    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- Iteration log: [{config.iteration_log.name}]({config.iteration_log})")
    lines.append(f"- Logs directory: [{config.logs_dir.name}]({config.logs_dir})")
    lines.append(f"- Findings directory: [{config.findings_dir.name}]({config.findings_dir})")
    lines.append(f"- History directory: [{config.history_dir.name}]({config.history_dir})")
    if config.run_reports_dir is not None:
        lines.append(f"- Run reports directory: [{config.run_reports_dir.name}]({config.run_reports_dir})")
    if report.get("aggregate_coverage_report"):
        lines.append(
            f"- Aggregate coverage report: "
            f"[{Path(report['aggregate_coverage_report']).name}]({report['aggregate_coverage_report']})"
        )
    lines.append("")

    content = "\n".join(lines)
    report_path.write_text(content, encoding="utf-8")
    latest_report_path.write_text(content, encoding="utf-8")
    if summary_report_path is not None:
        write_markdown(summary_report_path, lines)
    return report_path


# ---------------------------------------------------------------------------
# Core mutation loop — uses the two-node LangGraph
# ---------------------------------------------------------------------------

def _mutate_grammar(
    config,
    iteration: int,
    current_grammar: str,
    results,
    coverage_data,
    iteration_history_text: str = "",
) -> tuple[str | None, dict]:
    feedback: str | None = None
    raw_response = ""
    candidate_grammar: str | None = None
    validation_output = ""
    rationale = ""
    attempt_traces: list[dict] = []
    planner_analysis = ""
    reachability: dict[str, list[str]] = {}
    line_target_hints: list[dict[str, str]] = []
    request_profiles: dict[str, list[str]] | None = None

    for attempt in range(1, config.llm_attempts + 1):
        print(f"[llm] Attempt {attempt}/{config.llm_attempts}")
        attempt_trace: dict = {"attempt": attempt, "feedback_in": feedback}

        try:
            graph_state = run_mutation_graph(
                config,
                current_grammar,
                results,
                coverage_data,
                validation_feedback=feedback,
                iteration_history=iteration_history_text,
            )
            attempt_trace["graph_trace"] = graph_state.get("trace", [])

            # Log artifacts
            artifact_files = _write_attempt_artifacts(config, iteration, attempt, graph_state)
            attempt_trace["artifact_files"] = artifact_files

            # Extract planner analysis for reporting
            planner_raw = graph_state.get("planner_output", "")
            attempt_trace["planner_output"] = planner_raw
            try:
                planner_parsed = parse_planner_output(planner_raw)
                planner_analysis = planner_parsed.analysis
                reachability = {
                    "grammar": planner_parsed.reachable_by_grammar,
                    "headers": planner_parsed.reachable_by_headers_only,
                    "harness": planner_parsed.unreachable_harness_limits,
                }
                line_target_hints = planner_parsed.line_target_hints
                request_profiles = planner_parsed.request_space_recommendations
                attempt_trace["line_target_hints"] = line_target_hints
                attempt_trace["planner_parsed"] = True
            except ValueError as exc:
                attempt_trace["planner_parse_warning"] = str(exc)

            # Extract rewriter output
            raw_response = graph_state.get("final_raw_response", "")
            attempt_trace["raw_response"] = raw_response
            request_profiles = graph_state.get("request_profiles", request_profiles)

        except Exception as exc:
            validation_output = f"LLM graph execution failed: {exc}"
            feedback = (
                "The previous LLM call failed before producing usable JSON.\n"
                f"Error:\n{validation_output}\n"
                "Return JSON only with small updates to existing unprotected rules."
            )
            attempt_trace["status"] = "llm_error"
            attempt_trace["error"] = validation_output
            attempt_trace["feedback_out"] = feedback
            _write_attempt_trace(config, iteration, attempt, attempt_trace)
            attempt_traces.append(attempt_trace)
            print(f"[llm] Attempt {attempt} execution error: {validation_output}")
            continue

        try:
            plan = parse_mutation_plan(raw_response)
            rationale = plan.rationale
            candidate_grammar = apply_mutation_plan(current_grammar, plan)
            attempt_trace["parsed_plan"] = {
                "rationale": rationale,
                "updates": [
                    {"rule": update.rule, "replacement": update.replacement}
                    for update in plan.updates
                ],
            }
            changed_rules = ", ".join(update.rule for update in plan.updates)
            print(f"[llm] Attempt {attempt} proposed rules: {changed_rules}")
            if rationale:
                print(f"[llm] Attempt {attempt} rationale: {rationale}")

            # Consistency check
            try:
                planner_parsed_obj = parse_planner_output(planner_raw)
                warnings = validate_planner_rewriter_consistency(planner_parsed_obj, plan, current_grammar)
                if warnings:
                    for w in warnings:
                        print(f"[llm] Consistency warning: {w}")
                    attempt_trace["consistency_warnings"] = warnings
            except ValueError:
                pass

        except Exception as exc:
            validation_output = str(exc)
            feedback = (
                "Your previous response could not be parsed or applied.\n"
                f"Error:\n{validation_output}\n"
                "Return JSON only and replace only existing unprotected rules."
            )
            attempt_trace["status"] = "parse_or_apply_error"
            attempt_trace["error"] = validation_output
            attempt_trace["feedback_out"] = feedback
            _write_attempt_trace(config, iteration, attempt, attempt_trace)
            attempt_traces.append(attempt_trace)
            print(f"[llm] Attempt {attempt} parse/apply error: {validation_output}")
            continue

        is_valid, validation_output = validate_candidate_grammar(config, candidate_grammar)
        attempt_trace["candidate_grammar"] = candidate_grammar
        attempt_trace["validation_output"] = validation_output
        if is_valid:
            attempt_trace["status"] = "accepted"
            _write_attempt_trace(config, iteration, attempt, attempt_trace)
            attempt_traces.append(attempt_trace)
            print(f"[llm] Attempt {attempt} accepted.")
            return candidate_grammar, {
                "raw_response": raw_response,
                "rationale": rationale,
                "validation_output": validation_output,
                "attempt_traces": attempt_traces,
                "planner_analysis": planner_analysis,
                "reachability": reachability,
                "line_target_hints": line_target_hints,
                "request_profiles": request_profiles,
            }

        feedback = (
            "Your previous candidate grammar was rejected.\n"
            f"Validation error:\n{validation_output}\n"
            "Try again with smaller edits to existing unprotected rules only."
        )
        attempt_trace["status"] = "validation_error"
        attempt_trace["feedback_out"] = feedback
        _write_attempt_trace(config, iteration, attempt, attempt_trace)
        attempt_traces.append(attempt_trace)
        print(f"[llm] Attempt {attempt} validation error: {validation_output}")

    return None, {
        "raw_response": raw_response,
        "candidate_grammar": candidate_grammar,
        "rationale": rationale,
        "validation_output": validation_output,
        "attempt_traces": attempt_traces,
        "planner_analysis": planner_analysis,
        "reachability": reachability,
        "line_target_hints": line_target_hints,
        "request_profiles": request_profiles,
    }


def main() -> int:
    args = parse_args()
    config = make_config(args)
    ensure_dirs(
        config.cache_dir,
        config.findings_dir,
        config.history_dir,
        config.logs_dir,
        config.generator_dir,
        config.reports_dir,
        config.baselines_dir,
    )

    client = docker.from_env()
    if config.build_image:
        build_image(client, config)

    best_coverage = -1.0
    best_grammar_text = config.grammar_file.read_text(encoding="utf-8")
    normal_exit_codes = {0, 130, 143, None}
    run_started_ts = time.time()
    run_started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    _initialize_run_reporting(config, run_started_at)
    run_iterations: list[dict] = []
    run_status = "completed"
    run_error: str | None = None
    report_path: Path | None = None

    try:
        for iteration in range(1, config.iterations + 1):
            print(f"\n=== Iteration {iteration}/{config.iterations} ===")

            current_grammar = config.grammar_file.read_text(encoding="utf-8")
            save_grammar_snapshot(config, iteration, "before", current_grammar)
            remove_if_exists(config.cache_dir / ".coverage")
            remove_if_exists(config.coverage_json)
            iteration_record = {
                "iteration": iteration,
                "tests_configured": config.case_count,
                "mutation_status": "not_started",
                "decision": "pending",
            }

            try:
                percent_covered, coverage_data, results, baseline_meta = run_testing_batch(
                    config,
                    client,
                    iteration,
                    current_grammar,
                    "baseline",
                )
            except Exception as exc:
                iteration_record["decision"] = "execution_error"
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                save_finding(
                    config,
                    iteration,
                    "execution_error",
                    current_grammar,
                    None,
                    {"error": str(exc)},
                )
                raise

            iteration_record["tests_run"] = baseline_meta["tests_run"]
            iteration_record["results_json"] = baseline_meta["results_json"]
            iteration_record["coverage_json"] = baseline_meta.get("coverage_json")
            iteration_record["http_counts"] = baseline_meta["http"].get("counts", {})
            iteration_record["container_exit_code"] = baseline_meta["container_exit_code"]
            iteration_record["comparison_mode"] = "latest_saved_baseline"

            if baseline_meta["execution_error"]:
                iteration_record["decision"] = "execution_error"
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                save_finding(
                    config,
                    iteration,
                    "execution_error",
                    current_grammar,
                    None,
                    {
                        "error": baseline_meta["execution_error"],
                        "container_logs": baseline_meta["container_logs"],
                    },
                )
                raise RuntimeError(baseline_meta["execution_error"])

            for result in results:
                if result.status == "CRASH":
                    payload_file = config.testcases_dir / result.filename
                    payload_text = payload_file.read_text(encoding="utf-8") if payload_file.exists() else None
                    save_finding(
                        config,
                        iteration,
                        f"http_{result.status_code}_{result.filename}",
                        current_grammar,
                        payload_text,
                        {"result": asdict(result)},
                    )

            exit_code = baseline_meta["container_exit_code"]
            if exit_code not in normal_exit_codes:
                save_finding(
                    config,
                    iteration,
                    f"container_exit_{exit_code}",
                    current_grammar,
                    None,
                    {"exit_code": exit_code, "container_logs": baseline_meta["container_logs"]},
                )

            coverage_digest = baseline_meta["coverage"]
            iteration_record["coverage"] = coverage_digest
            iteration_record["coverage_percent"] = percent_covered
            baseline_report_info = _write_baseline_comparison_reports(
                config,
                iteration,
                current_grammar,
                coverage_data,
                percent_covered,
            )
            iteration_record.update(baseline_report_info)
            print(f"[coverage] {percent_covered:.2f}%")

            if percent_covered > best_coverage:
                best_coverage = percent_covered
                best_grammar_text = current_grammar
                save_grammar_snapshot(config, iteration, "best", current_grammar)

            if iteration == config.iterations:
                iteration_record["mutation_status"] = "skipped_final_iteration"
                iteration_record["decision"] = "kept_champion"
                iteration_record["llm_attempts"] = 0
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                print("[llm] Skipping mutation on the final iteration because there is no subsequent run to use a new grammar.")
                continue

            # Build iteration history for planner context
            history_text = iteration_history_formatter(run_iterations, max_entries=5)

            print("[llm] Starting two-node LangGraph mutation step.")
            candidate_grammar, mutation_meta = _mutate_grammar(
                config, iteration, current_grammar, results, coverage_data,
                iteration_history_text=history_text,
            )
            attempt_traces = mutation_meta.get("attempt_traces", [])
            iteration_record["llm_attempts"] = len(attempt_traces)
            iteration_record["artifact_files"] = (
                attempt_traces[-1].get("artifact_files", {}) if attempt_traces else {}
            )
            iteration_record["validation_output"] = mutation_meta.get("validation_output")
            iteration_record["mutation_rationale"] = mutation_meta.get("rationale")
            iteration_record["planner_analysis"] = mutation_meta.get("planner_analysis")
            iteration_record["reachability"] = mutation_meta.get("reachability")
            iteration_record["line_target_hints"] = mutation_meta.get("line_target_hints")
            if attempt_traces:
                last_parsed_plan = attempt_traces[-1].get("parsed_plan", {})
                iteration_record["proposed_rules"] = [
                    update["rule"] for update in last_parsed_plan.get("updates", [])
                ]

            request_profiles = mutation_meta.get("request_profiles")

            if candidate_grammar is None:
                iteration_record["mutation_status"] = "rejected"
                iteration_record["decision"] = "kept_current_grammar"
                iteration_record.update(
                    _write_candidate_comparison_reports(
                        config,
                        iteration,
                        current_grammar,
                        mutation_meta.get("candidate_grammar"),
                        decision=iteration_record["decision"],
                        mutation_status=iteration_record["mutation_status"],
                        candidate_coverage_data=None,
                        coverage_unavailable_reason="Candidate grammar was rejected during validation and was not executed.",
                        metadata={
                            "Validation Output": _preview_text(iteration_record.get("validation_output"), 200),
                            "Proposed Rules": iteration_record.get("proposed_rules", []),
                        },
                    )
                )
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                save_finding(
                    config,
                    iteration,
                    "invalid_candidate_grammar",
                    current_grammar,
                    None,
                    mutation_meta,
                )
                print("[llm] Candidate grammar was rejected after validation retries; keeping previous grammar.")
                continue

            print("[llm] Evaluating candidate grammar against the current champion.")
            try:
                candidate_percent, candidate_coverage_data, _, candidate_meta = run_testing_batch(
                    config,
                    client,
                    iteration,
                    candidate_grammar,
                    "candidate",
                    request_profiles=request_profiles,
                )
            except Exception as exc:
                iteration_record["mutation_status"] = "candidate_execution_error"
                iteration_record["decision"] = "kept_champion"
                iteration_record.update(
                    _write_candidate_comparison_reports(
                        config,
                        iteration,
                        current_grammar,
                        candidate_grammar,
                        decision=iteration_record["decision"],
                        mutation_status=iteration_record["mutation_status"],
                        candidate_coverage_data=None,
                        coverage_unavailable_reason=f"Candidate execution failed before coverage collection: {exc}",
                        metadata={"Proposed Rules": iteration_record.get("proposed_rules", [])},
                    )
                )
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                save_finding(
                    config,
                    iteration,
                    "candidate_execution_error",
                    current_grammar,
                    None,
                    {
                        "error": str(exc),
                        "candidate_grammar": candidate_grammar,
                        "mutation_meta": mutation_meta,
                    },
                )
                config.grammar_file.write_text(best_grammar_text, encoding="utf-8")
                print(f"[llm] Candidate evaluation failed: {exc}")
                print("[llm] Keeping the current champion grammar.")
                continue

            if candidate_meta["execution_error"]:
                iteration_record["mutation_status"] = "candidate_execution_error"
                iteration_record["decision"] = "kept_champion"
                iteration_record["candidate_results_json"] = candidate_meta.get("results_json")
                iteration_record.update(
                    _write_candidate_comparison_reports(
                        config,
                        iteration,
                        current_grammar,
                        candidate_grammar,
                        decision=iteration_record["decision"],
                        mutation_status=iteration_record["mutation_status"],
                        candidate_coverage_data=None,
                        coverage_unavailable_reason=(
                            "Candidate execution ended before coverage collection: "
                            f"{candidate_meta['execution_error']}"
                        ),
                        metadata={"Proposed Rules": iteration_record.get("proposed_rules", [])},
                    )
                )
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                save_finding(
                    config,
                    iteration,
                    "candidate_execution_error",
                    current_grammar,
                    None,
                    {
                        "error": candidate_meta["execution_error"],
                        "candidate_grammar": candidate_grammar,
                        "candidate_meta": candidate_meta,
                        "mutation_meta": mutation_meta,
                    },
                )
                config.grammar_file.write_text(best_grammar_text, encoding="utf-8")
                print(f"[llm] Candidate evaluation failed: {candidate_meta['execution_error']}")
                print("[llm] Keeping the current champion grammar.")
                continue

            improvement = candidate_percent - best_coverage
            iteration_record["candidate_coverage_percent"] = candidate_percent
            iteration_record["coverage_delta"] = improvement
            iteration_record["candidate_results_json"] = candidate_meta.get("results_json")
            iteration_record["candidate_coverage_json"] = candidate_meta.get("coverage_json")
            if candidate_percent >= best_coverage:
                best_coverage = candidate_percent
                best_grammar_text = candidate_grammar
                config.grammar_file.write_text(candidate_grammar, encoding="utf-8")
                save_grammar_snapshot(config, iteration, "after", candidate_grammar)
                save_grammar_snapshot(config, iteration, "best", candidate_grammar)
                iteration_record["mutation_status"] = "accepted"
                iteration_record["decision"] = "promoted_to_champion"
                iteration_record.update(
                    _write_candidate_comparison_reports(
                        config,
                        iteration,
                        current_grammar,
                        candidate_grammar,
                        decision=iteration_record["decision"],
                        mutation_status=iteration_record["mutation_status"],
                        candidate_coverage_data=candidate_coverage_data,
                        metadata={"Proposed Rules": iteration_record.get("proposed_rules", [])},
                    )
                )
                append_iteration_log(config, iteration_record)
                run_iterations.append(iteration_record)
                print(f"[llm] Accepted candidate grammar at {candidate_percent:.2f}% (delta {improvement:+.2f}).")
                continue

            config.grammar_file.write_text(best_grammar_text, encoding="utf-8")
            iteration_record["mutation_status"] = "regression"
            iteration_record["decision"] = "kept_champion"
            iteration_record.update(
                _write_candidate_comparison_reports(
                    config,
                    iteration,
                    current_grammar,
                    candidate_grammar,
                    decision=iteration_record["decision"],
                    mutation_status=iteration_record["mutation_status"],
                    candidate_coverage_data=candidate_coverage_data,
                    metadata={"Proposed Rules": iteration_record.get("proposed_rules", [])},
                )
            )
            append_iteration_log(config, iteration_record)
            run_iterations.append(iteration_record)
            save_finding(
                config,
                iteration,
                "candidate_regression",
                current_grammar,
                None,
                {
                    "candidate_grammar": candidate_grammar,
                    "candidate_coverage": candidate_percent,
                    "best_coverage": best_coverage,
                    "delta": improvement,
                    "candidate_meta": candidate_meta,
                    "mutation_meta": mutation_meta,
                },
            )
            print(f"[llm] Rejected candidate grammar at {candidate_percent:.2f}% (delta {improvement:+.2f}).")
            print(f"[llm] Keeping champion grammar at {best_coverage:.2f}%.")
    except Exception as exc:
        run_status = "failed"
        run_error = str(exc)
        raise
    finally:
        aggregate_report_info = _write_cycle_aggregate_coverage_report(config, run_iterations)
        report = {
            "status": run_status,
            "error": run_error,
            "started_at": run_started_at,
            "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "duration_seconds": time.time() - run_started_ts,
            "completed_iterations": len(run_iterations),
            "champion_coverage": best_coverage if best_coverage >= 0 else 0.0,
            "final_grammar": str(config.grammar_file),
            "findings_count": len(list(config.findings_dir.glob("iteration_*"))),
            "config": {
                "iterations": config.iterations,
                "case_count": config.case_count,
                "generation_depth": config.generation_depth,
                "image": config.image,
                "base_url": config.base_url,
                "llm_model": config.llm_model,
            },
            "iterations": run_iterations,
        }
        if aggregate_report_info:
            report.update(aggregate_report_info)
        report_path = _write_run_report(config, report)
        print(f"[report] Wrote run report to {report_path}")

    return 0
