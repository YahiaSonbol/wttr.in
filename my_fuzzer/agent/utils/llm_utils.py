import textwrap
from typing import Any
from ..models import TestResult
from ..core.config import FuzzerConfig
from .coverage_utils import coverage_excerpt

def feedback_block_formatter(validation_feedback: str | None) -> str:
    if not validation_feedback:
        return ""
    return textwrap.dedent(
        f"""
        ## Fix The Last Attempt

        {validation_feedback}
        """
    ).strip()


def _escape_markdown_cell(value: str | None, limit: int = 200) -> str:
    if not value:
        return "-"
    single_line = " ".join(value.split())
    if len(single_line) > limit:
        single_line = single_line[: limit - 3] + "..."
    return single_line.replace("|", "\\|")



def results_formatter(results: list[TestResult] | list[dict[str, Any]]) -> str:
    """Format HTTP test results as a compact summary for the LLM prompt.

    Shows aggregate counts plus a small sample of interesting results
    to keep prompt size manageable (~1-2K chars instead of 20K+).
    """
    if not results:
        return "No HTTP requests were recorded in the previous run."

    # Normalize to dicts for uniform access
    items: list[dict[str, Any]] = []
    for r in results:
        if isinstance(r, dict):
            items.append(r)
        else:
            items.append({
                "url": r.url, "status": r.status,
                "status_code": r.status_code, "error_message": r.error_message,
                "response_time_ms": r.response_time_ms,
                "headers": getattr(r, "headers", None),
            })

    # Aggregate counts
    counts: dict[str, int] = {}
    for item in items:
        s = item.get("status", "UNKNOWN")
        counts[s] = counts.get(s, 0) + 1

    lines = [f"**{len(items)} requests total**: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))]

    # Response time stats
    times = [item["response_time_ms"] for item in items if item.get("response_time_ms") is not None]
    if times:
        lines.append(f"Response times: min={min(times)}ms, max={max(times)}ms, avg={sum(times)//len(times)}ms")

    # Status code distribution
    code_counts: dict[str, int] = {}
    for item in items:
        code = item.get("status_code")
        if code is not None:
            key = str(code)
            code_counts[key] = code_counts.get(key, 0) + 1
    if code_counts:
        lines.append("Status codes: " + ", ".join(f"{code}×{n}" for code, n in sorted(code_counts.items())))

    # Sample crashes/errors (most valuable for the planner)
    crashes = [item for item in items if item.get("status") in ("CRASH", "ERROR")]
    if crashes:
        lines.append("")
        lines.append(f"### Crash/Error Samples ({len(crashes)} total, showing up to 5)")
        for item in crashes[:5]:
            url = _escape_markdown_cell(item.get("url", ""), 100)
            host = (item.get("headers") or {}).get("Host", "-")
            err = _escape_markdown_cell(item.get("error_message"), 80)
            lines.append(f"- `{item.get('status_code', '?')}` {url} (Host={host}) {err}")

    # Sample unique URL patterns (deduplicated by path prefix)
    seen_prefixes: set[str] = set()
    unique_samples: list[dict[str, Any]] = []
    for item in items:
        url = item.get("url", "")
        # Extract path part
        prefix = url.split("?")[0].split("localhost:8002")[-1][:30] if "localhost" in url else url[:30]
        if prefix not in seen_prefixes:
            seen_prefixes.add(prefix)
            unique_samples.append(item)

    lines.append("")
    lines.append(f"### URL Diversity ({len(seen_prefixes)} unique path prefixes, showing up to 8)")
    for item in unique_samples[:8]:
        url = _escape_markdown_cell(item.get("url", ""), 80)
        host = (item.get("headers") or {}).get("Host", "-")
        lines.append(f"- `{item.get('status_code', '?')}` {url} (Host={host})")

    return "\n".join(lines)


def coverage_data_formatter(coverage_data: dict[str, Any], config: FuzzerConfig) -> str:
    excerpt = coverage_excerpt(coverage_data, config)
    totals = excerpt.get("totals", {})
    percent = totals.get("percent_covered")
    if percent is None:
        percent = totals.get("percent_covered_display", "unknown")

    lines = [f"Overall coverage: {percent}%", ""]
    files = excerpt.get("files", {})
    if not files:
        lines.append("No missing-line hotspots were recorded.")
        return "\n".join(lines)

    # Cap to top 5 files, max 20 missing lines each
    for file_name, file_data in list(files.items())[:5]:
        missing = file_data.get("missing_lines", [])[:20]
        missing_str = ", ".join(str(l) for l in missing) or "none"
        if len(file_data.get("missing_lines", [])) > 20:
            missing_str += f" ... (+{len(file_data['missing_lines']) - 20} more)"
        lines.append(f"- **{file_name}**: missing lines [{missing_str}]")
    return "\n".join(lines).rstrip()


def missing_hotspots_formatter(coverage_data: dict[str, Any], config: FuzzerConfig) -> str:
    """Format the top missing-line hotspots for the planner prompt."""
    files = coverage_data.get("files", {})
    if not files:
        return "No missing-line data available."

    prioritized = sorted(
        files.items(),
        key=lambda item: len(item[1].get("missing_lines", [])),
        reverse=True,
    )

    lines: list[str] = []
    for file_name, file_data in prioritized[:5]:
        missing = file_data.get("missing_lines", [])
        if not missing:
            continue
        capped = missing[:15]
        extra = f" (+{len(missing) - 15} more)" if len(missing) > 15 else ""
        lines.append(f"**{file_name}** ({len(missing)} missing): lines {', '.join(str(l) for l in capped)}{extra}")

    return "\n".join(lines) if lines else "No significant missing-line hotspots."


def iteration_history_formatter(history: list[dict[str, Any]], max_entries: int = 5) -> str:
    """Format recent iteration history for the planner prompt."""
    if not history:
        return "No previous iterations."

    recent = history[-max_entries:]
    lines: list[str] = []
    for entry in recent:
        it = entry.get("iteration", "?")
        cov = entry.get("coverage_percent", "?")
        decision = entry.get("decision", "?")
        rationale = entry.get("mutation_rationale", "")
        rules = entry.get("proposed_rules", [])
        line = f"- Iteration {it}: coverage={cov}%, decision={decision}"
        if rules:
            line += f", rules=[{', '.join(rules)}]"
        if rationale:
            line += f", rationale=\"{rationale[:100]}\""
        lines.append(line)

    return "\n".join(lines)


def response_text_formatter(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    return str(content)