# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T17:53:20Z |
| Finished At | 2026-05-12T18:00:31Z |
| Duration Seconds | 430.16 |
| Configured Iterations | 10 |
| Completed Iterations | 2 |
| Tests Per Batch | 400 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 56.85% |
| Aggregate Coverage | 59.53% |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 9941 |
| Error | Server at http://localhost:8002 did not become ready: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 400 | 56.85% | 92 | 0 | 308 | 0 | 1 | regression | 54.98% | kept_champion |
| 2 | 400 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |
## Aggregate Coverage

- Coverage across all included iterations: 59.53%
- Covered lines: 1087
- Missing lines: 739
- Executable lines: 1826
- Included coverage artifacts: 2
- Aggregate report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/summary/cycle_aggregate_coverage.md)


## Iteration Details

### Iteration 1

- Tests run: 400
- Baseline coverage: 56.85%
- Container exit code: 0
- Mutation status: regression
- Decision: kept_champion
- Candidate coverage: 54.98%
- Candidate delta vs champion: -1.86
- Mutation rationale: Add concrete literals and path forms to hit under‑explored view, PNG, location and debug branches.
- Proposed rules: searchparameter, uri, search
- Validation summary: `The farthest rule from 'url' is 'string' (4 step(s)).`
- Planner analysis: The last run produced many crashes (500/503) and a modest number of successful 200 responses, most of which came from the static colon‑prefixed routes (:help, :translation, :iterm2). PNG and moon routes dominate the failures, while multi‑location cycling, detailed format flags and PNG filename op...
- Reachable by grammar: 5 items
- Reachable by headers only: 3 items
- Unreachable (harness): 2 items
- Line target hints: 11 items
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)
- Baseline coverage JSON: [iteration_001_baseline_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_coverage.json)
- Candidate results: [iteration_001_candidate_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_results.json)
- Candidate coverage JSON: [iteration_001_candidate_coverage.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_candidate_coverage.json)
- Baseline grammar diff: [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/grammar/iteration_001_baseline_vs_latest_saved_baseline.md)
- Baseline coverage diff (available): [iteration_001_baseline_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/coverage/iteration_001_baseline_vs_latest_saved_baseline.md)
- Candidate grammar diff: [iteration_001_current_vs_candidate.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/grammar/iteration_001_current_vs_candidate.md)
- Candidate coverage diff (available): [iteration_001_candidate_vs_latest_saved_baseline.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/coverage/iteration_001_candidate_vs_latest_saved_baseline.md)
- LLM artifacts: iteration_001_llm_attempt_01_planner_prompt.md, iteration_001_llm_attempt_01_planner_output.json, iteration_001_llm_attempt_01_rewriter_prompt.md, iteration_001_llm_attempt_01_rewriter_output.json, iteration_001_llm_attempt_01_trace.json

### Iteration 2

- Tests run: 400
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
- Run reports directory: [run_20260512_175320Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z)
- Aggregate coverage report: [cycle_aggregate_coverage.md](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175320Z/summary/cycle_aggregate_coverage.md)
