# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T17:24:31Z |
| Finished At | 2026-05-12T17:49:29Z |
| Duration Seconds | 1498.38 |
| Configured Iterations | 10 |
| Completed Iterations | 4 |
| Tests Per Batch | 1000 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | MiniMaxAI/MiniMax-M2.7 |
| Champion Coverage | 59.26% |
| Aggregate Coverage | 61.99% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 9910 |
| Error | Server at http://localhost:8002 did not become ready: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 1000 | 52.30% | 141 | 144 | 715 | 0 | 2 | accepted | 59.26% | promoted_to_champion |
| 2 | 1000 | 59.15% | 459 | 13 | 527 | 1 | 1 | regression | 57.28% | kept_champion |
| 3 | 1000 | 58.00% | 401 | 16 | 583 | 0 | 1 | candidate_execution_error | - | kept_champion |
| 4 | 1000 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |
## Aggregate Coverage

- Coverage across all included iterations: 61.99%
- Covered lines: 1132
- Missing lines: 694
- Executable lines: 1826
- Included coverage artifacts: 5
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 1000
- Baseline coverage: 52.30%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 59.26%
- Candidate delta vs champion: +6.96
- Mutation rationale: Fix broken optional-colon pattern in uri, add structured PNG/multi-location/moon date alternatives to query, and add use_imperial/narrow parameters to searchparameter to reach uncovered Python branches.
- Proposed rules: uri, query, searchparameter
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The previous run generated 715 crashes (71.5%) due to malformed URL structures, particularly from the `(':' )?` optional colon pattern in the uri rule producing invalid routes like `/:weather:moon`. The grammar also lacks structured alternatives for PNG routes with proper dimensions, moon date va...
- Reachable by grammar: 7 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Line target hints: 5 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_02_planner_prompt.md, iteration_001_llm_attempt_02_planner_output.json, iteration_001_llm_attempt_02_rewriter_prompt.md, iteration_001_llm_attempt_02_rewriter_output.json, iteration_001_llm_attempt_02_trace.json

### Iteration 2

- Tests run: 1000
- Baseline coverage: 59.15%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 57.28%
- Candidate delta vs champion: -1.97
- Mutation rationale: Add missing format modes, PNG parameters, static file routes, and fix malformed path generation to reduce 500 errors and reach uncovered Python branches.
- Proposed rules: query, searchparameter, uri
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The fuzzer generated 527 crashes (mostly 500 errors) from 1000 requests, indicating the grammar produces many malformed or server-rejected inputs. Coverage is at 59.14% with significant gaps in lib/view/v2.py (310 missing), lib/view/line.py (126 missing), lib/location.py (82 missing), lib/fmt/png...
- Reachable by grammar: 8 items
- Reachable by headers only: 4 items
- Unreachable (harness): 4 items
- Line target hints: 7 items
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)
- Baseline coverage JSON: [iteration_002_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_coverage.json)
- Candidate results: [iteration_002_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_results.json)
- Candidate coverage JSON: [iteration_002_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_coverage.json)
- Baseline grammar diff: [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_002_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_002_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_002_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_002_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_002_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_002_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_002_llm_attempt_01_planner_prompt.md, iteration_002_llm_attempt_01_planner_output.json, iteration_002_llm_attempt_01_rewriter_prompt.md, iteration_002_llm_attempt_01_rewriter_output.json, iteration_002_llm_attempt_01_trace.json

### Iteration 3

- Tests run: 1000
- Baseline coverage: 58.00%
- Container exit code: 0
- Mutation status: candidate_execution_error
- Decision: kept_champion
- Mutation rationale: Add PNG rendering parameters, numeric format modes, custom format placeholders, and static file routes to reach uncovered Python branches in lib/fmt/png.py, lib/view/line.py, and lib/wttr_srv.py.
- Proposed rules: query, searchparameter, uri
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: Coverage is flat at ~58% across 3 iterations. The grammar generates many crash-inducing requests (58% error rate) but fails to reach key Python branches. The biggest gaps are in lib/view/v2.py (310 missing lines), lib/view/line.py (115 missing), and lib/fmt/png.py (72 missing). Many missing lines...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 4 items
- Line target hints: 5 items
- Baseline results: [iteration_003_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_results.json)
- Baseline coverage JSON: [iteration_003_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_coverage.json)
- Candidate results: [iteration_003_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_candidate_results.json)
- Baseline grammar diff: [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_003_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_003_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_003_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_003_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/grammar/iteration_003_current_vs_candidate.md)
- Candidate coverage diff (not_available): [iteration_003_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/coverage/iteration_003_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_003_llm_attempt_01_planner_prompt.md, iteration_003_llm_attempt_01_planner_output.json, iteration_003_llm_attempt_01_rewriter_prompt.md, iteration_003_llm_attempt_01_rewriter_output.json, iteration_003_llm_attempt_01_trace.json

### Iteration 4

- Tests run: 1000
- Baseline coverage: 0.00%
- Container exit code: 0
- Mutation status: not_started
- Decision: execution_error
- Baseline results: [iteration_004_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_004_baseline_results.json)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_172431Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_172431Z/summary/cycle_aggregate_coverage.md)
