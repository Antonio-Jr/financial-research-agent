"""Typed runner helpers.

This module exposes a `BaseRunner` class intended as a thin typed
orchestration helper. Concrete runners should set `agent_class` to the
appropriate agent implementation and call `execute` to run the agent.
"""

from agents import Runner
from src.core.base_agent import BaseAgent


class BaseRunner[T: BaseAgent, R]:
    agent_class: type[T]

    @classmethod
    async def execute(cls, input_data: str, **agent_kwargs) -> R:
        """Instantiate the configured agent and run it asynchronously.

        Args:
          input_data: The input payload passed to the runner/agent.
          **agent_kwargs: Keyword arguments forwarded to the agent
            constructor.

        Returns:
          The final output produced by the runner, typed as `R`.
        """

        agent = cls.agent_class(**agent_kwargs)
        result = await Runner.run(agent, input_data)
        return result.final_output
