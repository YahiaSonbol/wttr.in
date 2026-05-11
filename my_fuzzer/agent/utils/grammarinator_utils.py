from pathlib import Path

from ..core.config import FuzzerConfig
from .cli_utils import remove_if_exists, run_command


def generate_testcases(config: FuzzerConfig, count: int | None = None) -> list[Path]:
    remove_if_exists(config.generator_dir)
    config.generator_dir.mkdir(parents=True, exist_ok=True)
    config.testcases_dir.mkdir(parents=True, exist_ok=True)
    requested_count = int(count if count is not None else config.case_count)

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
            str(requested_count),
            "--sys-path",
            ".",
        ],
        cwd=config.generator_dir,
    )

    payloads = sorted(config.testcases_dir.glob("*.txt"))
    if not payloads:
        raise RuntimeError("No payloads were generated.")
    return payloads
