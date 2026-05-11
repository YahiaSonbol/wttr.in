from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit
import re

from ..feature_coverage_catalog import (
    SCORED_CITIES,
    SCORED_FORMATS,
    build_feature_key,
    expected_feature_keys,
)
from ..models import TestResult


SCORED_CITY_SET = frozenset(SCORED_CITIES)
SCORED_FORMAT_SET = frozenset(SCORED_FORMATS)
FORMAT_QUERY_KEY = "format"
CITY_PATH_RE = re.compile(r"^[a-z0-9+.-]+$", re.IGNORECASE)


def normalize_city_name(raw_city: str) -> str:
    city = unquote(raw_city).strip().lower()
    city = city.replace("+", " ")
    city = re.sub(r"\s+", " ", city)
    return city


def normalize_feature_url(url: str, base_url: str) -> dict[str, Any]:
    result = {
        "feature_scored": False,
        "base_url": None,
        "city_name": None,
        "format_type": None,
        "feature_key": None,
        "ignored_reason": None,
    }

    if not url:
        result["ignored_reason"] = "empty_url"
        return result

    parsed = urlsplit(url)
    actual_base_url = ""
    if parsed.scheme and parsed.netloc:
        actual_base_url = f"{parsed.scheme}://{parsed.netloc}"
    result["base_url"] = actual_base_url or None

    if actual_base_url != base_url:
        result["ignored_reason"] = "unsupported_base_url"
        return result

    path = unquote(parsed.path or "").strip("/")
    if not path:
        result["ignored_reason"] = "root_only"
        return result
    if "/" in path:
        result["ignored_reason"] = "multi_path_segments"
        return result

    lowered = path.lower()
    if lowered.startswith("~"):
        result["ignored_reason"] = "special_lookup"
        return result
    if "@" in lowered:
        result["ignored_reason"] = "domain_or_moon_lookup"
        return result
    if ":" in lowered:
        result["ignored_reason"] = "multi_location_or_prefixed_route"
        return result
    if lowered.startswith(":"):
        result["ignored_reason"] = "special_route"
        return result

    query = parse_qs(parsed.query, keep_blank_values=True)

    format_type = "default"
    path_city = lowered
    if lowered.endswith(".png"):
        path_city = lowered[:-4]
        if "_" in path_city:
            result["ignored_reason"] = "png_option_suffix"
            return result
        format_type = "png"
    else:
        values = query.get(FORMAT_QUERY_KEY, [])
        if values:
            format_candidate = str(values[0]).strip().lower()
            if format_candidate not in SCORED_FORMAT_SET:
                result["ignored_reason"] = "unsupported_format"
                return result
            format_type = format_candidate

    if not CITY_PATH_RE.fullmatch(path_city):
        result["ignored_reason"] = "unsupported_city_shape"
        return result

    city_name = normalize_city_name(path_city)
    if not city_name:
        result["ignored_reason"] = "missing_city"
        return result
    if city_name == "moon":
        result["ignored_reason"] = "moon_route"
        return result
    if city_name not in SCORED_CITY_SET:
        result["ignored_reason"] = "unsupported_city"
        return result

    result["feature_scored"] = True
    result["city_name"] = city_name
    result["format_type"] = format_type
    result["feature_key"] = build_feature_key(base_url, city_name, format_type)
    result["ignored_reason"] = None
    return result


def summarize_feature_coverage(
    results: list[TestResult],
    base_url: str,
) -> dict[str, Any]:
    expected_keys = expected_feature_keys(base_url)
    hit_keys = {
        result.feature_key
        for result in results
        if result.feature_scored and result.feature_key
    }
    successful_keys = {
        result.feature_key
        for result in results
        if result.feature_scored and result.feature_key and result.status == "SUCCESS"
    }
    crashing_keys = {
        result.feature_key
        for result in results
        if result.feature_scored and result.feature_key and result.status in {"CRASH", "ERROR"}
    }

    city_counts = Counter(
        result.city_name
        for result in results
        if result.feature_scored and result.city_name
    )
    format_counts = Counter(
        result.format_type
        for result in results
        if result.feature_scored and result.format_type
    )
    ignored_reasons = Counter(
        result.ignored_reason
        for result in results
        if not result.feature_scored and result.ignored_reason
    )

    feature_examples: dict[str, str] = {}
    for result in results:
        if result.feature_scored and result.feature_key and result.feature_key not in feature_examples:
            feature_examples[result.feature_key] = result.url

    total = len(expected_keys)
    hit = len(hit_keys)
    successful_hit = len(successful_keys)

    return {
        "base_url": base_url,
        "scored_cities": list(SCORED_CITIES),
        "scored_formats": list(SCORED_FORMATS),
        "feature_total": total,
        "feature_hit": hit,
        "feature_coverage_percent": round((hit / total) * 100.0, 2) if total else 0.0,
        "successful_feature_hit": successful_hit,
        "successful_feature_coverage_percent": round((successful_hit / total) * 100.0, 2) if total else 0.0,
        "hit_feature_keys": sorted(hit_keys),
        "missing_feature_keys": sorted(expected_keys - hit_keys),
        "successful_feature_keys": sorted(successful_keys),
        "crashing_feature_keys": sorted(crashing_keys),
        "city_counts": dict(sorted(city_counts.items())),
        "format_counts": dict(sorted(format_counts.items())),
        "ignored_request_count": sum(ignored_reasons.values()),
        "ignored_request_reasons": dict(sorted(ignored_reasons.items())),
        "feature_examples": feature_examples,
    }


def merge_feature_summaries(
    summaries: list[dict[str, Any] | None],
    base_url: str,
) -> dict[str, Any]:
    expected_keys = expected_feature_keys(base_url)
    hit_keys: set[str] = set()
    successful_keys: set[str] = set()
    crashing_keys: set[str] = set()
    city_counts: Counter[str] = Counter()
    format_counts: Counter[str] = Counter()
    ignored_reasons: Counter[str] = Counter()
    feature_examples: dict[str, str] = {}

    for summary in summaries:
        if not summary:
            continue
        hit_keys.update(summary.get("hit_feature_keys", []))
        successful_keys.update(summary.get("successful_feature_keys", []))
        crashing_keys.update(summary.get("crashing_feature_keys", []))
        city_counts.update(summary.get("city_counts", {}))
        format_counts.update(summary.get("format_counts", {}))
        ignored_reasons.update(summary.get("ignored_request_reasons", {}))
        for feature_key, url in summary.get("feature_examples", {}).items():
            feature_examples.setdefault(feature_key, url)

    total = len(expected_keys)
    hit = len(hit_keys)
    successful_hit = len(successful_keys)

    return {
        "base_url": base_url,
        "scored_cities": list(SCORED_CITIES),
        "scored_formats": list(SCORED_FORMATS),
        "feature_total": total,
        "feature_hit": hit,
        "feature_coverage_percent": round((hit / total) * 100.0, 2) if total else 0.0,
        "successful_feature_hit": successful_hit,
        "successful_feature_coverage_percent": round((successful_hit / total) * 100.0, 2) if total else 0.0,
        "hit_feature_keys": sorted(hit_keys),
        "missing_feature_keys": sorted(expected_keys - hit_keys),
        "successful_feature_keys": sorted(successful_keys),
        "crashing_feature_keys": sorted(crashing_keys),
        "city_counts": dict(sorted(city_counts.items())),
        "format_counts": dict(sorted(format_counts.items())),
        "ignored_request_count": sum(ignored_reasons.values()),
        "ignored_request_reasons": dict(sorted(ignored_reasons.items())),
        "feature_examples": feature_examples,
    }


def feature_delta(old_summary: dict[str, Any] | None, new_summary: dict[str, Any]) -> dict[str, Any]:
    old_hit = set((old_summary or {}).get("hit_feature_keys", []))
    new_hit = set(new_summary.get("hit_feature_keys", []))
    old_success = set((old_summary or {}).get("successful_feature_keys", []))
    new_success = set(new_summary.get("successful_feature_keys", []))

    return {
        "new_hit_feature_keys": sorted(new_hit - old_hit),
        "lost_hit_feature_keys": sorted(old_hit - new_hit),
        "new_successful_feature_keys": sorted(new_success - old_success),
        "lost_successful_feature_keys": sorted(old_success - new_success),
        "feature_coverage_delta": round(
            float(new_summary.get("feature_coverage_percent", 0.0))
            - float((old_summary or {}).get("feature_coverage_percent", 0.0)),
            2,
        ),
        "successful_feature_coverage_delta": round(
            float(new_summary.get("successful_feature_coverage_percent", 0.0))
            - float((old_summary or {}).get("successful_feature_coverage_percent", 0.0)),
            2,
        ),
    }


def compact_feature_label(feature_key: str) -> str:
    _, city_name, format_type = feature_key.split("|", 2)
    return f"{city_name}[{format_type}]"


def feature_summary_formatter(summary: dict[str, Any]) -> str:
    if not summary:
        return "No city-format feature coverage was recorded."

    lines = [
        f"Executed city+format coverage: {summary.get('feature_hit', 0)}/{summary.get('feature_total', 0)} "
        f"({summary.get('feature_coverage_percent', 0.0):.2f}%)",
        f"Successful city+format coverage: {summary.get('successful_feature_hit', 0)}/{summary.get('feature_total', 0)} "
        f"({summary.get('successful_feature_coverage_percent', 0.0):.2f}%)",
    ]

    city_counts = summary.get("city_counts", {})
    if city_counts:
        top_cities = ", ".join(f"{city}×{count}" for city, count in list(city_counts.items())[:8])
        lines.append(f"Cities exercised: {top_cities}")

    format_counts = summary.get("format_counts", {})
    if format_counts:
        top_formats = ", ".join(f"{fmt}×{count}" for fmt, count in format_counts.items())
        lines.append(f"Formats exercised: {top_formats}")

    missing = summary.get("missing_feature_keys", [])[:8]
    if missing:
        lines.append("Missing combinations: " + ", ".join(compact_feature_label(key) for key in missing))

    ignored = summary.get("ignored_request_reasons", {})
    if ignored:
        ignored_text = ", ".join(f"{reason}×{count}" for reason, count in ignored.items())
        lines.append(f"Ignored requests: {ignored_text}")

    return "\n".join(lines)


def serialize_results(results: list[TestResult]) -> list[dict[str, Any]]:
    return [asdict(result) for result in results]
