# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T16:32:33Z |
| Finished At | 2026-05-12T17:12:35Z |
| Duration Seconds | 2402.51 |
| Configured Iterations | 10 |
| Completed Iterations | 3 |
| Tests Per Batch | 400 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 56.63% |
| Aggregate Coverage | 60.79% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 8548 |
| Error | Server at http://localhost:8002 did not become ready: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 400 | 55.26% | 70 | 28 | 302 | 0 | 1 | accepted | 56.63% | promoted_to_champion |
| 2 | 400 | 55.86% | 130 | 100 | 169 | 1 | 1 | regression | 56.57% | kept_champion |
| 3 | 400 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |
## Aggregate Coverage

- Coverage across all included iterations: 60.79%
- Covered lines: 1110
- Missing lines: 716
- Executable lines: 1826
- Included coverage artifacts: 4
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 400
- Baseline coverage: 55.26%
- Container exit code: 0
- Mutation status: accepted
- Decision: promoted_to_champion
- Candidate coverage: 56.63%
- Candidate delta vs champion: +1.37
- Mutation rationale: Add concrete flag bundles, IP/tilde/payload locations, and colon‑prefixed multi‑location routes to hit uncovered Python logic.
- Proposed rules: searchparameter, CITY, uri
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) and few successful 200 responses, indicating the fuzzer is over‑generating malformed paths and under‑exercising the richer query‑flag and PNG‑filename logic that drives most of the uncovered Python code. Coverage gaps cluster around view/format handlin...
- Reachable by grammar: 4 items
- Reachable by headers only: 2 items
- Unreachable (harness): 2 items
- Line target hints: 8 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 400
- Baseline coverage: 55.86%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 56.57%
- Candidate delta vs champion: -0.05
- Mutation rationale: Add concrete flag, key/value, and location alternatives to hit parsing, PNG, and moon branches
- Proposed rules: FLAG_BUNDLE, searchparameter, uri
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)
- Baseline coverage JSON: [iteration_002_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_coverage.json)
- Candidate results: [iteration_002_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_results.json)
- Candidate coverage JSON: [iteration_002_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_candidate_coverage.json)
- Baseline grammar diff: [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/grammar/iteration_002_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_002_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/coverage/iteration_002_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_002_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/grammar/iteration_002_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_002_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/coverage/iteration_002_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_002_llm_attempt_01_planner_prompt.md, iteration_002_llm_attempt_01_planner_output.json, iteration_002_llm_attempt_01_rewriter_prompt.md, iteration_002_llm_attempt_01_rewriter_output.json, iteration_002_llm_attempt_01_trace.json

### Iteration 3

- Tests run: 400
- Baseline coverage: 0.00%
- Container exit code: 0
- Mutation status: not_started
- Decision: execution_error
- Baseline results: [iteration_003_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_003_baseline_results.json)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_163233Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_163233Z/summary/cycle_aggregate_coverage.md)
