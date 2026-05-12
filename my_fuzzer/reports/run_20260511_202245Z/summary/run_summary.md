# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | completed |
| Started At | 2026-05-11T20:22:45Z |
| Finished At | 2026-05-11T20:47:56Z |
| Duration Seconds | 1511.00 |
| Configured Iterations | 10 |
| Completed Iterations | 10 |
| Tests Per Batch | 50 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 55.42% |
| Aggregate Coverage | 59.42% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 8410 |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 50 | 53.45% | 18 | 1 | 31 | 0 | 1 | accepted | 53.89% | promoted_to_champion |
| 2 | 50 | 53.23% | 19 | 7 | 24 | 0 | 1 | regression | 51.86% | kept_champion |
| 3 | 50 | 55.15% | 18 | 9 | 23 | 0 | 1 | regression | 52.79% | kept_champion |
| 4 | 50 | 53.72% | 13 | 7 | 30 | 0 | 1 | regression | 51.48% | kept_champion |
| 5 | 50 | 55.42% | 12 | 10 | 28 | 0 | 1 | regression | 49.78% | kept_champion |
| 6 | 50 | 54.49% | 7 | 9 | 34 | 0 | 1 | regression | 54.93% | kept_champion |
| 7 | 50 | 51.10% | 0 | 5 | 45 | 0 | 1 | regression | 53.45% | kept_champion |
| 8 | 50 | 54.98% | 7 | 7 | 36 | 0 | 1 | regression | 49.95% | kept_champion |
| 9 | 50 | 54.27% | 17 | 3 | 30 | 0 | 1 | regression | 53.50% | kept_champion |
| 10 | 50 | 54.76% | 8 | 9 | 33 | 0 | 0 | skipped_final_iteration | - | kept_champion |
## Aggregate Coverage

- Coverage across all included iterations: 59.42%
- Covered lines: 1085
- Missing lines: 741
- Executable lines: 1826
- Included coverage artifacts: 19
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 50
- Baseline coverage: 53.45%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 53.89%
- Candidate delta vs champion: +0.44
- Mutation rationale: Add percent‑encoding and flexible flags, and allow optional leading ':' to broaden URL families.
- Proposed rules: CITY, searchparameter, uri
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes (31) and a high proportion of 5xx responses, especially 503 from moon PNG routes and generic malformed query strings. Successful 200s are concentrated in colon‑prefixed API routes and some moon format queries. Coverage is low and many missing lines belong to vie...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 50
- Baseline coverage: 53.23%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.86%
- Candidate delta vs champion: -2.03
- Mutation rationale: Add flag‑only chains, percent‑encoded city with size/lang, and optional double slash to broaden PNG and API route coverage
- Proposed rules: searchparameter, CITY, uri
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many 503/500 responses and few distinct successful paths. Most crashes came from malformed PNG and moon routes with odd flags. Successes are limited to simple format queries and colon‑prefixed help routes. Coverage gaps are concentrated in view rendering, location parsing, P...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)
- Baseline coverage JSON: [iteration_002_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_coverage.json)
- Candidate results: [iteration_002_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_results.json)
- Candidate coverage JSON: [iteration_002_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_coverage.json)
- Baseline grammar diff: [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_002_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_002_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_002_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_002_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_002_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_002_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_002_llm_attempt_01_planner_prompt.md, iteration_002_llm_attempt_01_planner_output.json, iteration_002_llm_attempt_01_rewriter_prompt.md, iteration_002_llm_attempt_01_rewriter_output.json, iteration_002_llm_attempt_01_trace.json

### Iteration 3

- Tests run: 50
- Baseline coverage: 55.15%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 52.79%
- Candidate delta vs champion: -2.35
- Mutation rationale: Add productions to hit PNG size/lang validation, moon PNG with flags, and flag‑only parsing loops
- Proposed rules: searchparameter, CITY, query
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many 503 service errors and a handful of 200/404 responses. Crashes are concentrated on PNG and moon routes with malformed size/lang flags. Successful 200s come mainly from colon‑prefixed API routes and simple location lookups. Coverage gaps are large in view rendering, loca...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_003_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_results.json)
- Baseline coverage JSON: [iteration_003_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_coverage.json)
- Candidate results: [iteration_003_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_results.json)
- Candidate coverage JSON: [iteration_003_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_coverage.json)
- Baseline grammar diff: [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_003_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_003_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_003_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_003_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_003_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_003_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_003_llm_attempt_01_planner_prompt.md, iteration_003_llm_attempt_01_planner_output.json, iteration_003_llm_attempt_01_rewriter_prompt.md, iteration_003_llm_attempt_01_rewriter_output.json, iteration_003_llm_attempt_01_trace.json

### Iteration 4

- Tests run: 50
- Baseline coverage: 53.72%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 51.48%
- Candidate delta vs champion: -3.67
- Mutation rationale: Add colon‑prefixed API routes, richer flag chains, and expanded city patterns to hit under‑tested code paths
- Proposed rules: query, searchparameter, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 503/500 errors, while successful 200 responses were limited to simple default, format, and moon endpoints. PNG and colon‑prefixed API routes are generating mostly errors, indicating they are under‑tested. Coverage gaps are concentrated in view rendering (v2,...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_004_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_results.json)
- Baseline coverage JSON: [iteration_004_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_coverage.json)
- Candidate results: [iteration_004_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_results.json)
- Candidate coverage JSON: [iteration_004_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_candidate_coverage.json)
- Baseline grammar diff: [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_004_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_004_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_004_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_004_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_004_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_004_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_004_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_004_llm_attempt_01_planner_prompt.md, iteration_004_llm_attempt_01_planner_output.json, iteration_004_llm_attempt_01_rewriter_prompt.md, iteration_004_llm_attempt_01_rewriter_output.json, iteration_004_llm_attempt_01_trace.json

### Iteration 5

- Tests run: 50
- Baseline coverage: 55.42%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 49.78%
- Candidate delta vs champion: -5.64
- Mutation rationale: Add explicit language/size flags, richer city patterns, and colon‑prefixed API routes with full queries to hit under‑explored code paths.
- Proposed rules: searchparameter, CITY, query
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 500/503 errors, with a heavy bias toward colon‑prefixed and PNG‑related paths. Successful 200 responses are limited to a few simple routes (/:moon, //:source, :help etc.). Coverage gaps are concentrated in view rendering, location parsing, PNG generation and...
- Reachable by grammar: 3 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_005_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_results.json)
- Baseline coverage JSON: [iteration_005_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_baseline_coverage.json)
- Candidate results: [iteration_005_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_results.json)
- Candidate coverage JSON: [iteration_005_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_005_candidate_coverage.json)
- Baseline grammar diff: [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_005_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_005_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_005_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_005_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_005_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_005_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_005_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_005_llm_attempt_01_planner_prompt.md, iteration_005_llm_attempt_01_planner_output.json, iteration_005_llm_attempt_01_rewriter_prompt.md, iteration_005_llm_attempt_01_rewriter_output.json, iteration_005_llm_attempt_01_trace.json

### Iteration 6

- Tests run: 50
- Baseline coverage: 54.49%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 54.93%
- Candidate delta vs champion: -0.49
- Mutation rationale: Add richer flag/key chains, explicit help routes with format/lang, and more flexible city syntax for size/lang and hex sequences
- Proposed rules: searchparameter, query, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 500/503 errors, with very few successful 200 responses. Most hits come from generic city or flag‑only queries, while special routes (moon, PNG with size/lang, colon‑prefixed APIs) are still yielding errors or no coverage. Missing lines are concentrated in vi...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Baseline results: [iteration_006_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_results.json)
- Baseline coverage JSON: [iteration_006_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_baseline_coverage.json)
- Candidate results: [iteration_006_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_results.json)
- Candidate coverage JSON: [iteration_006_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_006_candidate_coverage.json)
- Baseline grammar diff: [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_006_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_006_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_006_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_006_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_006_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_006_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_006_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_006_llm_attempt_01_planner_prompt.md, iteration_006_llm_attempt_01_planner_output.json, iteration_006_llm_attempt_01_rewriter_prompt.md, iteration_006_llm_attempt_01_rewriter_output.json, iteration_006_llm_attempt_01_trace.json

### Iteration 7

- Tests run: 50
- Baseline coverage: 51.10%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.45%
- Candidate delta vs champion: -1.97
- Mutation rationale: Add plain weather, help routes, balanced flag/key=value combos, and richer city syntax to hit core view and location code.
- Proposed rules: query, searchparameter, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes (90% of responses) and very little successful traffic, indicating the grammar is over‑focusing on malformed paths (colon‑prefixed, flag‑only chains, extreme PNG size/lang combos). Coverage is still low and many core modules (view, location, png, server) have lar...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_007_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_results.json)
- Baseline coverage JSON: [iteration_007_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_baseline_coverage.json)
- Candidate results: [iteration_007_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_results.json)
- Candidate coverage JSON: [iteration_007_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_007_candidate_coverage.json)
- Baseline grammar diff: [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_007_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_007_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_007_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_007_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_007_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_007_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_007_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_007_llm_attempt_01_planner_prompt.md, iteration_007_llm_attempt_01_planner_output.json, iteration_007_llm_attempt_01_rewriter_prompt.md, iteration_007_llm_attempt_01_rewriter_output.json, iteration_007_llm_attempt_01_trace.json

### Iteration 8

- Tests run: 50
- Baseline coverage: 54.98%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 49.95%
- Candidate delta vs champion: -5.48
- Mutation rationale: Add colon‑prefixed API routes with full queries, enhance flag‑only and mixed flag/key=value handling, and broaden CITY percent‑encoding patterns for deeper coverage.
- Proposed rules: query, searchparameter, CITY
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 503s, with only a handful of successful 200 responses. Successes are concentrated on simple format queries and basic moon PNG routes, while most paths (colon‑prefixed APIs, extended PNG size/lang routes, flag‑only chains) trigger server errors. Coverage gaps...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_008_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_results.json)
- Baseline coverage JSON: [iteration_008_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_baseline_coverage.json)
- Candidate results: [iteration_008_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_results.json)
- Candidate coverage JSON: [iteration_008_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_008_candidate_coverage.json)
- Baseline grammar diff: [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_008_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_008_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_008_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_008_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_008_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_008_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_008_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_008_llm_attempt_01_planner_prompt.md, iteration_008_llm_attempt_01_planner_output.json, iteration_008_llm_attempt_01_rewriter_prompt.md, iteration_008_llm_attempt_01_rewriter_output.json, iteration_008_llm_attempt_01_trace.json

### Iteration 9

- Tests run: 50
- Baseline coverage: 54.27%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 53.50%
- Candidate delta vs champion: -1.92
- Mutation rationale: Expand CITY for deeper PNG combos, add flag‑only chains, and create moon routes with size/language and format flags
- Proposed rules: CITY, searchparameter, query
- Validation summary: `The farthest rule from 'url' is 'STRING' (4 step(s)).`
- Planner analysis: The last run produced many crashes and 500/503 errors, with a heavy bias toward colon‑prefixed routes and generic flag chains. Successful 200 responses are clustered around simple ?format= queries and help routes, while moon and PNG variants are mostly causing server errors, indicating they are u...
- Reachable by grammar: 4 items
- Reachable by headers only: 3 items
- Unreachable (harness): 3 items
- Baseline results: [iteration_009_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_results.json)
- Baseline coverage JSON: [iteration_009_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_baseline_coverage.json)
- Candidate results: [iteration_009_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_results.json)
- Candidate coverage JSON: [iteration_009_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_009_candidate_coverage.json)
- Baseline grammar diff: [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_009_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_009_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_009_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_009_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_009_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_009_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_009_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_009_llm_attempt_01_planner_prompt.md, iteration_009_llm_attempt_01_planner_output.json, iteration_009_llm_attempt_01_rewriter_prompt.md, iteration_009_llm_attempt_01_rewriter_output.json, iteration_009_llm_attempt_01_trace.json

### Iteration 10

- Tests run: 50
- Baseline coverage: 54.76%
- Container exit code: 0
- Mutation status: skipped_final_iteration
- Decision: kept_champion
- Baseline results: [iteration_010_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_results.json)
- Baseline coverage JSON: [iteration_010_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_010_baseline_coverage.json)
- Baseline grammar diff: [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/grammar/iteration_010_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_010_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/coverage/iteration_010_baseline_vs_latest_saved_baseline.md)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260511_202245Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260511_202245Z/summary/cycle_aggregate_coverage.md)
