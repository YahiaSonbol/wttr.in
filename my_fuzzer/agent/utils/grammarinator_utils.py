from ..core.config import FuzzerConfig
from .cli_utils import remove_if_exists, run_command
from pathlib import Path

def generate_testcases(config: FuzzerConfig) -> list[Path]:
    remove_if_exists(config.testcases_dir)
    config.testcases_dir.mkdir(parents=True, exist_ok=True)

    run_command(
        [
            "grammarinator-process",
            str(config.grammar_file),
            "-o",
            str(config.generator_dir),
            "--no-actions",
        ],
        cwd=config.repo_root,
    )

    run_command(
        [
            "grammarinator-generate",
            "urlGenerator.urlGenerator",
            "-r",
            "url",
            "-d",
            str(config.generation_depth),
            "-o",
            "test-cases/payload_%d.txt",
            "-n",
            str(config.case_count),
            "--sys-path",
            ".",
        ],
        cwd=config.generator_dir,
    )

    payloads = sorted(config.testcases_dir.glob("*.txt"))
    if not payloads:
        raise RuntimeError("No payloads were generated.")
    return payloads

