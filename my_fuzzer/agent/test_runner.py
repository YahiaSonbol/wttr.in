from __future__ import annotations

import random
import time
from pathlib import Path
import requests
from dataclasses import asdict
from .models import TestResult, RequestSpec
from .profiles import resolve_profiles, random_profile_set
from .utils.cli_utils import (
    write_json,
    remove_if_exists,
)
from .utils.grammarinator_utils import (
    generate_testcases,
)
from .utils.docker_utils import (
    start_container,
    stop_and_collect_container,
)
from .utils.coverage_utils import (
    extract_coverage,
    coverage_summary,
    write_markdown_results,
    result_summary,
)

def wait_for_server(base_url: str, timeout_seconds: float) -> None:
    deadline = time.time() + timeout_seconds
    last_error: Exception | None = None

    while time.time() < deadline:
        try:
            response = requests.get(base_url + "/", timeout=2)
            if response.status_code < 500:
                return
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(0.5)

    raise RuntimeError(f"Server at {base_url} did not become ready: {last_error}")


def build_request_specs(
    payloads: list[Path],
    request_profiles: dict[str, list[str]] | None = None,
) -> list[RequestSpec]:
    """Convert payload files into ``RequestSpec`` objects with headers.

    If the planner provided ``request_profiles``, those are resolved into
    concrete header sets and distributed across payloads. Otherwise a mix
    of random profiles is used.
    """
    header_sets = resolve_profiles(request_profiles)

    specs: list[RequestSpec] = []
    for i, payload in enumerate(payloads):
        url = payload.read_text(encoding="utf-8").strip()
        # Round-robin through available header sets
        headers = dict(header_sets[i % len(header_sets)]) if header_sets else {}
        specs.append(RequestSpec(url=url, headers=headers))
    return specs


def _compact_url(url: str, limit: int = 70) -> str:
    """Truncate a URL for log display."""
    if len(url) <= limit:
        return url
    return url[: limit - 3] + "..."


def run_http_tests(
    specs: list[RequestSpec],
    timeout_seconds: float,
) -> list[TestResult]:
    results: list[TestResult] = []
    total = len(specs)
    counts = {"SUCCESS": 0, "WARNING": 0, "CRASH": 0, "ERROR": 0}

    for i, spec in enumerate(specs):
        url = spec.url
        headers = spec.headers or {}
        host = headers.get("Host", "-")
        ua_short = headers.get("User-Agent", "-")[:12]
        progress = f"[test] {i+1:>3}/{total}"
        print(f"{progress}  {_compact_url(url)}  Host={host}  UA={ua_short}")
        if not url:
            results.append(
                TestResult(
                    filename=f"payload_{i}.txt",
                    url="",
                    status="ERROR",
                    status_code=None,
                    error_message="Empty payload file",
                    response_time_ms=None,
                    headers=headers,
                )
            )
            continue

        start = time.perf_counter()
        try:
            response = requests.get(url, headers=headers, timeout=timeout_seconds)
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            status = "SUCCESS" if response.status_code == 200 else "WARNING"
            if response.status_code >= 500:
                status = "CRASH"

            results.append(
                TestResult(
                    filename=f"payload_{i}.txt",
                    url=url,
                    status=status,
                    status_code=response.status_code,
                    error_message=None,
                    response_time_ms=elapsed_ms,
                    headers=headers,
                )
            )
        except requests.RequestException as exc:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            results.append(
                TestResult(
                    filename=f"payload_{i}.txt",
                    url=url,
                    status="ERROR",
                    status_code=None,
                    error_message=str(exc),
                    response_time_ms=elapsed_ms,
                    headers=headers,
                )
            )

        counts[results[-1].status] = counts.get(results[-1].status, 0) + 1

    # Print compact summary
    print(f"[test] ─── Results: {counts['SUCCESS']}✓  {counts['WARNING']}⚠  {counts['CRASH']}✗  {counts['ERROR']}⊘  ({total} total)")
    return results



def run_testing_batch(
    config,
    client,
    iteration: int,
    grammar_text: str,
    label: str,
    request_profiles: dict[str, list[str]] | None = None,
) -> tuple[float | None, dict | None, list, dict]:
    original_grammar = config.grammar_file.read_text(encoding="utf-8")
    config.grammar_file.write_text(grammar_text, encoding="utf-8")

    try:
        remove_if_exists(config.cache_dir / ".coverage")
        remove_if_exists(config.coverage_json)

        print(f"[fuzz:{label}] Generating payloads from the {label} grammar.")
        payloads = generate_testcases(config)
        print(f"[fuzz:{label}] Generated {len(payloads)} payloads.")

        # Build request specs with header profiles
        specs = build_request_specs(payloads, request_profiles)
        print(f"[fuzz:{label}] Built {len(specs)} request specs with header profiles.")

        container = start_container(client, config, iteration)
        results = []
        execution_error = None

        try:
            print(f"[http:{label}] Waiting for local server at {config.base_url}")
            wait_for_server(config.base_url, config.startup_timeout)
            print(f"[http:{label}] Running {len(specs)} HTTP requests.")
            results = run_http_tests(specs, config.request_timeout)
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
