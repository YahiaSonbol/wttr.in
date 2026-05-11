from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
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
)
from .utils.report_utils import (
    ensure_report_dirs,
    write_coverage_diff_report,
    write_cycle_report,
    write_iteration_report,
    write_url_diff_report,
)
from .utils.feature_coverage import (
    feature_delta,
    merge_feature_summaries,
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
            path = config.raw_dir / f"{prefix}_{suffix}"
            path.write_text(content if isinstance(content, str) else json.dumps(content, indent=2), encoding="utf-8")
            files[suffix] = str(path)

    trace = state.get("trace", [])
    if trace:
        trace_path = config.raw_dir / f"{prefix}_trace.json"
        write_json(trace, trace_path)
        files["trace"] = str(trace_path)

    return files


def _write_attempt_trace(config, iteration: int, attempt: int, payload: dict) -> None:
    trace_file = config.raw_dir / f"iteration_{iteration:03d}_llm_attempt_{attempt:02d}.json"
    write_json(payload, trace_file)


def _preview_text(text: str | None, limit: int = 240) -> str:
    if not text:
        return ""
    single_line = " ".join(text.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3] + "..."


def _score_tuple(feature_summary: dict | None, line_coverage: float | None) -> tuple[float, float, float]:
    summary = feature_summary or {}
    return (
        float(summary.get("feature_coverage_percent", 0.0) or 0.0),
        float(summary.get("successful_feature_coverage_percent", 0.0) or 0.0),
        float(line_coverage or 0.0),
    )


def _update_cumulative_feature_progress(
    config,
    iteration_record: dict,
    cumulative_feature_summary: dict | None,
    *iteration_feature_summaries: dict | None,
) -> dict:
    next_cumulative = merge_feature_summaries(
        [cumulative_feature_summary, *iteration_feature_summaries],
        config.base_url,
    )
    iteration_record["cumulative_feature_summary"] = next_cumulative
    iteration_record["cumulative_feature_coverage_percent"] = next_cumulative.get(
        "feature_coverage_percent",
        0.0,
    )
    iteration_record["cumulative_successful_feature_coverage_percent"] = next_cumulative.get(
        "successful_feature_coverage_percent",
        0.0,
    )
    iteration_record["cumulative_feature_delta"] = feature_delta(
        cumulative_feature_summary,
        next_cumulative,
    )
    return next_cumulative


def _write_iteration_artifacts(
    config,
    iteration_record: dict,
    previous_baseline_coverage,
    previous_baseline_feature,
    previous_baseline_results,
    baseline_coverage,
    baseline_feature: dict,
    baseline_results,
    candidate_coverage=None,
    candidate_feature: dict | None = None,
    candidate_results=None,
) -> None:
    coverage_diff_path, diff_summary = write_coverage_diff_report(
        config,
        iteration_record["iteration"],
        previous_baseline_coverage,
        previous_baseline_feature,
        baseline_coverage,
        baseline_feature,
        candidate_coverage=candidate_coverage,
        candidate_feature=candidate_feature,
    )
    url_diff_path = write_url_diff_report(
        config,
        iteration_record["iteration"],
        previous_baseline_results,
        baseline_results,
        candidate_results=candidate_results,
    )
    iteration_record["coverage_diff_report"] = str(coverage_diff_path)
    iteration_record["url_diff_report"] = str(url_diff_path)
    iteration_record["diff_summary"] = diff_summary
    iteration_report_path = write_iteration_report(config, iteration_record)
    iteration_record["iteration_report"] = str(iteration_report_path)


def _write_run_report(config, report: dict) -> Path:
    return write_cycle_report(config, report)


# ---------------------------------------------------------------------------
# Core mutation loop — uses the two-node LangGraph
# ---------------------------------------------------------------------------

def _mutate_grammar(
    config,
    iteration: int,
    current_grammar: str,
    results,
    coverage_data,
    feature_summary: dict,
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
                feature_summary,
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
                request_profiles = planner_parsed.request_space_recommendations
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
        config.raw_dir,
        config.reports_dir,
        config.generator_dir,
    )
    ensure_report_dirs(config)

    client = docker.from_env()
    if config.build_image:
        build_image(client, config)

    best_score = (-1.0, -1.0, -1.0)
    best_grammar_text = config.grammar_file.read_text(encoding="utf-8")
    normal_exit_codes = {0, 130, 143, None}
    run_started_ts = time.time()
    run_started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    run_iterations: list[dict] = []
    run_status = "completed"
    run_error: str | None = None
    report_path: Path | None = None
    previous_baseline_coverage = None
    previous_baseline_feature = None
    previous_baseline_results = None
    cumulative_cycle_feature = None

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
            iteration_record["http_counts"] = baseline_meta["http"].get("counts", {})
            iteration_record["container_exit_code"] = baseline_meta["container_exit_code"]
            iteration_record["feature_summary"] = baseline_meta["feature"]
            iteration_record["generation"] = baseline_meta.get("generation", {})
            iteration_record["baseline_feature_json"] = baseline_meta.get("feature_json")
            iteration_record["feature_coverage_percent"] = baseline_meta["feature"].get("feature_coverage_percent", 0.0)
            iteration_record["successful_feature_coverage_percent"] = baseline_meta["feature"].get(
                "successful_feature_coverage_percent", 0.0
            )
            if baseline_meta.get("coverage_json"):
                iteration_record["coverage_json"] = baseline_meta["coverage_json"]

            if baseline_meta["execution_error"]:
                iteration_record["decision"] = "execution_error"
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    None,
                    baseline_meta["feature"],
                    results,
                )
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
            iteration_record["coverage_percent"] = percent_covered

            iteration_summary = {
                "iteration": iteration,
                "coverage": coverage_digest,
                "feature": baseline_meta["feature"],
                "feature_coverage_percent": baseline_meta["feature"].get("feature_coverage_percent", 0.0),
                "generation": baseline_meta.get("generation", {}),
                "http": baseline_meta["http"],
                "container_exit_code": exit_code,
                "coverage_json": baseline_meta.get("coverage_json"),
                "feature_json": baseline_meta.get("feature_json"),
                "results_json": baseline_meta["results_json"],
            }
            append_iteration_log(config, iteration_summary)
            print(f"[coverage] {percent_covered:.2f}%")

            baseline_score = _score_tuple(baseline_meta["feature"], percent_covered)
            if baseline_score > best_score:
                best_score = baseline_score
                best_grammar_text = current_grammar
                save_grammar_snapshot(config, iteration, "best", current_grammar)

            if iteration == config.iterations:
                iteration_record["mutation_status"] = "skipped_final_iteration"
                iteration_record["decision"] = "kept_champion"
                iteration_record["llm_attempts"] = 0
                cumulative_cycle_feature = _update_cumulative_feature_progress(
                    config,
                    iteration_record,
                    cumulative_cycle_feature,
                    baseline_meta["feature"],
                )
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    coverage_data,
                    baseline_meta["feature"],
                    results,
                )
                run_iterations.append(iteration_record)
                previous_baseline_coverage = coverage_data
                previous_baseline_feature = baseline_meta["feature"]
                previous_baseline_results = results
                print("[llm] Skipping mutation on the final iteration because there is no subsequent run to use a new grammar.")
                continue

            # Build iteration history for planner context
            history_text = iteration_history_formatter(run_iterations, max_entries=5)

            print("[llm] Starting two-node LangGraph mutation step.")
            candidate_grammar, mutation_meta = _mutate_grammar(
                config, iteration, current_grammar, results, coverage_data, baseline_meta["feature"],
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
            if attempt_traces:
                last_parsed_plan = attempt_traces[-1].get("parsed_plan", {})
                iteration_record["proposed_rules"] = [
                    update["rule"] for update in last_parsed_plan.get("updates", [])
                ]

            request_profiles = mutation_meta.get("request_profiles")

            if candidate_grammar is None:
                iteration_record["mutation_status"] = "rejected"
                iteration_record["decision"] = "kept_current_grammar"
                cumulative_cycle_feature = _update_cumulative_feature_progress(
                    config,
                    iteration_record,
                    cumulative_cycle_feature,
                    baseline_meta["feature"],
                )
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    coverage_data,
                    baseline_meta["feature"],
                    results,
                )
                run_iterations.append(iteration_record)
                previous_baseline_coverage = coverage_data
                previous_baseline_feature = baseline_meta["feature"]
                previous_baseline_results = results
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
                candidate_percent, candidate_coverage_data, candidate_results, candidate_meta = run_testing_batch(
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
                cumulative_cycle_feature = _update_cumulative_feature_progress(
                    config,
                    iteration_record,
                    cumulative_cycle_feature,
                    baseline_meta["feature"],
                )
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    coverage_data,
                    baseline_meta["feature"],
                    results,
                )
                run_iterations.append(iteration_record)
                previous_baseline_coverage = coverage_data
                previous_baseline_feature = baseline_meta["feature"]
                previous_baseline_results = results
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

            iteration_record["candidate_results_json"] = candidate_meta.get("results_json")
            iteration_record["candidate_feature_summary"] = candidate_meta.get("feature")
            iteration_record["candidate_generation"] = candidate_meta.get("generation", {})
            iteration_record["candidate_feature_json"] = candidate_meta.get("feature_json")
            iteration_record["candidate_feature_coverage_percent"] = candidate_meta.get("feature", {}).get(
                "feature_coverage_percent", 0.0
            )
            iteration_record["candidate_successful_feature_coverage_percent"] = candidate_meta.get("feature", {}).get(
                "successful_feature_coverage_percent", 0.0
            )
            if candidate_meta.get("coverage_json"):
                iteration_record["candidate_coverage_json"] = candidate_meta["coverage_json"]

            if candidate_meta["execution_error"]:
                iteration_record["mutation_status"] = "candidate_execution_error"
                iteration_record["decision"] = "kept_champion"
                cumulative_cycle_feature = _update_cumulative_feature_progress(
                    config,
                    iteration_record,
                    cumulative_cycle_feature,
                    baseline_meta["feature"],
                )
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    coverage_data,
                    baseline_meta["feature"],
                    results,
                )
                run_iterations.append(iteration_record)
                previous_baseline_coverage = coverage_data
                previous_baseline_feature = baseline_meta["feature"]
                previous_baseline_results = results
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

            champion_score_before = best_score
            candidate_score = _score_tuple(candidate_meta["feature"], candidate_percent)
            improvement = candidate_score[0] - champion_score_before[0]
            iteration_record["candidate_coverage_percent"] = candidate_percent
            iteration_record["feature_delta"] = improvement
            iteration_record["line_coverage_delta"] = candidate_percent - percent_covered
            if candidate_score >= best_score:
                best_score = candidate_score
                best_grammar_text = candidate_grammar
                config.grammar_file.write_text(candidate_grammar, encoding="utf-8")
                save_grammar_snapshot(config, iteration, "after", candidate_grammar)
                save_grammar_snapshot(config, iteration, "best", candidate_grammar)
                iteration_record["mutation_status"] = "accepted"
                iteration_record["decision"] = "promoted_to_champion"
                cumulative_cycle_feature = _update_cumulative_feature_progress(
                    config,
                    iteration_record,
                    cumulative_cycle_feature,
                    baseline_meta["feature"],
                    candidate_meta["feature"],
                )
                _write_iteration_artifacts(
                    config,
                    iteration_record,
                    previous_baseline_coverage,
                    previous_baseline_feature,
                    previous_baseline_results,
                    coverage_data,
                    baseline_meta["feature"],
                    results,
                    candidate_coverage=candidate_coverage_data,
                    candidate_feature=candidate_meta["feature"],
                    candidate_results=candidate_results,
                )
                run_iterations.append(iteration_record)
                previous_baseline_coverage = coverage_data
                previous_baseline_feature = baseline_meta["feature"]
                previous_baseline_results = results
                print(
                    f"[llm] Accepted candidate grammar at feature {candidate_meta['feature'].get('feature_coverage_percent', 0.0):.2f}% "
                    f"and line coverage {candidate_percent:.2f}%."
                )
                continue

            config.grammar_file.write_text(best_grammar_text, encoding="utf-8")
            iteration_record["mutation_status"] = "regression"
            iteration_record["decision"] = "kept_champion"
            cumulative_cycle_feature = _update_cumulative_feature_progress(
                config,
                iteration_record,
                cumulative_cycle_feature,
                baseline_meta["feature"],
                candidate_meta["feature"],
            )
            _write_iteration_artifacts(
                config,
                iteration_record,
                previous_baseline_coverage,
                previous_baseline_feature,
                previous_baseline_results,
                coverage_data,
                baseline_meta["feature"],
                results,
                candidate_coverage=candidate_coverage_data,
                candidate_feature=candidate_meta["feature"],
                candidate_results=candidate_results,
            )
            run_iterations.append(iteration_record)
            previous_baseline_coverage = coverage_data
            previous_baseline_feature = baseline_meta["feature"]
            previous_baseline_results = results
            save_finding(
                config,
                iteration,
                "candidate_regression",
                current_grammar,
                None,
                {
                    "candidate_grammar": candidate_grammar,
                    "candidate_coverage": candidate_percent,
                    "candidate_feature_coverage": candidate_meta["feature"].get("feature_coverage_percent", 0.0),
                    "best_feature_coverage": best_score[0],
                    "delta": improvement,
                    "candidate_meta": candidate_meta,
                    "mutation_meta": mutation_meta,
                },
            )
            print(
                f"[llm] Rejected candidate grammar at feature {candidate_meta['feature'].get('feature_coverage_percent', 0.0):.2f}% "
                f"(delta {improvement:+.2f})."
            )
            print(f"[llm] Keeping champion grammar at feature {best_score[0]:.2f}%.")
    except Exception as exc:
        run_status = "failed"
        run_error = str(exc)
        raise
    finally:
        report = {
            "status": run_status,
            "error": run_error,
            "started_at": run_started_at,
            "finished_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "duration_seconds": time.time() - run_started_ts,
            "completed_iterations": len(run_iterations),
            "champion_feature_coverage": best_score[0] if best_score[0] >= 0 else 0.0,
            "champion_successful_feature_coverage": best_score[1] if best_score[1] >= 0 else 0.0,
            "champion_line_coverage": best_score[2] if best_score[2] >= 0 else 0.0,
            "cumulative_feature_coverage": (cumulative_cycle_feature or {}).get("feature_coverage_percent", 0.0),
            "cumulative_successful_feature_coverage": (
                cumulative_cycle_feature or {}
            ).get("successful_feature_coverage_percent", 0.0),
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
            "cumulative_feature_summary": cumulative_cycle_feature or {},
        }
        report_path = _write_run_report(config, report)
        print(f"[report] Wrote run report to {report_path}")

    return 0
