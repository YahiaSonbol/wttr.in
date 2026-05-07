#!/usr/bin/env python3

from __future__ import annotations

import logging

from agent.orchestrator import main


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


if __name__ == "__main__":
    setup_logging()
    raise SystemExit(main())
