# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T17:14:16Z |
| Finished At | 2026-05-12T17:21:08Z |
| Duration Seconds | 411.86 |
| Configured Iterations | 10 |
| Completed Iterations | 2 |
| Tests Per Batch | 200 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 50.99% |
| Aggregate Coverage | 55.59% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 8578 |
| Error | Server at http://localhost:8002 did not become ready: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 200 | 50.99% | 8 | 5 | 187 | 0 | 1 | regression | 50.93% | kept_champion |
| 2 | 200 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |
## Aggregate Coverage

- Coverage across all included iterations: 55.59%
- Covered lines: 1015
- Missing lines: 811
- Executable lines: 1826
- Included coverage artifacts: 2
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 200
- Baseline coverage: 50.99%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 50.93%
- Candidate delta vs champion: -0.05
- Mutation rationale: Add concrete literals and alternatives to hit uncovered code paths (debug, static pages, tilde/IP locations, PNG options, imperial flag, etc.)
- Proposed rules: searchparameter, uri, query
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes (503/500) and very few successful responses. Most crashes came from colon‑prefixed multi‑location routes and malformed query strings. Successful hits are limited to generic weather routes, so many code paths (PNG handling, view/format flags, moon routes, debug q...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Line target hints: 6 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 200
- Baseline coverage: 0.00%
- Container exit code: 0
- Mutation status: not_started
- Decision: execution_error
- Baseline results: [iteration_002_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_002_baseline_results.json)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_171416Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_171416Z/summary/cycle_aggregate_coverage.md)
