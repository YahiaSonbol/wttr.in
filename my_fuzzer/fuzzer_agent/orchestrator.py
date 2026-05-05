from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import time

from .core import (
    ensure_dirs,
    load_default_environment,
    load_env_file,
    make_config,
    parse_args,
    remove_if_exists,
    require_runtime_dependencies,
)
from .coverage_runner import (
    append_iteration_log,
    build_image,
    coverage_summary,
    docker,
    extract_coverage,
    generate_testcases,
    result_summary,
    run_http_tests,
    save_finding,
    save_grammar_snapshot,
    start_container,
    stop_and_collect_container,
    wait_for_server,
    write_json,
    write_markdown_results,
)
from .llm import build_mutation_prompt, call_llm
from .validator import apply_mutation_plan, parse_mutation_plan, validate_candidate_grammar


def _write_attempt_trace(config, iteration: int, attempt: int, payload: dict) -> None:
    trace_file = config.logs_dir / f"iteration_{iteration:03d}_llm_attempt_{attempt:02d}.json"
    write_json(payload, trace_file)


def _write_attempt_prompt(config, iteration: int, attempt: int, prompt: str) -> Path:
    prompt_file = config.logs_dir / f"iteration_{iteration:03d}_llm_attempt_{attempt:02d}_prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    return prompt_file


def _preview_text(text: str | None, limit: int = 240) -> str:
    if not text:
        return ""
    single_line = " ".join(text.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 3] + "..."


def _write_run_report(config, report: dict) -> Path:
    started_at = report["started_at"].replace(":", "").replace("-", "")
    started_at = started_at.replace("T", "_").replace("Z", "")
    report_path = config.logs_dir / f"run_report_{started_at}.md"
    latest_report_path = config.logs_dir / "latest_run_report.md"

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
        if item.get("results_json"):
            lines.append(f"- Baseline results: [{Path(item['results_json']).name}]({item['results_json']})")
        if item.get("candidate_results_json"):
            lines.append(
                f"- Candidate results: [{Path(item['candidate_results_json']).name}]({item['candidate_results_json']})"
            )
        if item.get("attempt_trace_files"):
            trace_names = ", ".join(Path(path).name for path in item["attempt_trace_files"])
            lines.append(f"- LLM attempt traces: {trace_names}")
        if item.get("attempt_prompt_files"):
            prompt_names = ", ".join(Path(path).name for path in item["attempt_prompt_files"])
            lines.append(f"- LLM prompts: {prompt_names}")
        lines.append("")

    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- Iteration log: [{config.iteration_log.name}]({config.iteration_log})")
    lines.append(f"- Logs directory: [{config.logs_dir.name}]({config.logs_dir})")
    lines.append(f"- Findings directory: [{config.findings_dir.name}]({config.findings_dir})")
    lines.append(f"- History directory: [{config.history_dir.name}]({config.history_dir})")
    lines.append("")

    content = "\n".join(lines)
    report_path.write_text(content, encoding="utf-8")
    latest_report_path.write_text(content, encoding="utf-8")
    return report_path


def _run_measurement_batch(
    config,
    client,
    iteration: int,
    grammar_text: str,
    label: str,
) -> tuple[float | None, dict | None, list, dict]:
    original_grammar = config.grammar_file.read_text(encoding="utf-8")
    config.grammar_file.write_text(grammar_text, encoding="utf-8")

    try:
        remove_if_exists(config.cache_dir / ".coverage")
        remove_if_exists(config.coverage_json)

        print(f"[fuzz:{label}] Generating payloads from the {label} grammar.")
        payloads = generate_testcases(config)
        print(f"[fuzz:{label}] Generated {len(payloads)} payloads.")
        container = start_container(client, config, iteration)
        results = []
        execution_error = None

        try:
            print(f"[http:{label}] Waiting for local server at {config.base_url}")
            wait_for_server(config.base_url, config.startup_timeout)
            print(f"[http:{label}] Running {len(payloads)} HTTP requests.")
            results = run_http_tests(payloads, config.request_timeout)
        except Exception as exc:  # pragma: no cover
            execution_error = exc
        finally:
            print(f"[docker:{label}] Stopping container and collecting logs.")
            exit_code, container_logs = stop_and_collect_container(container, config.stop_timeout)

        results_markdown = config.logs_dir / f"iteration_{iteration:03d}_{label}_results.md"
        results_json = config.logs_dir / f"iteration_{iteration:03d}_{label}_results.json"
        write_markdown_results(results, results_markdown)
        write_json([asdict(result) for result in results], results_json)
        if label == "baseline":
            write_markdown_results(results, config.generator_dir / "test_results.md")

        metadata = {
            "label": label,
            "tests_run": len(payloads),
            "http": result_summary(results),
            "container_exit_code": exit_code,
            "container_logs": container_logs,
            "results_json": str(results_json),
            "results_markdown": str(results_markdown),
            "execution_error": str(execution_error) if execution_error else None,
        }

        if execution_error is not None:
            return None, None, results, metadata

        print(f"[coverage:{label}] Extracting coverage data.")
        coverage_data = extract_coverage(config)
        coverage_digest = coverage_summary(coverage_data, config)
        percent_covered = float(coverage_digest["percent_covered"] or 0.0)
        print(f"[coverage:{label}] {percent_covered:.2f}%")

        metadata["coverage"] = coverage_digest
        return percent_covered, coverage_data, results, metadata
    finally:
        config.grammar_file.write_text(original_grammar, encoding="utf-8")


def _mutate_grammar(
    config,
    iteration: int,
    current_grammar: str,
    results,
    coverage_data,
) -> tuple[str | None, dict]:
    feedback: str | None = None
    raw_response = ""
    candidate_grammar: str | None = None
    validation_output = ""
    rationale = ""
    attempt_traces: list[dict] = []

    for attempt in range(1, config.llm_attempts + 1):
        print(f"[llm] Attempt {attempt}/{config.llm_attempts}")
        prompt = build_mutation_prompt(
            config,
            current_grammar,
            results,
            coverage_data,
            validation_feedback=feedback,
        )
        prompt_file = _write_attempt_prompt(config, iteration, attempt, prompt)
        attempt_trace: dict = {
            "attempt": attempt,
            "prompt_file": str(prompt_file),
            "feedback_in": feedback,
        }

        try:
            llm_result = call_llm(config, prompt)
            raw_response = llm_result.raw_response
            attempt_trace["llm_trace"] = llm_result.trace
            attempt_trace["raw_response"] = raw_response
        except Exception as exc:
            validation_output = f"LLM execution failed: {exc}"
            feedback = (
                "The previous LLM call failed before producing usable JSON.\n"
                f"Error:\n{validation_output}\n"
                "Return JSON only with small updates to the existing mutable rules."
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
        except Exception as exc:
            validation_output = str(exc)
            feedback = (
                "Your previous response could not be parsed or applied.\n"
                f"Error:\n{validation_output}\n"
                "Return JSON only and replace only the allowed existing rules."
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
            }

        feedback = (
            "Your previous candidate grammar was rejected.\n"
            f"Validation error:\n{validation_output}\n"
            "Try again with smaller edits to the existing mutable rules only."
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
    }


def main() -> int:
    load_default_environment()
    args = parse_args()
    if args.env_file:
        load_env_file(Path(args.env_file).expanduser().resolve(), override=True)

    require_runtime_dependencies()
    config = make_config(args)
    ensure_dirs(
        config.cache_dir,
        config.findings_dir,
        config.history_dir,
        config.logs_dir,
        config.generator_dir,
    )

    client = docker.from_env()
    if config.build_image:
        build_image(client, config)

    best_coverage = -1.0
    best_grammar_text = config.grammar_file.read_text(encoding="utf-8")
    normal_exit_codes = {0, 130, 143, None}
    run_started_ts = time.time()
    run_started_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
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
                percent_covered, coverage_data, results, baseline_meta = _run_measurement_batch(
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

            if baseline_meta["execution_error"]:
                iteration_record["decision"] = "execution_error"
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
                "http": baseline_meta["http"],
                "container_exit_code": exit_code,
                "coverage_json": str(config.coverage_json),
                "results_json": baseline_meta["results_json"],
            }
            append_iteration_log(config, iteration_summary)
            print(f"[coverage] {percent_covered:.2f}%")

            if percent_covered > best_coverage:
                best_coverage = percent_covered
                best_grammar_text = current_grammar
                save_grammar_snapshot(config, iteration, "best", current_grammar)

            if iteration == config.iterations:
                iteration_record["mutation_status"] = "skipped_final_iteration"
                iteration_record["decision"] = "kept_champion"
                iteration_record["llm_attempts"] = 0
                run_iterations.append(iteration_record)
                print("[llm] Skipping mutation on the final iteration because there is no subsequent run to use a new grammar.")
                continue

            print("[llm] Starting simple LangGraph mutation step.")
            candidate_grammar, mutation_meta = _mutate_grammar(config, iteration, current_grammar, results, coverage_data)
            attempt_traces = mutation_meta.get("attempt_traces", [])
            iteration_record["llm_attempts"] = len(attempt_traces)
            iteration_record["attempt_trace_files"] = [
                str(config.logs_dir / f"iteration_{iteration:03d}_llm_attempt_{trace['attempt']:02d}.json")
                for trace in attempt_traces
            ]
            iteration_record["attempt_prompt_files"] = [
                trace["prompt_file"] for trace in attempt_traces if trace.get("prompt_file")
            ]
            iteration_record["validation_output"] = mutation_meta.get("validation_output")
            iteration_record["mutation_rationale"] = mutation_meta.get("rationale")
            if attempt_traces:
                last_parsed_plan = attempt_traces[-1].get("parsed_plan", {})
                iteration_record["proposed_rules"] = [
                    update["rule"] for update in last_parsed_plan.get("updates", [])
                ]

            if candidate_grammar is None:
                iteration_record["mutation_status"] = "rejected"
                iteration_record["decision"] = "kept_current_grammar"
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
                candidate_percent, _, _, candidate_meta = _run_measurement_batch(
                    config,
                    client,
                    iteration,
                    candidate_grammar,
                    "candidate",
                )
            except Exception as exc:
                iteration_record["mutation_status"] = "candidate_execution_error"
                iteration_record["decision"] = "kept_champion"
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
            if candidate_percent >= best_coverage:
                best_coverage = candidate_percent
                best_grammar_text = candidate_grammar
                config.grammar_file.write_text(candidate_grammar, encoding="utf-8")
                save_grammar_snapshot(config, iteration, "after", candidate_grammar)
                save_grammar_snapshot(config, iteration, "best", candidate_grammar)
                iteration_record["mutation_status"] = "accepted"
                iteration_record["decision"] = "promoted_to_champion"
                run_iterations.append(iteration_record)
                print(f"[llm] Accepted candidate grammar at {candidate_percent:.2f}% (delta {improvement:+.2f}).")
                continue

            config.grammar_file.write_text(best_grammar_text, encoding="utf-8")
            iteration_record["mutation_status"] = "regression"
            iteration_record["decision"] = "kept_champion"
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
        report_path = _write_run_report(config, report)
        print(f"[report] Wrote run report to {report_path}")

    return 0
