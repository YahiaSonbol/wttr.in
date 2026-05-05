from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def my_fuzzer_dir() -> Path:
    return repo_root() / "my_fuzzer"


@dataclass
class TestResult:
    filename: str
    url: str
    status: str
    status_code: int | None
    error_message: str | None
    response_time_ms: int | None


@dataclass
class FuzzerConfig:
    repo_root: Path
    my_fuzzer_dir: Path
    env_file: Path
    grammar_file: Path
    generator_dir: Path
    testcases_dir: Path
    cache_dir: Path
    findings_dir: Path
    history_dir: Path
    logs_dir: Path
    coverage_json: Path
    iteration_log: Path
    image: str
    host_port: int
    container_port: int
    iterations: int
    case_count: int
    generation_depth: int
    request_timeout: float
    startup_timeout: float
    stop_timeout: int
    build_image: bool
    llm_model: str
    llm_base_url: str
    llm_timeout: float
    llm_attempts: int
    max_missing_files: int
    max_missing_lines_per_file: int

    @property
    def base_url(self) -> str:
        return f"http://localhost:{self.host_port}"


def run_command(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        args,
        cwd=str(cwd),
        env=env,
        text=True,
        input=input_text,
        capture_output=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            f"  cmd: {' '.join(args)}\n"
            f"  cwd: {cwd}\n"
            f"  exit_code: {result.returncode}\n"
            f"  stdout:\n{result.stdout}\n"
            f"  stderr:\n{result.stderr}"
        )
    return result


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def remove_if_exists(path: Path) -> None:
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def write_json(data: Any, output_file: Path) -> None:
    import json

    output_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _strip_matching_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def load_env_file(env_file: Path, *, override: bool = False) -> bool:
    if not env_file.exists():
        return False

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = _strip_matching_quotes(value.strip())
        if override or key not in os.environ:
            os.environ[key] = value
    return True


def load_default_environment() -> list[Path]:
    loaded: list[Path] = []
    for env_file in [repo_root() / ".env", my_fuzzer_dir() / ".env"]:
        if load_env_file(env_file):
            loaded.append(env_file)
    return loaded


def require_runtime_dependencies() -> None:
    missing_modules: list[str] = []
    missing_commands: list[str] = []

    for module_name in ["docker", "requests", "coverage"]:
        if importlib.util.find_spec(module_name) is None:
            missing_modules.append(module_name)

    if not os.environ.get("FUZZER_LLM_COMMAND"):
        for module_name in ["langgraph", "langchain_core", "langchain_openai"]:
            if importlib.util.find_spec(module_name) is None:
                missing_modules.append(module_name)

    for command_name in ["grammarinator-process", "grammarinator-generate"]:
        if shutil.which(command_name) is None:
            missing_commands.append(command_name)

    messages: list[str] = []
    if missing_modules:
        messages.append("python modules: " + ", ".join(missing_modules))
    if missing_commands:
        messages.append("commands: " + ", ".join(missing_commands))

    if messages:
        raise RuntimeError(
            "Missing host dependencies for the fuzzer loop: "
            + "; ".join(messages)
            + ". Install `my_fuzzer/requirements-fuzzer.txt` first."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM-guided autonomous grammar fuzzer")
    parser.add_argument("--env-file", default=None)
    parser.add_argument("--iterations", type=int, default=10)
    parser.add_argument("--cases", type=int, default=100)
    parser.add_argument("--depth", type=int, default=20)
    parser.add_argument("--image", default="wttr:latest")
    parser.add_argument("--host-port", type=int, default=8002)
    parser.add_argument("--container-port", type=int, default=8002)
    parser.add_argument("--startup-timeout", type=float, default=20)
    parser.add_argument("--request-timeout", type=float, default=10)
    parser.add_argument("--stop-timeout", type=int, default=10)
    parser.add_argument("--llm-model", default=None)
    parser.add_argument("--llm-base-url", default=None)
    parser.add_argument("--llm-timeout", type=float, default=180)
    parser.add_argument("--llm-attempts", type=int, default=3)
    parser.add_argument("--build-image", action="store_true")
    parser.add_argument("--max-missing-files", type=int, default=10)
    parser.add_argument("--max-missing-lines-per-file", type=int, default=50)
    return parser.parse_args()


def make_config(args: argparse.Namespace) -> FuzzerConfig:
    root = repo_root()
    fuzzer_dir = my_fuzzer_dir()
    env_file = Path(args.env_file).expanduser().resolve() if args.env_file else fuzzer_dir / ".env"
    generator_dir = fuzzer_dir / "url-fuser"

    llm_model = args.llm_model or os.environ.get("OPENAI_MODEL", "z-ai/glm-4.5-air:free")
    llm_base_url = args.llm_base_url or os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

    return FuzzerConfig(
        repo_root=root,
        my_fuzzer_dir=fuzzer_dir,
        env_file=env_file,
        grammar_file=fuzzer_dir / "url.g4",
        generator_dir=generator_dir,
        testcases_dir=generator_dir / "test-cases",
        cache_dir=fuzzer_dir / "fuzzer_cache",
        findings_dir=fuzzer_dir / "findings",
        history_dir=fuzzer_dir / "history",
        logs_dir=fuzzer_dir / "logs",
        coverage_json=fuzzer_dir / "coverage.json",
        iteration_log=fuzzer_dir / "logs" / "iterations.jsonl",
        image=args.image,
        host_port=args.host_port,
        container_port=args.container_port,
        iterations=args.iterations,
        case_count=args.cases,
        generation_depth=args.depth,
        request_timeout=args.request_timeout,
        startup_timeout=args.startup_timeout,
        stop_timeout=args.stop_timeout,
        build_image=args.build_image,
        llm_model=llm_model,
        llm_base_url=llm_base_url,
        llm_timeout=args.llm_timeout,
        llm_attempts=max(1, args.llm_attempts),
        max_missing_files=args.max_missing_files,
        max_missing_lines_per_file=args.max_missing_lines_per_file,
    )
