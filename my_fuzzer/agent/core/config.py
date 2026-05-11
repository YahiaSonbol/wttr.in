from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
import argparse
import os


@dataclass
class FuzzerConfig:
    # == Main Directories ==
    repo_root: Path
    my_fuzzer_dir: Path
    
    ## == Essential Files ==
    env_file: Path
    grammar_file: Path
    coverage_json: Path
    iteration_log: Path

    ## == Helper Directories ==
    generator_dir: Path
    testcases_dir: Path
    cache_dir: Path
    findings_dir: Path
    history_dir: Path
    logs_dir: Path
    reports_dir: Path
    raw_dir: Path

    # == Target Settings ==
    image: str
    host_port: int
    container_port: int

    # == Fuzzer Settings ==
    iterations: int
    case_count: int
    generation_depth: int
    build_image: bool

    # == Timeouts ==
    request_timeout: float
    startup_timeout: float
    stop_timeout: int

    # == LLM Settings ==
    llm_model: str
    llm_base_url: str
    llm_timeout: float
    llm_attempts: int

    max_missing_files: int
    max_missing_lines_per_file: int

    @property
    def base_url(self) -> str:
        return f"http://localhost:{self.host_port}"

def make_config(args: argparse.Namespace) -> FuzzerConfig:
    repo_root = Path(__file__).resolve().parents[3]
    fuzzer_dir = repo_root / "my_fuzzer"

    env_file = Path(args.env_file).expanduser().resolve() if args.env_file else fuzzer_dir / ".env"
    generator_dir = fuzzer_dir / "generator"
    logs_dir = fuzzer_dir / "logs"
    raw_dir = logs_dir / "raw"
    reports_dir = logs_dir / "reports"

    load_dotenv(env_file)
    llm_model = str(os.getenv("LLM_MODEL_NAME"))
    llm_base_url = str(os.getenv("LLM_BASE_URL"))

    return FuzzerConfig(
        repo_root=repo_root,
        my_fuzzer_dir=fuzzer_dir,

        env_file=env_file,
        grammar_file=fuzzer_dir / "url.g4",
        coverage_json=fuzzer_dir / "coverage.json",
        iteration_log=raw_dir / "iterations.jsonl",

        generator_dir=generator_dir,
        testcases_dir=generator_dir / "test-cases",
        cache_dir=fuzzer_dir / "fuzzer_cache",
        findings_dir=fuzzer_dir / "findings",
        history_dir=fuzzer_dir / "history",
        logs_dir=logs_dir,
        reports_dir=reports_dir,
        raw_dir=raw_dir,
        
        image=args.image,
        host_port=args.host_port,
        container_port=args.container_port,

        iterations=args.iterations,
        case_count=args.cases,
        generation_depth=args.depth,
        build_image=args.build_image,

        request_timeout=args.request_timeout,
        startup_timeout=args.startup_timeout,
        stop_timeout=args.stop_timeout,

        llm_model=llm_model,
        llm_base_url=llm_base_url,
        llm_timeout=args.llm_timeout,
        llm_attempts=max(1, args.llm_attempts),

        max_missing_files=args.max_missing_files,
        max_missing_lines_per_file=args.max_missing_lines_per_file,
    )



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM-guided autonomous grammar fuzzer")
    parser.add_argument("--env-file", default=None)
    parser.add_argument("--iterations", type=int, default=25)
    parser.add_argument("--cases", type=int, default=400)
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
