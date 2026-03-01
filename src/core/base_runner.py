from typing import Type
from agents import Runner
from src.core.base_agent import BaseAgent

class BaseRunner[T: BaseAgent, R]:
  agent_class: Type[T]

  @classmethod
  async def execute(cls, input_data: str, **agent_kwargs) -> R:
    """
    Orchestrate an agent execution with typed form.
    Allows to override any parameter from agent during the execution time.
    """

    # Instantiate a specific agent (See agents in src.agents)
    agent = cls.agent_class(**agent_kwargs)

    # Calls the original runner lib
    result = await Runner.run(agent, input_data)

    # Returns the final output casted to R Type (Generics)
    return result.final_output