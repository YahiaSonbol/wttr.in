# Fuzzer Loop Run Report

## Overview

| Field | Value |
|---|---|
| Status | failed |
| Started At | 2026-05-12T19:27:26Z |
| Finished At | 2026-05-12T19:27:28Z |
| Duration Seconds | 1.82 |
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
| Findings Count | 9941 |
| Error | 500 Server Error for http+docker://localhost/v1.54/containers/b0ce214a8e3b00076d26d9049b34ea41b76f1cabfaa2b9de74cf7b229b3f95a5/start: Internal Server Error ("failed to set up container networking: driver failed programming external connectivity on endpoint wttr-fuzzer-655479-1 (171253824ddfd157e5a9b7e397e1089e439ec9c360d5a60b6de8d93232eb9e69): Bind for 0.0.0.0:8002 failed: port is already allocated") |

## Iteration Summary

| Iteration | Tests | Coverage | Success | Warning | Crash | Error | LLM Attempts | Mutation | Candidate Coverage | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | 0 | 0.00% | 0 | 0 | 0 | 0 | 0 | not_started | - | execution_error |

## Iteration Details

### Iteration 1

- Tests run: 0
- Baseline coverage: 0.00%
- Container exit code: None
- Mutation status: not_started
- Decision: execution_error

## Artifacts

- Iteration log: [iterations.jsonl](/home/youssef/github/wttr.in/my_fuzzer/logs/iterations.jsonl)
- Logs directory: [logs](/home/youssef/github/wttr.in/my_fuzzer/logs)
- Findings directory: [findings](/home/youssef/github/wttr.in/my_fuzzer/findings)
- History directory: [history](/home/youssef/github/wttr.in/my_fuzzer/history)
- Run reports directory: [run_20260512_192726Z](/home/youssef/github/wttr.in/my_fuzzer/reports/run_20260512_192726Z)
