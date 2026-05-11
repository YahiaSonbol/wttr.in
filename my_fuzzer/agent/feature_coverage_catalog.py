from __future__ import annotations

SCORED_CITIES: tuple[str, ...] = (
    "bangkok",
    "beijing",
    "berlin",
    "cairo",
    "delhi",
    "dubai",
    "hongkong",
    "istanbul",
    "london",
    "madrid",
    "moscow",
    "newyork",
    "paris",
    "riyadh",
    "rome",
    "seoul",
    "singapore",
    "sydney",
    "tokyo",
    "toronto",
)

SCORED_FORMATS: tuple[str, ...] = (
    "default",
    "j1",
    "j2",
    "v2",
    "v2n",
    "v2d",
    "p1",
    "png",
)


def build_feature_key(base_url: str, city_name: str, format_type: str) -> str:
    return f"{base_url}|{city_name}|{format_type}"


def expected_feature_keys(base_url: str) -> set[str]:
    return {
        build_feature_key(base_url, city_name, format_type)
        for city_name in SCORED_CITIES
        for format_type in SCORED_FORMATS
    }
