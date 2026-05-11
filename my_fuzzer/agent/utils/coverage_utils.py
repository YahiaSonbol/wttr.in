from typing import Any
from ..core.config import FuzzerConfig
from ..models import TestResult
from .cli_utils import run_command, write_json, ensure_dirs
from dataclasses import asdict
from pathlib import Path
import json 
import shutil
import sys
import re

def coverage_excerpt(
    coverage_data: dict[str, Any],
    config: FuzzerConfig,
) -> dict[str, Any]:
    excerpt: dict[str, Any] = {"files": {}}
    prioritized_files = sorted(
        coverage_data.get("files", {}).items(),
        key=lambda item: len(item[1].get("missing_lines", [])),
        reverse=True,
    )

    for file_name, file_data in prioritized_files[: config.max_missing_files]:
        missing_lines = file_data.get("missing_lines", [])
        if not missing_lines:
            continue
        excerpt["files"][file_name] = {
            "executed_lines": file_data.get("executed_lines", [])[: config.max_missing_lines_per_file],
            "missing_lines": missing_lines[: config.max_missing_lines_per_file],
            "summary": file_data.get("summary", {}),
        }

    excerpt["totals"] = coverage_data.get("totals", {})
    return excerpt

def write_markdown_results(results: list[TestResult], output_file: Path) -> None:
    with output_file.open("w", encoding="utf-8") as handle:
        handle.write("# Backend API Test Results\n\n")
        handle.write("| Filename | URL | Status | Status Code | Response Time (ms) | Feature Key | Ignored Reason | Error |\n")
        handle.write("|----------|-----|--------|-------------|--------------------|-------------|----------------|-------|\n")
        for result in results:
            handle.write(
                f"| {result.filename} | {result.url} | {result.status} | "
                f"{result.status_code if result.status_code is not None else 'N/A'} | "
                f"{result.response_time_ms if result.response_time_ms is not None else 'N/A'} | "
                f"{result.feature_key or '-'} | "
                f"{result.ignored_reason or '-'} | "
                f"{result.error_message or '-'} |\n"
            )


def extract_coverage(config: FuzzerConfig) -> dict[str, Any]:
    coverage_data_file = config.cache_dir / ".coverage"
    if not coverage_data_file.exists():
        raise RuntimeError(f"Expected coverage file was not written: {coverage_data_file}")

    temp_coverage_file = coverage_data_file.with_name(".coverage.docker")
    shutil.copy2(coverage_data_file, temp_coverage_file)

    run_command(
        [
            sys.executable,
            "-m",
            "coverage",
            "combine",
            f"--data-file={coverage_data_file}",
            str(temp_coverage_file),
        ],
        cwd=config.repo_root,
    )

    run_command(
        [
            sys.executable,
            "-m",
            "coverage",
            "json",
            f"--data-file={coverage_data_file}",
            "-o",
            str(config.coverage_json),
        ],
        cwd=config.repo_root,
    )

    return json.loads(config.coverage_json.read_text(encoding="utf-8"))

def coverage_summary(
    coverage_data: dict[str, Any],
    config: FuzzerConfig,
) -> dict[str, Any]:
    files = coverage_data.get("files", {})
    trimmed_missing: dict[str, list[int]] = {}
    total_missing_lines = 0

    for _, file_data in files.items():
        total_missing_lines += len(file_data.get("missing_lines", []))

    prioritized_files = sorted(
        files.items(),
        key=lambda item: len(item[1].get("missing_lines", [])),
        reverse=True,
    )

    for file_name, file_data in prioritized_files[: config.max_missing_files]:
        missing_lines = file_data.get("missing_lines", [])
        if not missing_lines:
            continue
        trimmed_missing[file_name] = missing_lines[: config.max_missing_lines_per_file]

    totals = coverage_data.get("totals", {})
    percent = totals.get("percent_covered")
    if percent is None:
        percent = totals.get("percent_covered_display")

    return {
        "percent_covered": percent,
        "covered_lines": totals.get("covered_lines"),
        "num_statements": totals.get("num_statements"),
        "missing_lines_total": total_missing_lines,
        "missing_lines_by_file": trimmed_missing,
    }

def result_summary(results: list[TestResult]) -> dict[str, Any]:
    counts = {"SUCCESS": 0, "WARNING": 0, "CRASH": 0, "ERROR": 0}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1

    return {
        "counts": counts,
        "crashes": [asdict(result) for result in results if result.status == "CRASH"],
        "errors": [asdict(result) for result in results if result.status == "ERROR"],
        "non_200": [asdict(result) for result in results if result.status != "SUCCESS"][:20],
        "successful_samples": [asdict(result) for result in results if result.status == "SUCCESS"][:5],
    }


def save_finding(
    config: FuzzerConfig,
    iteration: int,
    label: str,
    grammar_text: str,
    payload_text: str | None,
    metadata: dict[str, Any],
) -> None:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "_", label).strip("_") or "finding"
    finding_dir = config.findings_dir / f"iteration_{iteration:03d}_{slug}"
    ensure_dirs(finding_dir)

    (finding_dir / "url.g4").write_text(grammar_text, encoding="utf-8")
    if payload_text is not None:
        (finding_dir / "payload.txt").write_text(payload_text, encoding="utf-8")
    write_json(metadata, finding_dir / "metadata.json")


def save_grammar_snapshot(config: FuzzerConfig, iteration: int, suffix: str, grammar_text: str) -> None:
    snapshot = config.history_dir / f"iteration_{iteration:03d}_{suffix}.g4"
    snapshot.write_text(grammar_text, encoding="utf-8")


def append_iteration_log(config: FuzzerConfig, summary: dict[str, Any]) -> None:
    with config.iteration_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(summary) + "\n")
