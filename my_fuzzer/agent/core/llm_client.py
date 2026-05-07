from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .config import FuzzerConfig

_chat_client: ChatOpenAI | None = None


def get_chat_client(config: FuzzerConfig) -> ChatOpenAI:
    global _chat_client

    if _chat_client is not None:
        return _chat_client

    load_dotenv(config.env_file)
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError(
            f"Missing `LLM_API_KEY`. Put it in `{config.env_file}` or export it first."
        )

    _chat_client = ChatOpenAI(
        model=config.llm_model,
        api_key=api_key,
        base_url=config.llm_base_url,
        timeout=config.llm_timeout,
        temperature=0.2,
        max_tokens=8192,
        max_retries=0,
    )
    return _chat_client
