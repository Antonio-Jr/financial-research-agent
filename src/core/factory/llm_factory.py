from functools import lru_cache
from typing import Any

from openai import AsyncOpenAI

from agents import OpenAIChatCompletionsModel
from src.config import settings


class InitLLM:
    """
    Factory class responsible for initializing and configuring the LLM provider.
    Implements a Singleton pattern using lru_cache to ensure connection pooling
    and resource efficiency.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def configure() -> Any:
        """
        Configures the OpenAI Chat Completions model using environment settings.

        Returns:
            An instance of the configured LLM model ready for Agent consumption.
        """
        # AsyncOpenAI client manages its own connection pool
        custom_client = AsyncOpenAI(
            api_key=settings.LLM_API_KEY, base_url=settings.LLM_BASE_URL
        )

        # Wrapping the client into the framework's specific Model class
        model = OpenAIChatCompletionsModel(
            model=settings.LLM_MODEL_NAME, openai_client=custom_client
        )

        return model
