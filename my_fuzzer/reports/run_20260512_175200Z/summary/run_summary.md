# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T17:52:00Z |
| Finished At | 2026-05-12T17:52:25Z |
| Duration Seconds | 24.59 |
| Configured Iterations | 10 |
| Completed Iterations | 1 |
| Tests Per Batch | 400 |
| Generation Depth | 20 |
| Image | wttr:latest |
| Base URL | http://localhost:8002 |
| LLM Model | openai/gpt-oss-120b:free |
| Champion Coverage | 0.00% |
| Aggregate Coverage | - |
| Final Grammar | /home/youssef/github/wttr.in/my_fuzzer/url.g4 |
| Findings Count | 9910 |
| Error | Server at http://localhost:8002 did not become ready: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer')) |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 400 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |

## Iteration Details

### Iteration 1

- Tests run: 400
- Baseline coverage: 0.00%
- Container exit code: 0
- Mutation status: not_started
- Decision: execution_error
- Baseline results: [iteration_001_baseline_results.json](/home/youssef/github/wttr.in/my_fuzzer/logs/iteration_001_baseline_results.json)

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_175200Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_175200Z)
