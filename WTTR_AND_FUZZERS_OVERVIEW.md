# wttr.in Project And Fuzzers Overview

## What `wttr.in` Is

`wttr.in` is a console-first weather service that exposes weather information through very simple HTTP URLs. The project is designed so a user can query weather data from a terminal with tools such as `curl`, `wget`, `httpie`, or from a browser and scripts. The service can render the same weather information in several output styles, including ANSI terminal output, plain text, HTML, PNG images, JSON, and Prometheus metrics.

At a high level, the repository implements a web service that:

- accepts location-oriented URL paths and query parameters,
- resolves locations such as city names, airport codes, domains, or special places,
- formats the result for humans or scripts,
- exposes special routes such as help pages and moon information,
- supports localization, units, one-line status formats, and image rendering.

The root [README.md](/home/youssef/github/wttr.in/README.md:1) describes the project as a popular weather reporting service and documents how users interact with it over HTTP.

## What The Service Does

The service is built around the idea that the URL itself is the interface. Common behaviors described in the README include:

- weather by current IP-based location, for example `curl wttr.in`,
- weather by city or place, for example `wttr.in/London`,
- weather by airport code, for example `wttr.in/muc`,
- weather for special named places by prefixing the query with `~`,
- weather lookup by domain name such as `wttr.in/@github.com`,
- help and documentation pages such as `wttr.in/:help`,
- moon-related pages such as `/moon` and `/moon@<location>`,
- image rendering with `.png`,
- one-line and structured formats with `?format=...`,
- locale and unit switches through flags and query parameters.

This makes `wttr.in` a good fuzzing target because the server accepts a wide range of URL shapes:

- path-driven inputs,
- query-string flags,
- special static routes,
- format variations,
- location names with many syntactic forms,
- PNG-style path suffixes that encode options in the path itself.

## Repository Context

This repository contains the `wttr.in` application itself plus local fuzzing infrastructure under `my_fuzzer/`.

The fuzzing area contains two related but different systems:

1. an agentic, coverage-guided grammar fuzzer in `my_fuzzer/fuzzer_agent/`,
2. a simpler URL fuzzer in `my_fuzzer/url-fuser/` that relies on Grammarinator-generated URLs and direct HTTP execution.

The main grammar both fuzzers work from is [my_fuzzer/url.g4](/home/youssef/github/wttr.in/my_fuzzer/url.g4:1).

## Why Fuzz `wttr.in`

The server is a strong fuzzing target because:

- its input surface is almost entirely URL-shaped,
- small path or query changes can exercise different code paths,
- special routes exist alongside regular location routes,
- output mode selection changes behavior,
- localization and format flags introduce combinatorial variety,
- malformed or surprising inputs may trigger untested branches or server failures.

Grammar-based fuzzing is a good fit because the input language is structured rather than arbitrary bytes. Instead of sending random strings, the fuzzer sends URLs that are intentionally close to the kinds of requests `wttr.in` expects, while still mutating toward edge cases and under-tested syntax.

## The Agentic Fuzzer

### Purpose

The agentic fuzzer is the more advanced testing loop. Its goal is not just to generate many URLs, but to improve the URL grammar over time using runtime feedback from the real server. It does this by combining grammar-based generation, HTTP execution, line coverage measurement, and an LLM-driven mutation step.

### Main Components

The current implementation is split across these files:

- [my_fuzzer/fuzzer_loop.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_loop.py:1): entry point that starts the fuzzer loop.
- [my_fuzzer/fuzzer_agent/core.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/core.py:1): shared configuration, environment loading, dependency checks, path setup, and subprocess execution helpers.
- [my_fuzzer/fuzzer_agent/coverage_runner.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/coverage_runner.py:1): Grammarinator execution, Docker server control, HTTP test execution, result export, coverage extraction, and artifact writing.
- [my_fuzzer/fuzzer_agent/llm.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/llm.py:1): prompt construction and LLM calling logic for grammar mutation.
- [my_fuzzer/fuzzer_agent/validator.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/validator.py:1): parsing and validating partial grammar edits, and ensuring only allowed rules are changed.
- [my_fuzzer/url.g4](/home/youssef/github/wttr.in/my_fuzzer/url.g4:1): the ANTLR grammar being evolved.

### Agentic Fuzzer Workflow

The loop implemented in [my_fuzzer/fuzzer_agent/orchestrator.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/orchestrator.py:1) follows this broad sequence:

1. Start from the current grammar in `my_fuzzer/url.g4`.
2. Run `grammarinator-process` to turn the grammar into a Python generator.
3. Run `grammarinator-generate` to create many concrete URL payload files.
4. Start a local `wttr.in` server in Docker with coverage enabled.
5. Replay all generated URLs against the server with Python `requests`.
6. Record per-request results such as URL, HTTP status, error text, and response time.
7. Stop the container and extract coverage data with `coverage.py`.
8. Build an LLM prompt from:
   - the current grammar,
   - selected HTTP results,
   - coverage hotspots and missing lines,
   - explicit mutation constraints,
   - hints about useful `wttr.in` route patterns.
9. Ask the LLM for a small mutation plan rather than a full grammar rewrite.
10. Apply only the allowed rule replacements.
11. Validate the candidate grammar with `grammarinator-process`.
12. Re-run the measurement flow with the candidate grammar.
13. Compare the candidate coverage to the current champion grammar.
14. Keep the better grammar and continue the next iteration.

### Why It Is "Agentic"

This fuzzer is called agentic because it closes the loop between execution feedback and the next generation step. The grammar is not static. Instead:

- the fuzzer observes what requests reached the server,
- coverage tells it which code is still under-exercised,
- the prompt gives the LLM concrete evidence from the latest run,
- the model proposes a focused change to a small part of the grammar,
- the validator gates that proposal before it enters the next loop.

This makes it a simple feedback-driven grammar search system rather than a one-shot test generator.

## Tools And Techniques Used By The Agentic Fuzzer

### 1. Grammarinator

Grammarinator is used for grammar-based test generation.

- `grammarinator-process` compiles [my_fuzzer/url.g4](/home/youssef/github/wttr.in/my_fuzzer/url.g4:1) into generator code.
- `grammarinator-generate` produces concrete test case files under `my_fuzzer/url-fuser/test-cases/`.
- The generator target is `urlGenerator.urlGenerator`.

This is the core technique that turns an abstract ANTLR grammar into actual HTTP requests.

Concrete outputs from this toolchain include:

- [my_fuzzer/url-fuser/urlGenerator.py](/home/youssef/github/wttr.in/my_fuzzer/url-fuser/urlGenerator.py:1): generated Python generator code,
- `my_fuzzer/url-fuser/test-cases/payload_*.txt`: generated URL payload files,
- parser-related generated artifacts under `my_fuzzer/.antlr/`.

### 2. ANTLR Grammar Design

The grammar is expressed as an ANTLR4 grammar in `url.g4`. This is important because it gives the fuzzer a structured model of valid and semi-valid URL syntax rather than using blind random mutation.

The validator explicitly distinguishes between:

- mutable rules such as `query`, `search`, `searchparameter`, `string`, `DIGITS`, `HEX`, `STRING`, and `CITY`,
- immutable rules such as `url`, `uri`, `protocol`, `host`, `port`, `PROTOCOL`, `HOSTNAME`, and `PORTS`.

This rule partition is defined in [my_fuzzer/fuzzer_agent/validator.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/validator.py:9).

### 3. Dockerized Server Execution

The fuzzer runs the local `wttr.in` service inside Docker. This provides:

- a reproducible runtime,
- local control over the port,
- coverage file collection through a mounted cache directory,
- clean startup and teardown per run.

This behavior lives in [my_fuzzer/fuzzer_agent/coverage_runner.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/coverage_runner.py:22).

### 4. HTTP Replay With `requests`

After generating payload files, the fuzzer replays them as actual HTTP GET requests against the local server. Each payload becomes a live integration test.

For every request, the fuzzer records:

- the payload filename,
- the URL that was sent,
- the final classification,
- the HTTP status code if there was a response,
- an error message if the request failed,
- the response time in milliseconds.

The classifications used by the agentic fuzzer are:

- `SUCCESS`: the server returned HTTP 200,
- `WARNING`: the server returned a non-200 response below 500,
- `CRASH`: the server returned a 5xx response,
- `ERROR`: the client could not complete the request.

### 5. Coverage-Guided Feedback

The server writes a coverage data file into `my_fuzzer/fuzzer_cache/.coverage`. The fuzzer then:

- copies the coverage file,
- combines data with `coverage combine`,
- exports JSON with `coverage json`,
- analyzes totals, covered lines, and missing lines,
- highlights the most relevant missing-line hotspots.

This happens in [my_fuzzer/fuzzer_agent/coverage_runner.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/coverage_runner.py:194).

Coverage is the main signal used to decide whether a candidate grammar is better than the current one.

Concrete outputs from this stage include:

- `my_fuzzer/fuzzer_cache/.coverage`,
- `my_fuzzer/logs/iteration_*_coverage.json`.

### 6. LLM-Guided Grammar Mutation

The LLM layer in [my_fuzzer/fuzzer_agent/llm.py](/home/youssef/github/wttr.in/my_fuzzer/fuzzer_agent/llm.py:1) does not ask the model to rewrite the whole grammar. Instead it:

- passes the latest meaningful HTTP results,
- passes extracted coverage hotspots,
- shows the immutable base rules,
- shows only the mutable rule blocks,
- includes route-specific hints that are relevant to `wttr.in`,
- instructs the model to change only 1 to 3 rules,
- expects a JSON mutation plan back.

This is a focused prompt-engineering technique that reduces destructive full rewrites and keeps the search localized.

Concrete outputs from this stage include:

- `my_fuzzer/logs/iteration_*_llm_attempt_*_prompt.md`,
- `my_fuzzer/logs/iteration_*_llm_attempt_*.json`,
- candidate grammar snapshots in `my_fuzzer/history/`.

### 7. LangGraph And LangChain

The LLM implementation uses a very small graph-based control flow and an OpenAI-compatible chat model client.

- `llm.py` builds a prompt and calls `ChatOpenAI`.
- The file also contains a simple LangGraph state graph rather than a heavy tool-using ReAct loop.
- A custom external command can also be used through `FUZZER_LLM_COMMAND`.

The practical role of this layer is to generate candidate grammar edits from execution evidence.

### 8. Partial Grammar Editing

One of the strongest safety mechanisms in the system is that the model does not replace the entire grammar file. Instead:

- the validator parses the model response as a mutation plan,
- each update must name a specific mutable rule,
- each replacement must be a complete rule block for that rule,
- duplicate updates are rejected,
- edits to immutable rules are rejected,
- the resulting candidate must still pass `grammarinator-process`.

This keeps the grammar evolution controlled and interpretable.

Concrete outputs from this validation and editing stage include:

- `my_fuzzer/history/iteration_*_before.g4`,
- `my_fuzzer/history/iteration_*_after.g4`,
- `my_fuzzer/history/iteration_*_best.g4`.

### 9. Artifact Logging And Reproducibility

The agentic fuzzer writes out a large set of artifacts so each iteration can be inspected later. This is an important debugging and research technique because it lets you compare:

- what inputs were generated,
- how the server responded,
- what coverage changed,
- what prompt the model saw,
- what change the model proposed,
- whether the change validated,
- whether the candidate grammar was accepted or rejected.

## Agentic Fuzzer Outputs

The agentic fuzzer produces several categories of output under `my_fuzzer/`.

### Generated Inputs

- `my_fuzzer/url-fuser/test-cases/*.txt`

These are concrete generated URLs, one per file. They are the raw inputs that get sent to the local server.

### Coverage Cache

- `my_fuzzer/fuzzer_cache/.coverage`
- many cached payload-derived artifacts under `my_fuzzer/fuzzer_cache/`

The cache directory stores the runtime coverage file and related generated inputs used during fuzzing.

### Per-Iteration Request Results

- `my_fuzzer/logs/iteration_*_results.json`
- `my_fuzzer/logs/iteration_*_results.md`
- `my_fuzzer/logs/iteration_*_baseline_results.json`
- `my_fuzzer/logs/iteration_*_baseline_results.md`
- `my_fuzzer/logs/iteration_*_candidate_results.json`
- `my_fuzzer/logs/iteration_*_candidate_results.md`

These files capture the actual request execution results for each batch. They let you inspect which generated URLs succeeded, warned, errored, or crashed.

### Coverage Reports

- `my_fuzzer/logs/iteration_*_coverage.json`

These JSON files contain exported line coverage data from the instrumented server run.

### LLM Prompt And Trace Files

- `my_fuzzer/logs/iteration_*_llm_attempt_*_prompt.md`
- `my_fuzzer/logs/iteration_*_llm_attempt_*.json`
- older attempt artifacts such as `iteration_001_attempt_01_prompt.md`, `iteration_001_attempt_01_response.txt`, and `iteration_001_attempt_01_validation.txt`

These files are useful for understanding why the grammar changed. They preserve the exact mutation prompt, the structured attempt trace, and in some cases the raw model response or validation feedback.

### Run-Level Reports

- `my_fuzzer/logs/iterations.jsonl`
- `my_fuzzer/logs/latest_run_report.md`
- `my_fuzzer/logs/run_report_*.md`

These summarize the run across iterations and track coverage, decisions, and selected artifacts.

### Grammar History

- `my_fuzzer/history/iteration_*_before.g4`
- `my_fuzzer/history/iteration_*_after.g4`
- `my_fuzzer/history/iteration_*_best.g4`

These are snapshots of the grammar before mutation, after mutation, and after selection. They make the grammar evolution auditable over time.

### Findings And Interesting Cases

- `my_fuzzer/findings/`

This directory stores saved findings such as crash-inducing or otherwise notable payloads together with metadata and grammar context so they can be investigated later.

## Tool-To-Output Map

The fuzzing work in this repository is easier to understand if each major tool is tied to its direct outputs:

| Tool or Technique | Role | Typical Output |
|---|---|---|
| ANTLR grammar in `my_fuzzer/url.g4` | Defines the URL language | source grammar that drives both fuzzers |
| `grammarinator-process` | Compiles grammar into generator code | `my_fuzzer/url-fuser/urlGenerator.py` and related generated parser artifacts |
| `grammarinator-generate` | Produces concrete test inputs | `my_fuzzer/url-fuser/test-cases/payload_*.txt` |
| Python `requests` replay | Executes generated URLs against the server | request status, status code, timing, and error data |
| Docker target execution | Runs the local `wttr.in` server in an isolated environment | container logs and a mounted coverage file |
| `coverage.py` | Measures executed and missing lines | `.coverage` data and `iteration_*_coverage.json` |
| LLM mutation step | Proposes focused grammar edits | `iteration_*_llm_attempt_*_prompt.md` and trace JSON |
| Validator | Enforces safe partial grammar edits and syntax validity | accepted or rejected candidate grammar plus validation feedback |
| History snapshots | Preserve grammar evolution | `iteration_*_before.g4`, `iteration_*_after.g4`, `iteration_*_best.g4` |
| Findings capture | Saves interesting or failing cases | `my_fuzzer/findings/...` with metadata, payloads, and grammar context |

## The Separate URL Fuzzer

### Purpose

The separate URL fuzzer is a simpler, more direct fuzzer. It is useful when you want to generate URLs from the grammar and test them against the server without involving the full agentic coverage-guided loop.

It lives primarily in:

- [my_fuzzer/url-fuser/test_runner.py](/home/youssef/github/wttr.in/my_fuzzer/url-fuser/test_runner.py:1)
- [my_fuzzer/url-fuser/urlGenerator.py](/home/youssef/github/wttr.in/my_fuzzer/url-fuser/urlGenerator.py:1)
- [my_fuzzer/url-fuser/test_results.md](/home/youssef/github/wttr.in/my_fuzzer/url-fuser/test_results.md:1)

### How It Works

The separate URL fuzzer uses the same grammar source but a much simpler execution model:

1. `grammarinator-process` compiles the grammar.
2. `grammarinator-generate` produces URL payload files.
3. The Python test runner reads every generated `.txt` payload file.
4. Each URL is sent to the local backend using `requests.get(...)`.
5. The result is stored in a Python dictionary.
6. All results are exported into a markdown table.

Unlike the agentic fuzzer, this simpler fuzzer does not:

- collect coverage,
- build LLM prompts,
- mutate the grammar,
- validate candidate grammar edits,
- compare champion and candidate grammars across iterations.

### Output Of The Separate URL Fuzzer

The main output artifact is:

- [my_fuzzer/url-fuser/test_results.md](/home/youssef/github/wttr.in/my_fuzzer/url-fuser/test_results.md:1)

That file contains a markdown table with:

- filename,
- URL,
- status,
- HTTP status code,
- error message.

The status model in this smaller fuzzer is simpler than the agentic one:

- `SUCCESS` for HTTP 200,
- `WARNING` for non-200 HTTP responses,
- `ERROR` for timeouts, connection failures, and other request exceptions.

It is essentially a grammar-driven URL replay tool plus report generator.

## Difference Between The Two Fuzzers

### Agentic Fuzzer

- uses grammar-based generation,
- runs the server inside Docker,
- collects line coverage,
- builds prompts from live execution data,
- asks an LLM to mutate only selected grammar rules,
- validates the candidate grammar,
- compares candidate performance against the current best grammar,
- stores a rich artifact trail.

### Separate URL Fuzzer

- uses grammar-based generation,
- sends requests directly with `requests`,
- records request outcomes,
- exports a markdown report,
- does not evolve the grammar,
- does not use coverage,
- does not use an LLM.

The agentic fuzzer is for iterative improvement of the input model. The separate URL fuzzer is for straightforward grammar-based endpoint exercising and quick reporting.

## Important Techniques Across The Fuzzing Work

Several broader testing techniques are being used in this repository:

- grammar-based fuzzing with ANTLR and Grammarinator,
- structure-preserving mutation rather than byte-level randomness,
- coverage-guided exploration,
- real HTTP integration testing instead of mocked handlers,
- containerized target execution,
- prompt engineering for constrained grammar evolution,
- partial program transformation instead of full-file regeneration,
- artifact-driven debugging and reproducibility.

Together, these techniques make the fuzzing setup useful both for finding failures and for learning how to generate more interesting `wttr.in` requests over time.

## Summary

`wttr.in` is a URL-centric weather service with a wide and expressive HTTP input space. The repository includes two fuzzing systems tailored to that interface.

The separate URL fuzzer is the lightweight option: generate URLs from a grammar, send them to the server, and record what happened.

The agentic fuzzer is the research-oriented option: generate URLs, measure real coverage, use the latest execution evidence to guide an LLM, mutate only safe parts of the grammar, validate the result, and iterate toward better server exploration.

For this project, the important outputs are not just crashes. They also include:

- generated test cases,
- per-request execution reports,
- coverage JSON,
- prompt and trace files,
- grammar history snapshots,
- saved findings,
- run-level summaries.

That combination makes the fuzzing work understandable, repeatable, and useful for improving both the grammar and the confidence in the `wttr.in` server.
