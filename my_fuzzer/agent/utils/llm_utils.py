import textwrap
from typing import Any
from pathlib import Path
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


def _resolve_source_path(file_name: str, config: FuzzerConfig) -> Path | None:
    candidate = Path(file_name)
    if candidate.is_absolute():
        return candidate if candidate.exists() else None

    repo_relative = config.repo_root / candidate
    if repo_relative.exists():
        return repo_relative
    return None


def _source_excerpt_for_line(path: Path, line_no: int, radius: int = 2) -> str | None:
    try:
        source_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None

    if line_no < 1 or line_no > len(source_lines):
        return None

    start = max(1, line_no - radius)
    end = min(len(source_lines), line_no + radius)
    excerpt: list[str] = []
    for idx in range(start, end + 1):
        marker = ">" if idx == line_no else " "
        line = source_lines[idx - 1].replace("\t", "    ")
        if len(line) > 160:
            line = line[:157] + "..."
        excerpt.append(f"{marker} {idx:>4}: {line}")
    return "\n".join(excerpt)


def _functions_for_missing_line(file_data: dict[str, Any], line_no: int) -> list[str]:
    functions = file_data.get("functions", {})
    if not isinstance(functions, dict):
        return []

    names: list[str] = []
    for name, function_data in functions.items():
        if not name or not isinstance(function_data, dict):
            continue
        if line_no in function_data.get("missing_lines", []):
            names.append(name)
    return names


def missing_line_context_formatter(
    coverage_data: dict[str, Any],
    config: FuzzerConfig,
    *,
    max_files: int = 3,
    max_lines_per_file: int = 3,
) -> str:
    """Format source excerpts for top missing lines so the planner can infer inputs."""
    files = coverage_data.get("files", {})
    if not files:
        return "No missing-line source context available."

    prioritized = sorted(
        files.items(),
        key=lambda item: len(item[1].get("missing_lines", [])),
        reverse=True,
    )

    file_limit = min(max_files, getattr(config, "max_missing_files", max_files))
    line_limit = min(max_lines_per_file, getattr(config, "max_missing_lines_per_file", max_lines_per_file))
    sections: list[str] = []

    for file_name, file_data in prioritized[:file_limit]:
        missing = file_data.get("missing_lines", [])
        if not missing:
            continue

        section_lines = [f"### {file_name}"]
        source_path = _resolve_source_path(file_name, config)
        if source_path is None:
            section_lines.append("Source file not available in the repo checkout.")
            sections.append("\n".join(section_lines))
            continue

        for line_no in missing[:line_limit]:
            function_names = _functions_for_missing_line(file_data, line_no)
            section_lines.append(f"Target line: {line_no}")
            if function_names:
                section_lines.append(f"Likely function: {', '.join(f'`{name}`' for name in function_names)}")
            excerpt = _source_excerpt_for_line(source_path, line_no)
            if excerpt is None:
                section_lines.append("Source excerpt unavailable for this line.")
                continue
            section_lines.append("```text")
            section_lines.append(excerpt)
            section_lines.append("```")

        sections.append("\n".join(section_lines))

    return "\n\n".join(sections) if sections else "No missing-line source context available."


def codebase_reachability_guide_formatter() -> str:
    """Return a static Python-coverage guide mapping request shapes to code regions."""
    return textwrap.dedent(
        """
        Only use this guide for Python-covered modules. Ignore non-Python files in the repo when reasoning about coverage because the collected coverage artifacts only track `bin/*.py` and `lib/*.py`.

        ### `bin/srv.py:47-69` Flask route entrypoints
        - Reach with: `/files/<path>`, `/favicon.ico`, `/malformed-response.html`, `/`, and `/<location>`.
        - Add to grammar: explicit static-file routes like `files/<segment>`, exact literals `favicon.ico` and `malformed-response.html`, root `/`, and single-segment location paths.
        - Coverage note: these routes are Python-covered and are the first branch point before `wttr_srv.wttr()` runs.

        ### `lib/wttr_srv.py:58-76` plain text page dispatch
        - Reach with: `/:help`, `/:bash.function`, `/:iterm2`, and `/:translation`.
        - Add to grammar: exact colon-prefixed literals for each static page.
        - Coverage note: these are fast-path Python branches and do not need weather lookup to be exercised.

        ### `lib/wttr_srv.py:79-167` client IP, language header, and host-based language/view parsing
        - Reach with: `X-PNG-Query-For`, `X-Forwarded-For`, `Accept-Language: fr-CA,fr;q=0.8`, and hosts like `fr.wttr.in`, `v2.wttr.in`, `v3.wttr.in`.
        - Add to grammar: none for the header-only parts; keep those in request profiles. For view/lang-by-host behavior, also keep it in request profiles because host values are not emitted by the URL grammar.
        - Coverage note: these branches are visible to Python coverage, but the right way to hit them is with header/host variation rather than new URL productions.

        ### `lib/wttr_srv.py:170-190` html vs text output selection
        - Reach with: plain-text UAs such as `curl`, `wget`, `python-requests`; browser-like UAs; `force-ansi`; non-v2/v3 view names; PNG filename requests.
        - Add to grammar: query flags and view literals that influence this branch, especially `A`, `format`/`view` values, and PNG path shapes.
        - Coverage note: pair grammar changes with UA profiles, because the same URL can go down different Python branches depending on the client type.

        ### `lib/wttr_srv.py:193-208` cyclic location selection
        - Reach with: colon-separated location strings not starting with `:`, for example `/Paris:Berlin:Rome?period=2`.
        - Add to grammar: multi-location path alternatives using literal `:` separators, plus `period=<int>`.
        - Coverage note: this is a good example of a Python-covered branch that generic single-city grammars will miss completely.

        ### `lib/wttr_srv.py:211-275` response routing for line, moon, weather, png, and follow-line branches
        - Reach with: oneline requests that set `view` via `format` or PNG filename metadata, moon routes like `/moon` and `/moon@2025-05-01`, normal weather locations like `/Cairo`, PNG outputs like `/Cairo.png`, and follow-line suppressors like `F`, `days=0`, `q`, `Q`, `T`, `d`.
        - Add to grammar: exact literals `moon`, `moon@<date>`, `.png`, `format`/`view` families (`j1`, `j2`, `p1`, `v2`, `v3`, custom placeholders), and short-flag bundles containing `F`, `q`, `Q`, `T`, `d`, `0`.
        - Coverage note: this block controls several important Python-covered branches, so the grammar should intentionally generate each family rather than rely on broad `STRING` tokens.

        ### `lib/wttr_srv.py:278-366` request parsing, serialized payloads, PNG filenames, and location processing
        - Reach with: serialized `b_<payload>` locations, `.png` filenames, colon-cycling locations, and locations that trigger `location_processing`.
        - Add to grammar: `b_`-prefixed payload shapes if the grammar can emit them safely, richer PNG filenames, and varied location prefixes like `~`, `@host`, IP strings, and `moon@...`.
        - Coverage note: this is a central Python parser stage; many downstream branches are only reachable if this stage produces the right `parsed_query` fields.

        ### `lib/wttr_srv.py:369-420` top-level request handling, rate limiting, and debug-friendly parsing path
        - Reach with: ordinary location requests, blocked locations, and explicit debug queries like `?debug=true`.
        - Add to grammar: concrete `debug=true` query support so the fuzzer can intentionally exercise the Python debug/request-handling branch when useful.
        - Coverage note: even when the fuzzer usually optimizes for normal responses, keeping `debug=true` reachable helps cover Python-only request wrapper logic.

        ### `lib/parse_query.py:35-127` query flag parsing and unit-selection logic
        - Reach with: bundled flags such as `A`, `d`, `n`, `m`, `M`, `u`, `I`, `t`, `T`, `p`, `q`, `Q`, `F`, and day digits `0`, `1`, `2`, `3`; valued params like `lang=fr`, `view=v2`, `format=%l:+%c`, `period=3`.
        - Add to grammar: exact single-letter flag bundles and concrete key=value pairs instead of arbitrary keys.
        - Coverage note: Python coverage here depends on generating the exact flag letters and specific values, especially combinations like `M` with metric wind or digit flags with `days`.

        ### `lib/parse_query.py:130-177` PNG filename parser
        - Reach with: names like `City_200x_lang=ru.png`, `City_x150.png`, `City_200x150_mq.png`, `City_t=90_u.png`.
        - Add to grammar: underscore-separated PNG tokens for width-only, height-only, width×height, `key=value`, and packed one-letter options before `.png`.
        - Coverage note: Python coverage treats PNG filenames as a separate parser surface from normal query strings, so the guide should mention both.

        ### `lib/location.py:91-102` and `lib/location.py:426-522` location normalization and resolution
        - Reach with: `~City`, `@hostname`, raw IP addresses, `moon@<suffix>`, unicode or symbol-heavy locations, and blocked / alias-prone locations.
        - Add to grammar: explicit `~` and `@` prefixes, `moon@...` variants, IPv4-like strings, plus locations containing `+` and `_` so normalization logic is exercised.
        - Coverage note: many Python-covered geolocation branches are controlled by location syntax, not by query flags.

        ### `lib/view/line.py:43-49` and `lib/view/line.py:457-501` preconfigured formats, JSON modes, Prometheus, v2, and custom placeholders
        - Reach with: `?format=1`, `?format=2`, `?format=3`, `?format=4`, `?format=69`, `?format=j1`, `?format=j2`, `?format=p1`, `?format=v2`, `?format=v2d`, `?format=v2n`, and custom placeholders like `%l`, `%c`, `%t`, `%w`, `%m`, `%M`, `%S`, `%s`, `%D`, `%d`, `%z`, `%T`, `%Z`.
        - Add to grammar: exact `format=` values for these named modes and literal placeholder-rich custom format strings.
        - Coverage note: this is one of the most valuable Python-covered surfaces because small syntax changes in `format` unlock very different renderers and post-processing paths.

        ### `lib/view/wttr.py:91-177` Wego wrapper and post-processing flags
        - Reach with: `use_ms_for_wind`, `narrow`, supported `lang`, `use_imperial`, `days=0/1/2`, `no-caption`, `no-terminal`, `no-city`, `dumb`, and `padding`.
        - Add to grammar: exact long keys or single-letter flags that populate those parsed query fields, especially `M`, `n`, `u`, `0`, `1`, `2`, `q`, `Q`, `T`, `d`, `p`.
        - Coverage note: this Python-covered code is a direct payoff from generating richer query flags.

        ### `lib/view/moon.py:14-64` moon rendering modifiers
        - Reach with: `/moon`, `/moon@2025-05-01`, `/moon@invalid-date`, `lang=<code>`, `T`, `d`, and html-producing user agents.
        - Add to grammar: `moon` and `moon@<date-like-string>` route families plus flags that trigger no-terminal and dumb output.
        - Coverage note: moon coverage is mostly driven by route shape rather than generic query fuzzing.

        ### `lib/fmt/png.py:70-257` PNG rendering options
        - Reach with: any `.png` request plus options like `background=000000`, `transparency=90`, and inverted-colors-related flags.
        - Add to grammar: `.png` route families and concrete `background=<6 hex>` / `transparency=<0..255>` parameters or PNG filename tokens.
        - Coverage note: the Python PNG formatter has its own branches for color decoding and transparency clamping, so concrete numeric and hex values matter.
        """
    ).strip()


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
