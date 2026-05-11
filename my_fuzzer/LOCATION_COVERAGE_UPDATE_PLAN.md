# City And Format Coverage Update Plan

## Goal

Narrow the agentic fuzzer metric so it measures only one feature:

- `base URL + city name + format type`

Everything else is out of scope for the scored coverage:

- no IP-location coverage,
- no `~` special-place coverage,
- no `@domain` coverage,
- no moon coverage,
- no multi-location `:` coverage,
- no PNG option-suffix coverage beyond recognizing plain `png` as a format type,
- no extra query-flag coverage besides format selection.

The reporting model stays Markdown-first:

- one Markdown report per iteration,
- one Markdown report for the whole cycle,
- one Markdown coverage-diff report per iteration,
- one Markdown URL-diff report per iteration,
- a diff summary inside the cycle report.

## Scope Definition

The scored feature tuple is:

- `base_url`
- `city_name`
- `format_type`

### Base URL

The base URL is fixed by the current harness and protected grammar rules:

- `http://localhost:8002`

Because it is fixed, it is part of the normalized tuple for completeness, but it is not a varying dimension in practice.

### City Name

Only plain city-style location entries are scored.

Examples that should count:

- `/London`
- `/Moscow`
- `/Salt+Lake+City`
- `/Berlin?format=j1`
- `/Paris.png`

Examples that should not count:

- `/~Eiffel+Tower`
- `/@github.com`
- `/Moon`
- `/Moon@2016-12-25`
- `/London:Paris:Berlin`
- `/?format=j1`

### Format Type

Normalize all scored requests into one of these format types:

- `default`
- `j1`
- `j2`
- `v2`
- `v2n`
- `v2d`
- `p1`
- `png`

Normalization rules:

- `/Berlin` -> `default`
- `/Berlin?format=j1` -> `j1`
- `/Berlin?format=v2` -> `v2`
- `/Berlin.png` -> `png`
- `/Berlin?format=png` -> `png`

All other query flags should be ignored for the scored feature.

## Current State

### What the fuzzer does today

The current loop in `my_fuzzer/agent/orchestrator.py`:

- runs a baseline batch,
- optionally mutates the grammar,
- runs a candidate batch,
- compares line coverage only,
- writes mixed Markdown and JSON artifacts.

### What is missing

Today the fuzzer does not compute a focused feature-coverage score for:

- which city names were exercised,
- which format types were exercised for those cities,
- which `city + format` combinations were reached.

## Main Design Decision

Treat the new metric as **feature coverage**, not general location coverage.

Two signals should be reported side by side:

- `line coverage`
- `city-format feature coverage`

The feature coverage score is the percent of expected `city + format` combinations that were exercised by the run.

## Proposed Implementation

### 1. Replace The Broad Location Metric With A Focused Feature Metric

Create a new helper module:

- `my_fuzzer/agent/utils/feature_coverage.py`

Responsibilities:

- parse each generated URL,
- decide whether it belongs to the scored feature space,
- extract `city_name`,
- extract `format_type`,
- normalize the request into a canonical tuple:
  - `(base_url, city_name, format_type)`
- ignore everything outside that space.

Recommended per-request metadata:

- `feature_scored: bool`
- `base_url: str | None`
- `city_name: str | None`
- `format_type: str | None`
- `feature_key: str | None`
- `ignored_reason: str | None`

### 2. Define The Scored Denominator Explicitly

Add a checked-in catalog that defines the expected scored space:

- `my_fuzzer/agent/feature_coverage_catalog.py`

The catalog should declare:

- the allowed city list,
- the allowed format-type list,
- the generated Cartesian product of `city x format`,
- optional examples for reporting.

Recommended rule:

- the score should only use combinations from:
  - `scored_cities x scored_formats`

Recommended first source for cities:

- reuse the current grammar’s known city set from `my_fuzzer/url.g4`

Recommended first format set:

- `default`
- `j1`
- `j2`
- `v2`
- `v2n`
- `v2d`
- `p1`
- `png`

### 3. Ignore Everything Else Explicitly

Requests outside the scored feature space should still be logged, but not counted toward the feature score.

Recommended ignored groups:

- root-only requests
- moon routes
- special `~` routes
- `@domain` routes
- direct IP routes
- multi-location routes
- routes without a city
- routes with unsupported format values
- routes whose path shape is not `/<city>` plus optional recognized format encoding

This should be visible in reports under an “Ignored Requests” section, but not in the feature numerator or denominator.

### 4. Extend Request Result Records

Update `my_fuzzer/agent/models.py` and `my_fuzzer/agent/test_runner.py` so each executed request carries feature metadata.

Recommended additions to `TestResult`:

- `feature_scored: bool = False`
- `base_url: str | None = None`
- `city_name: str | None = None`
- `format_type: str | None = None`
- `feature_key: str | None = None`
- `ignored_reason: str | None = None`

Update `run_http_tests(...)` to:

- classify the URL before sending it,
- attach normalized feature metadata,
- preserve the current HTTP result fields.

### 5. Compute Per-Iteration Feature Coverage

During each batch run, compute a feature coverage summary next to the current line coverage summary.

Recommended summary fields:

- `feature_total`
- `feature_hit`
- `feature_coverage_percent`
- `hit_feature_keys`
- `missing_feature_keys`
- `city_counts`
- `format_counts`
- `successful_feature_keys`
- `crashing_feature_keys`
- `ignored_request_count`
- `ignored_request_reasons`

Recommended scoring rule:

- count a feature as hit if at least one request with that normalized tuple was executed,
- optionally also track `successful_feature_hit` separately, but keep the main score based on execution unless you want a stricter metric.

Recommended stricter alternative:

- report both:
  - `executed_feature_coverage_percent`
  - `successful_feature_coverage_percent`

That usually gives a better view than collapsing success and crash into one number.

### 6. Keep Grammar Mutations Focused On The Scored Feature

Update `my_fuzzer/url.g4` and planner guidance so mutations focus on generating more useful `city + format` combinations.

Grammar priorities:

- keep plain city paths healthy,
- keep `?format=...` generation healthy,
- keep `.png` generation healthy as the `png` format type,
- reduce emphasis on non-scored families.

Recommended de-emphasis:

- moon-heavy paths
- `~` special places
- `@domain`
- API-like invented prefixes
- unusual non-format query parameters unless they are needed for validity

### 7. Add Feature Coverage Diff Reports

Create Markdown diff reports that compare old and new coverage for the scored feature.

Recommended file pattern:

- `my_fuzzer/logs/reports/iteration_001_coverage_diff.md`

Recommended comparisons:

1. `previous_iteration_baseline -> current_iteration_baseline`
2. `current_iteration_baseline -> current_iteration_candidate`

Recommended sections:

- line coverage delta
- executed feature coverage delta
- successful feature coverage delta
- newly hit `city + format` keys
- lost `city + format` keys
- top cities added
- top formats added

### 8. Add URL Diff Reports Focused On The Scored Feature

Create Markdown URL-diff reports that compare generated URLs between iterations.

Recommended file pattern:

- `my_fuzzer/logs/reports/iteration_001_url_diff.md`

Recommended sections:

- new scored feature keys
- removed scored feature keys
- new concrete URL examples
- ignored URL examples
- repeated URL patterns dominating the batch
- normalization examples:
  - raw URL -> feature key

The URL diff should emphasize normalized `city + format` changes, not generic path novelty.

### 9. Replace The Report Content With Feature-Focused Markdown

Recommended report layout:

- `my_fuzzer/logs/reports/iteration_001_report.md`
- `my_fuzzer/logs/reports/iteration_001_coverage_diff.md`
- `my_fuzzer/logs/reports/iteration_001_url_diff.md`
- `my_fuzzer/logs/reports/cycle_report_<timestamp>.md`
- `my_fuzzer/logs/reports/latest_cycle_report.md`
- `my_fuzzer/logs/raw/...` for machine artifacts still needed internally

Each iteration report should include:

- baseline line coverage
- baseline feature coverage
- candidate line coverage if present
- candidate feature coverage if present
- new hit `city + format` combinations
- missing combinations
- ignored request summary
- links to the diff reports

### 10. Upgrade The Cycle Report

Refactor the cycle report writer in `my_fuzzer/agent/orchestrator.py` so the full-cycle report summarizes feature progress.

The cycle report should include:

- best line coverage reached
- best feature coverage reached
- per-iteration feature delta
- combinations first reached in each iteration
- combinations still missing at end of cycle
- compact diff summary

Recommended diff summary fields:

- line coverage trend
- executed feature coverage trend
- successful feature coverage trend
- newly reached `city + format` keys per iteration

### 11. Feed Feature Gaps Back Into The Planner

Extend the planner context so it sees:

- overrepresented cities
- overrepresented formats
- missing `city + format` pairs
- pairs that only crash
- pairs never generated

Prompt-level objective:

- improve line coverage,
- and increase coverage of missing `city + format` combinations,
- while ignoring non-scored URL families.

## Suggested File-Level Change List

- `my_fuzzer/agent/models.py`
  - add feature metadata fields to request results
- `my_fuzzer/agent/test_runner.py`
  - classify URLs into scored or ignored
  - compute feature summaries
- `my_fuzzer/agent/utils/feature_coverage.py`
  - new feature normalization and scoring logic
- `my_fuzzer/agent/feature_coverage_catalog.py`
  - scored city list, format list, and expected combinations
- `my_fuzzer/agent/utils/report_utils.py`
  - Markdown writers for iteration, coverage diff, URL diff, and cycle report
- `my_fuzzer/agent/utils/llm_utils.py`
  - format feature coverage data for planner prompts
- `my_fuzzer/agent/prompts/planner_agent.md`
  - mention missing `city + format` combinations
- `my_fuzzer/agent/orchestrator.py`
  - orchestrate feature snapshots, diffs, and cycle summaries
- `my_fuzzer/url.g4`
  - bias generation toward scored `city + format` paths

## Recommended Delivery Order

### Phase 1: Feature coverage model

- implement URL normalization to `base URL + city + format`
- implement the scored catalog
- annotate test results with feature metadata
- compute per-iteration feature coverage summaries

### Phase 2: Report refactor

- add Markdown iteration report writer
- add Markdown coverage diff writer
- add Markdown URL diff writer
- refactor the cycle report to include feature diff summaries

### Phase 3: Grammar and planner alignment

- update `url.g4`
- surface missing `city + format` pairs to the planner
- de-emphasize non-scored route families

### Phase 4: Validation

- run a short cycle
- verify that each iteration produces only Markdown human reports
- verify that ignored routes do not affect the feature score
- verify that the cycle report highlights only `city + format` progress

## Acceptance Criteria

The update is complete when all of the following are true:

1. Each iteration emits one main iteration Markdown report plus Markdown diff reports.
2. The full run emits one cycle Markdown report and one `latest` alias.
3. Every executed request is either normalized into `base URL + city + format` or marked ignored with a reason.
4. The reports show both line coverage and feature coverage.
5. The feature score only uses the defined `city + format` matrix.
6. IP, moon, special-place, domain, multi-location, and other non-scored routes do not affect the feature score.
7. Coverage diff reports show old vs new feature coverage in Markdown.
8. URL diff reports show differences in normalized `city + format` combinations in Markdown.
9. The cycle report contains a compact feature diff summary.

## Recommended First Implementation Slice

The safest first cut is:

1. implement feature normalization
2. compute feature coverage in `run_testing_batch(...)`
3. add iteration Markdown reporting
4. add feature coverage diff reporting
5. add URL diff reporting
6. update planner and grammar guidance

This keeps the change tightly focused on the one feature you want to measure.
