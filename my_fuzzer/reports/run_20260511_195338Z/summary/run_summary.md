# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | completed |
| Started At | 2026-05-11T19:53:38Z |
| Finished At | 2026-05-11T20:22:40Z |
| Duration Seconds | 1742.08 |
| Configured Iterations | 10 |
| Completed Iterations | 10 |
| Tests Per Batch | 50 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 55.86% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 8403 |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 50 | 51.42% | 11 | 0 | 39 | 0 | 1 | regression | 51.31% | kept_champion |
| 2 | 50 | 53.29% | 31 | 0 | 19 | 0 | 1 | accepted | 54.00% | promoted_to_champion |
| 3 | 50 | 52.85% | 12 | 1 | 37 | 0 | 1 | regression | 51.59% | kept_champion |
| 4 | 50 | 52.96% | 12 | 1 | 37 | 0 | 1 | regression | 53.45% | kept_champion |
| 5 | 50 | 46.82% | 24 | 3 | 23 | 0 | 1 | regression | 52.30% | kept_champion |
| 6 | 50 | 51.86% | 10 | 0 | 40 | 0 | 2 | regression | 53.94% | kept_champion |
| 7 | 50 | 48.85% | 13 | 0 | 37 | 0 | 3 | accepted | 54.00% | promoted_to_champion |
| 8 | 50 | 50.11% | 17 | 1 | 32 | 0 | 1 | accepted | 54.27% | promoted_to_champion |
| 9 | 50 | 55.86% | 21 | 0 | 29 | 0 | 1 | regression | 50.55% | kept_champion |
| 10 | 50 | 51.15% | 12 | 0 | 38 | 0 | 0 | skipped_final_iteration | - | kept_champion |

## Iteration Details

### Iteration 1

- Tests run: 50
- Baseline coverage: 51.42%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.31%
- Candidate delta vs champion: -0.11
- Mutation rationale: Add size/language suffixes, mixed flag/key-value parameters, and colon‑prefixed routes with optional trailing slash and query to hit under‑explored code paths.
- Proposed rules: CITY, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) but only a handful of successful 200 responses, most of which came from generic special routes (/:iterm2, /:bash.function) and simple moon/format queries. Coverage is still low and many core modules (view, png, location, parse_query) have large untouch...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (no_previous_baseline): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 50
- Baseline coverage: 53.29%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 54.00%
- Candidate delta vs champion: +0.71
- Mutation rationale: Add flag‑chain mixing, HEX keys/values, richer PNG suffixes, and query strings for colon‑prefixed routes to hit under‑explored code paths.
- Proposed rules: searchparameter, CITY, query
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many 503 responses from a narrow set of paths (moon, PNG, and colon‑prefixed routes) while successful 200s came mostly from simple city lookups and format=png queries. Coverage gaps are concentrated in view rendering (v2, line), location parsing, PNG generation and query par...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)
- Baseline coverage JSON: [iteration_002_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_coverage.json)
- Candidate results: [iteration_002_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_results.json)
- Candidate coverage JSON: [iteration_002_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_coverage.json)
- Baseline grammar diff: [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_002_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_002_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_002_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_002_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_002_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_002_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_002_llm_attempt_01_planner_prompt.md, iteration_002_llm_attempt_01_planner_output.json, iteration_002_llm_attempt_01_rewriter_prompt.md, iteration_002_llm_attempt_01_rewriter_output.json, iteration_002_llm_attempt_01_trace.json

### Iteration 3

- Tests run: 50
- Baseline coverage: 52.85%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.59%
- Candidate delta vs champion: -2.41
- Mutation rationale: Add mixed flag/key-value support, colon‑prefixed API routes, and PNG size/language suffixes to broaden coverage
- Proposed rules: searchparameter, query, CITY
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) and few successes, with most requests hitting generic city or moon routes. Header diversity is low (mostly default Host), and PNG/format queries dominate the failures. Coverage gaps are in view rendering, location parsing, PNG generation and query pars...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Baseline results: [iteration_003_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_results.json)
- Baseline coverage JSON: [iteration_003_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_coverage.json)
- Candidate results: [iteration_003_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_results.json)
- Candidate coverage JSON: [iteration_003_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_coverage.json)
- Baseline grammar diff: [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_003_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_003_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_003_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_003_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_003_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_003_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_003_llm_attempt_01_planner_prompt.md, iteration_003_llm_attempt_01_planner_output.json, iteration_003_llm_attempt_01_rewriter_prompt.md, iteration_003_llm_attempt_01_rewriter_output.json, iteration_003_llm_attempt_01_trace.json

### Iteration 4

- Tests run: 50
- Baseline coverage: 52.96%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.45%
- Candidate delta vs champion: -0.55
- Mutation rationale: Add PNG suffixes, richer flag/key combos, and colon‑prefixed routes with queries to hit under‑tested code paths
- Proposed rules: CITY, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) and few successful 200 responses, with most requests hitting generic city or moon routes. Coverage is stuck around 53% and many missing lines belong to view rendering, location lookup, PNG generation and server dispatch logic. The over‑abundant respons...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_004_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_results.json)
- Baseline coverage JSON: [iteration_004_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_coverage.json)
- Candidate results: [iteration_004_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_results.json)
- Candidate coverage JSON: [iteration_004_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_coverage.json)
- Baseline grammar diff: [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_004_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_004_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_004_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_004_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_004_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_004_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_004_llm_attempt_01_planner_prompt.md, iteration_004_llm_attempt_01_planner_output.json, iteration_004_llm_attempt_01_rewriter_prompt.md, iteration_004_llm_attempt_01_rewriter_output.json, iteration_004_llm_attempt_01_trace.json

### Iteration 5

- Tests run: 50
- Baseline coverage: 46.82%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 52.30%
- Candidate delta vs champion: -1.70
- Mutation rationale: Add moon PNG size/lang routes, richer flag/key mixes, and malformed city suffixes to hit PNG, locale, and flag handling code.
- Proposed rules: query, searchparameter, CITY
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many 503/500 errors on simple city or moon routes, while successful 200 responses were dominated by plain city lookups and a few colon‑prefixed config routes. PNG and moon‑related paths are still rare, and flag‑heavy query strings have not triggered many new branches. Covera...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_005_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_results.json)
- Baseline coverage JSON: [iteration_005_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_coverage.json)
- Candidate results: [iteration_005_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_results.json)
- Candidate coverage JSON: [iteration_005_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_coverage.json)
- Baseline grammar diff: [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_005_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_005_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_005_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_005_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_005_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_005_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_005_llm_attempt_01_planner_prompt.md, iteration_005_llm_attempt_01_planner_output.json, iteration_005_llm_attempt_01_rewriter_prompt.md, iteration_005_llm_attempt_01_rewriter_output.json, iteration_005_llm_attempt_01_trace.json

### Iteration 6

- Tests run: 50
- Baseline coverage: 51.86%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.94%
- Candidate delta vs champion: -0.05
- Mutation rationale: Add size/lang suffixes, malformed format/lang values, and richer moon PNG routes to hit uncovered code paths
- Proposed rules: CITY, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) but only 10 successful 200 responses, all coming from a small set of paths (default '/', simple format queries, and a few PNG routes). Coverage is stuck around low‑mid 50% and many lines in view, location, PNG rendering and query parsing remain untouch...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_006_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_results.json)
- Baseline coverage JSON: [iteration_006_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_coverage.json)
- Candidate results: [iteration_006_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_results.json)
- Candidate coverage JSON: [iteration_006_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_coverage.json)
- Baseline grammar diff: [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_006_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_006_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_006_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_006_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_006_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_006_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_006_llm_attempt_02_planner_prompt.md, iteration_006_llm_attempt_02_planner_output.json, iteration_006_llm_attempt_02_rewriter_prompt.md, iteration_006_llm_attempt_02_rewriter_output.json, iteration_006_llm_attempt_02_trace.json

### Iteration 7

- Tests run: 50
- Baseline coverage: 48.85%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 54.00%
- Candidate delta vs champion: +0.00
- Mutation rationale: Add size/language suffixes, richer flag/value mixes, and PNG/moon routes to hit uncovered code paths
- Proposed rules: CITY, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'string' (5 step(s)).`
- Planner analysis: The fuzzer is generating many crashes and a handful of successful 200 responses, but most successes come from generic or malformed query strings (e.g., //:help, weather:...). Moon and PNG routes dominate the crash set, yet their code paths remain largely uncovered. Header diversity is low – only ...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_007_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_results.json)
- Baseline coverage JSON: [iteration_007_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_coverage.json)
- Candidate results: [iteration_007_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_results.json)
- Candidate coverage JSON: [iteration_007_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_coverage.json)
- Baseline grammar diff: [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_007_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_007_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_007_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_007_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_007_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_007_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_007_llm_attempt_03_planner_prompt.md, iteration_007_llm_attempt_03_planner_output.json, iteration_007_llm_attempt_03_rewriter_prompt.md, iteration_007_llm_attempt_03_rewriter_output.json, iteration_007_llm_attempt_03_trace.json

### Iteration 8

- Tests run: 50
- Baseline coverage: 50.11%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 54.27%
- Candidate delta vs champion: +0.27
- Mutation rationale: Add variable PNG size/language routes, malformed flag combos, and richer city patterns per planner
- Proposed rules: query, searchparameter, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many 5xx responses (mostly 503) from simple PNG and format endpoints, while successful 200s came from a few colon‑prefixed API routes and mixed flag queries. Coverage is still low and many lines in view, location and PNG rendering modules remain untouched. The grammar alread...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_008_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_results.json)
- Baseline coverage JSON: [iteration_008_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_coverage.json)
- Candidate results: [iteration_008_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_results.json)
- Candidate coverage JSON: [iteration_008_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_coverage.json)
- Baseline grammar diff: [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_008_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_008_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_008_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_008_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_008_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_008_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_008_llm_attempt_01_planner_prompt.md, iteration_008_llm_attempt_01_planner_output.json, iteration_008_llm_attempt_01_rewriter_prompt.md, iteration_008_llm_attempt_01_rewriter_output.json, iteration_008_llm_attempt_01_trace.json

### Iteration 9

- Tests run: 50
- Baseline coverage: 55.86%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 50.55%
- Candidate delta vs champion: -5.31
- Mutation rationale: Add richer flag syntax, full query support for colon routes, and more flexible city patterns to hit under‑explored code paths.
- Proposed rules: searchparameter, query, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes (29/50) and a modest coverage (~56%). Most successful responses are 200 from simple city or location: routes, while errors dominate moon and PNG variants. Coverage gaps are concentrated in view rendering, location parsing, PNG generation and server dispatch, whi...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_009_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_results.json)
- Baseline coverage JSON: [iteration_009_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_coverage.json)
- Candidate results: [iteration_009_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_results.json)
- Candidate coverage JSON: [iteration_009_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_coverage.json)
- Baseline grammar diff: [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_009_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_009_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_009_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_009_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_009_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_009_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_009_llm_attempt_01_planner_prompt.md, iteration_009_llm_attempt_01_planner_output.json, iteration_009_llm_attempt_01_rewriter_prompt.md, iteration_009_llm_attempt_01_rewriter_output.json, iteration_009_llm_attempt_01_trace.json

### Iteration 10

- Tests run: 50
- Baseline coverage: 51.15%
- Container exit code: 0
- Mutation status: skipped_final_iteration
- Decision: kept_champion
- Baseline results: [iteration_010_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_results.json)
- Baseline coverage JSON: [iteration_010_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_coverage.json)
- Baseline grammar diff: [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/grammar/iteration_010_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z/coverage/iteration_010_baseline_vs_latest_saved_baseline.md)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260511_195338Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_195338Z)
