"""Core wrappers for project agents.

This module provides a `BaseAgent` specialization that injects the
project-level LLM configuration before delegating to the underlying
agent implementation provided by the external library.
"""

from agents import Agent
from src.core.factory.llm_factory import InitLLM


class BaseAgent(Agent):
    """Agent wrapper that applies project LLM defaults.

    The wrapper ensures a model configuration is provided by using
    `InitLLM.configure()` when no explicit `model` keyword argument is
    passed. After preparing kwargs it defers construction to the
    upstream `Agent` class from the third-party library.
    """

    def __init__(self, **kwargs):
        """Initialize the agent, injecting a default model when missing.

        Args:
            **kwargs: Forwarded to the upstream `Agent` constructor. If
                the `model` key is absent a default is provided by the
                project's LLM factory.
        """
        if "model" not in kwargs:
            kwargs["model"] = InitLLM.configure()

        super().__init__(**kwargs)
