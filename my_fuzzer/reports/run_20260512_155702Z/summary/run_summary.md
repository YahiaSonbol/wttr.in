# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | completed |
| Started At | 2026-05-12T15:57:02Z |
| Finished At | 2026-05-12T16:32:24Z |
| Duration Seconds | 2122.45 |
| Configured Iterations | 10 |
| Completed Iterations | 10 |
| Tests Per Batch | 50 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 54.55% |
| Aggregate Coverage | 58.05% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 8418 |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 50 | 53.34% | 11 | 11 | 28 | 0 | 1 | regression | 53.18% | kept_champion |
| 2 | 50 | 53.61% | 14 | 10 | 26 | 0 | 1 | regression | 51.20% | kept_champion |
| 3 | 50 | 52.74% | 6 | 3 | 41 | 0 | 1 | regression | 51.86% | kept_champion |
| 4 | 50 | 51.70% | 18 | 9 | 23 | 0 | 1 | regression | 48.47% | kept_champion |
| 5 | 50 | 52.52% | 8 | 6 | 36 | 0 | 1 | regression | 53.40% | kept_champion |
| 6 | 50 | 52.46% | 6 | 4 | 40 | 0 | 1 | regression | 52.85% | kept_champion |
| 7 | 50 | 50.77% | 3 | 3 | 44 | 0 | 1 | regression | 48.30% | kept_champion |
| 8 | 50 | 53.67% | 10 | 4 | 36 | 0 | 1 | regression | 52.41% | kept_champion |
| 9 | 50 | 53.78% | 15 | 9 | 26 | 0 | 1 | regression | 51.92% | kept_champion |
| 10 | 50 | 54.55% | 11 | 4 | 35 | 0 | 0 | skipped_final_iteration | - | kept_champion |
## Aggregate Coverage

- Coverage across all included iterations: 58.05%
- Covered lines: 1060
- Missing lines: 766
- Executable lines: 1826
- Included coverage artifacts: 19
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 50
- Baseline coverage: 53.34%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.18%
- Candidate delta vs champion: -0.16
- Mutation rationale: Add missing format options, imperial flag, colon API routes, and strict PNG size/lang pattern per planner guidance
- Proposed rules: searchparameter, query, uri
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many 503/404 responses and few successful 200s, with crashes concentrated on PNG and colon‑prefixed routes. Coverage gaps are spread across view, location and PNG rendering modules, many of which are gated by specific query keys, format values, language suffixes, and host‑ba...
- Reachable by grammar: 5 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 50
- Baseline coverage: 53.61%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.20%
- Candidate delta vs champion: -2.41
- Mutation rationale: Add explicit use_imperial and full lang enums, enforce size+lang PNG routes, and allow mixed flag/value chains after language suffix.
- Proposed rules: searchparameter, uri, search
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 503/500 errors, with a heavy bias toward colon‑prefixed API routes and generic city/format queries. PNG routes and moon‑related endpoints are still under‑exercised, and several code paths that depend on specific query keys (use_imperial, lang, format variant...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 6 items
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)
- Baseline coverage JSON: [iteration_002_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_coverage.json)
- Candidate results: [iteration_002_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_results.json)
- Candidate coverage JSON: [iteration_002_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_coverage.json)
- Baseline grammar diff: [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_002_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_002_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_002_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_002_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_002_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_002_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_002_llm_attempt_01_planner_prompt.md, iteration_002_llm_attempt_01_planner_output.json, iteration_002_llm_attempt_01_rewriter_prompt.md, iteration_002_llm_attempt_01_rewriter_output.json, iteration_002_llm_attempt_01_trace.json

### Iteration 3

- Tests run: 50
- Baseline coverage: 52.74%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.86%
- Candidate delta vs champion: -1.75
- Mutation rationale: Add needed query keys, expand colon‑API routes, and loosen language suffix handling to hit uncovered code paths.
- Proposed rules: searchparameter, query, LANG_SUFFIX
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes (41) and few successes (6). Most responses are 500/503 errors coming from a wide variety of path prefixes, while successful 200s are limited to simple default routes and basic format queries. Coverage gaps are concentrated in view rendering, location handling, P...
- Reachable by grammar: 5 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_003_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_results.json)
- Baseline coverage JSON: [iteration_003_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_coverage.json)
- Candidate results: [iteration_003_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_results.json)
- Candidate coverage JSON: [iteration_003_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_coverage.json)
- Baseline grammar diff: [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_003_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_003_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_003_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_003_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_003_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_003_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_003_llm_attempt_01_planner_prompt.md, iteration_003_llm_attempt_01_planner_output.json, iteration_003_llm_attempt_01_rewriter_prompt.md, iteration_003_llm_attempt_01_rewriter_output.json, iteration_003_llm_attempt_01_trace.json

### Iteration 4

- Tests run: 50
- Baseline coverage: 51.70%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 48.47%
- Candidate delta vs champion: -5.15
- Mutation rationale: Add explicit use_imperial and v2 formats, constrain language suffix, and enable PNG size/lang routes with optional query strings
- Proposed rules: LANG_SUFFIX, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The fuzzer is generating many moon‑related and colon‑prefixed routes, but most responses are 503/500 errors and only a few 200s from generic city paths. Coverage gaps are concentrated in utility functions (encoding, imperial flag handling, location debug, PNG rendering, and server routing) that a...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 6 items
- Baseline results: [iteration_004_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_results.json)
- Baseline coverage JSON: [iteration_004_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_coverage.json)
- Candidate results: [iteration_004_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_results.json)
- Candidate coverage JSON: [iteration_004_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_coverage.json)
- Baseline grammar diff: [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_004_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_004_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_004_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_004_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_004_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_004_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_004_llm_attempt_01_planner_prompt.md, iteration_004_llm_attempt_01_planner_output.json, iteration_004_llm_attempt_01_rewriter_prompt.md, iteration_004_llm_attempt_01_rewriter_output.json, iteration_004_llm_attempt_01_trace.json

### Iteration 5

- Tests run: 50
- Baseline coverage: 52.52%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.40%
- Candidate delta vs champion: -0.22
- Mutation rationale: Add use_imperial flag, full format set, tighten LANG_SUFFIX, and expand colon‑prefixed API routes for richer coverage
- Proposed rules: searchparameter, LANG_SUFFIX, query
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The fuzzer is heavily hitting error paths (500/503) and only a few successful routes, most of which are simple city lookups or colon‑prefixed help routes. PNG and moon related routes are causing many failures, indicating they are under‑tested. Coverage gaps are concentrated in utility functions (...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_005_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_results.json)
- Baseline coverage JSON: [iteration_005_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_coverage.json)
- Candidate results: [iteration_005_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_results.json)
- Candidate coverage JSON: [iteration_005_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_coverage.json)
- Baseline grammar diff: [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_005_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_005_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_005_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_005_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_005_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_005_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_005_llm_attempt_01_planner_prompt.md, iteration_005_llm_attempt_01_planner_output.json, iteration_005_llm_attempt_01_rewriter_prompt.md, iteration_005_llm_attempt_01_rewriter_output.json, iteration_005_llm_attempt_01_trace.json

### Iteration 6

- Tests run: 50
- Baseline coverage: 52.46%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 52.85%
- Candidate delta vs champion: -0.77
- Mutation rationale: Add missing keys, flag‑only handling, explicit PNG size/lang syntax and broaden language suffix to hit uncovered code paths
- Proposed rules: searchparameter, LANG_SUFFIX, query
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) and only a handful of successful 200 responses, most of which came from the generic city or PNG routes. The response distribution is heavily skewed toward server errors, indicating that the grammar is still generating many malformed or unsupported requ...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Line target hints: 6 items
- Baseline results: [iteration_006_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_results.json)
- Baseline coverage JSON: [iteration_006_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_coverage.json)
- Candidate results: [iteration_006_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_results.json)
- Candidate coverage JSON: [iteration_006_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_coverage.json)
- Baseline grammar diff: [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_006_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_006_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_006_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_006_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_006_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_006_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_006_llm_attempt_01_planner_prompt.md, iteration_006_llm_attempt_01_planner_output.json, iteration_006_llm_attempt_01_rewriter_prompt.md, iteration_006_llm_attempt_01_rewriter_output.json, iteration_006_llm_attempt_01_trace.json

### Iteration 7

- Tests run: 50
- Baseline coverage: 50.77%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 48.30%
- Candidate delta vs champion: -5.31
- Mutation rationale: Add missing use_imperial key, concrete language suffixes, and broaden flag handling to hit uncovered code paths
- Proposed rules: searchparameter, LANG_SUFFIX
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes (44) and few successes (3). Most responses are 500/503 errors from a narrow set of paths (colon‑prefixed routes, moon PNGs, generic city lookups). Successful 200s came from simple moon or format queries. Coverage is stuck around 52% and many hot‑spot lines remai...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Line target hints: 6 items
- Baseline results: [iteration_007_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_results.json)
- Baseline coverage JSON: [iteration_007_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_coverage.json)
- Candidate results: [iteration_007_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_results.json)
- Candidate coverage JSON: [iteration_007_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_coverage.json)
- Baseline grammar diff: [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_007_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_007_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_007_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_007_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_007_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_007_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_007_llm_attempt_01_planner_prompt.md, iteration_007_llm_attempt_01_planner_output.json, iteration_007_llm_attempt_01_rewriter_prompt.md, iteration_007_llm_attempt_01_rewriter_output.json, iteration_007_llm_attempt_01_trace.json

### Iteration 8

- Tests run: 50
- Baseline coverage: 53.67%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 52.41%
- Candidate delta vs champion: -1.26
- Mutation rationale: Add use_imperial, flag‑only tokens, concrete language suffixes, and explicit query alternatives to hit uncovered code paths.
- Proposed rules: searchparameter, query, LANG_SUFFIX
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes and few successes, with most requests hitting generic city/moon routes and flag‑only query strings. Coverage is stuck around 52% and many missing lines are in view rendering, PNG generation, query parsing and location handling. Over‑represented responses are 500...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_008_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_results.json)
- Baseline coverage JSON: [iteration_008_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_coverage.json)
- Candidate results: [iteration_008_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_results.json)
- Candidate coverage JSON: [iteration_008_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_coverage.json)
- Baseline grammar diff: [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_008_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_008_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_008_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_008_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_008_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_008_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_008_llm_attempt_01_planner_prompt.md, iteration_008_llm_attempt_01_planner_output.json, iteration_008_llm_attempt_01_rewriter_prompt.md, iteration_008_llm_attempt_01_rewriter_output.json, iteration_008_llm_attempt_01_trace.json

### Iteration 9

- Tests run: 50
- Baseline coverage: 53.78%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.92%
- Candidate delta vs champion: -1.86
- Mutation rationale: Add use_imperial flag, broaden language suffix handling, and expose full colon‑prefixed API routes with query strings to hit uncovered view/line, view/v2, fmt/png and PNG size/lang logic.
- Proposed rules: searchparameter, LANG_SUFFIX, query
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and a high proportion of 500/503 responses, but most successful 200s came from very generic paths (plain city names, simple format queries, and the ':' help routes). PNG and moon related routes are still under‑tested, and several internal flags (use_imperial, la...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_009_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_results.json)
- Baseline coverage JSON: [iteration_009_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_coverage.json)
- Candidate results: [iteration_009_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_results.json)
- Candidate coverage JSON: [iteration_009_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_coverage.json)
- Baseline grammar diff: [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_009_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_009_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_009_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_009_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_009_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_009_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_009_llm_attempt_01_planner_prompt.md, iteration_009_llm_attempt_01_planner_output.json, iteration_009_llm_attempt_01_rewriter_prompt.md, iteration_009_llm_attempt_01_rewriter_output.json, iteration_009_llm_attempt_01_trace.json

### Iteration 10

- Tests run: 50
- Baseline coverage: 54.55%
- Container exit code: 0
- Mutation status: skipped_final_iteration
- Decision: kept_champion
- Baseline results: [iteration_010_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_results.json)
- Baseline coverage JSON: [iteration_010_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_coverage.json)
- Baseline grammar diff: [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/grammar/iteration_010_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/coverage/iteration_010_baseline_vs_latest_saved_baseline.md)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_155702Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_155702Z/summary/cycle_aggregate_coverage.md)
