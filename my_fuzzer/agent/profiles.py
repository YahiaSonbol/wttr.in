"""Reusable request-header profiles for expanded fuzzing.

Each profile category contains named presets. The planner can recommend
specific profile names, or the runner can pick randomly.
"""

from __future__ import annotations

import random
from typing import Any


# ---------------------------------------------------------------------------
# Host profiles — sent as ``Host:`` header while connecting to localhost
# ---------------------------------------------------------------------------

HOST_PROFILES: dict[str, str] = {
    "wttr.in": "wttr.in",
    "de.wttr.in": "de.wttr.in",
    "fr.wttr.in": "fr.wttr.in",
    "ru.wttr.in": "ru.wttr.in",
    "zh.wttr.in": "zh.wttr.in",
    "ja.wttr.in": "ja.wttr.in",
    "es.wttr.in": "es.wttr.in",
    "ar.wttr.in": "ar.wttr.in",
    "ko.wttr.in": "ko.wttr.in",
    "v2.wttr.in": "v2.wttr.in",
    "v3.wttr.in": "v3.wttr.in",
    "localhost": "localhost",
}


# ---------------------------------------------------------------------------
# User-Agent profiles
# ---------------------------------------------------------------------------

USER_AGENT_PROFILES: dict[str, str] = {
    "curl": "curl/8.0.1",
    "wget": "Wget/1.21",
    "browser_chrome": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "browser_firefox": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
    ),
    "terminal_httpie": "HTTPie/3.2.2",
    "terminal_fetch": "Go-http-client/2.0",
    "image_fetcher": "Googlebot-Image/1.0",
    "empty": "",
}


# ---------------------------------------------------------------------------
# Accept-Language profiles
# ---------------------------------------------------------------------------

ACCEPT_LANGUAGE_PROFILES: dict[str, str] = {
    "english": "en-US,en;q=0.9",
    "german": "de-DE,de;q=0.9,en;q=0.5",
    "russian": "ru-RU,ru;q=0.9,en;q=0.3",
    "chinese": "zh-CN,zh;q=0.9,en;q=0.5",
    "japanese": "ja-JP,ja;q=0.9,en;q=0.3",
    "arabic": "ar-SA,ar;q=0.9,en;q=0.5",
    "french": "fr-FR,fr;q=0.9,en;q=0.3",
    "spanish": "es-ES,es;q=0.9,en;q=0.5",
    "korean": "ko-KR,ko;q=0.9,en;q=0.3",
    "multi_weighted": "de-DE,de;q=0.9,fr;q=0.7,en;q=0.5,ja;q=0.3",
    "unsupported_fallback": "xx-XX,en;q=0.1",
    "malformed": ";;;q=abc,,",
}


# ---------------------------------------------------------------------------
# IP persona profiles — sent as X-Forwarded-For / X-Real-IP
# ---------------------------------------------------------------------------

IP_PERSONA_PROFILES: dict[str, dict[str, str]] = {
    "us_public": {
        "X-Forwarded-For": "8.8.8.8",
        "X-Real-IP": "8.8.8.8",
    },
    "de_public": {
        "X-Forwarded-For": "85.214.132.117",
        "X-Real-IP": "85.214.132.117",
    },
    "jp_public": {
        "X-Forwarded-For": "202.12.27.33",
        "X-Real-IP": "202.12.27.33",
    },
    "ru_public": {
        "X-Forwarded-For": "77.88.55.66",
        "X-Real-IP": "77.88.55.66",
    },
    "br_public": {
        "X-Forwarded-For": "200.160.2.3",
        "X-Real-IP": "200.160.2.3",
    },
    "localhost": {
        "X-Forwarded-For": "127.0.0.1",
        "X-Real-IP": "127.0.0.1",
    },
    "private_network": {
        "X-Forwarded-For": "10.0.0.42",
        "X-Real-IP": "192.168.1.100",
    },
    "multi_hop_proxy": {
        "X-Forwarded-For": "203.0.113.50, 198.51.100.178, 192.0.2.1",
        "X-Real-IP": "203.0.113.50",
    },
    "malformed_chain": {
        "X-Forwarded-For": "not-an-ip, 999.999.999.999, ::1",
        "X-Real-IP": "garbage",
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_header_set(
    *,
    host: str | None = None,
    ua: str | None = None,
    lang: str | None = None,
    ip_profile: str | None = None,
) -> dict[str, str]:
    """Build a header dict from named profile values."""
    headers: dict[str, str] = {}
    if host is not None:
        headers["Host"] = HOST_PROFILES.get(host, host)
    if ua is not None:
        headers["User-Agent"] = USER_AGENT_PROFILES.get(ua, ua)
    if lang is not None:
        headers["Accept-Language"] = ACCEPT_LANGUAGE_PROFILES.get(lang, lang)
    if ip_profile is not None:
        ip_data = IP_PERSONA_PROFILES.get(ip_profile, {})
        headers.update(ip_data)
    return headers


def random_profile_set() -> dict[str, str]:
    """Return a randomly assembled header set."""
    return build_header_set(
        host=random.choice(list(HOST_PROFILES)),
        ua=random.choice(list(USER_AGENT_PROFILES)),
        lang=random.choice(list(ACCEPT_LANGUAGE_PROFILES)),
        ip_profile=random.choice(list(IP_PERSONA_PROFILES)),
    )


def profile_names_summary() -> dict[str, list[str]]:
    """Return profile category names for embedding in the planner prompt."""
    return {
        "host_profiles": list(HOST_PROFILES.keys()),
        "ua_profiles": list(USER_AGENT_PROFILES.keys()),
        "accept_language_profiles": list(ACCEPT_LANGUAGE_PROFILES.keys()),
        "ip_profiles": list(IP_PERSONA_PROFILES.keys()),
    }


def resolve_profiles(recommendations: dict[str, list[str]] | None) -> list[dict[str, str]]:
    """Turn planner profile recommendations into concrete header sets.

    Returns a list of header dicts. If no recommendations, returns a small
    set of random profiles.
    """
    if not recommendations:
        return [random_profile_set() for _ in range(3)]

    header_sets: list[dict[str, str]] = []
    hosts = recommendations.get("host_profiles", [])
    uas = recommendations.get("ua_profiles", [])
    langs = recommendations.get("language_profiles", [])
    ips = recommendations.get("ip_profiles", [])

    # Build cross-product of recommended profiles (bounded)
    max_combos = 6
    count = 0
    for h in (hosts or [None]):
        for u in (uas or [None]):
            for l in (langs or [None]):
                for i in (ips or [None]):
                    if count >= max_combos:
                        break
                    header_sets.append(build_header_set(host=h, ua=u, lang=l, ip_profile=i))
                    count += 1

    if not header_sets:
        header_sets = [random_profile_set() for _ in range(3)]

    return header_sets
