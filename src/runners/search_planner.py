
"""Search planner runner.

This module exposes `SearchPlannerRunner`, which prepares planner
instructions and invokes the `SearchPlannerAgent` to produce a
`SearchPlan` for a given query.
"""

import logging

from src.agents.search_planner import SearchPlannerAgent
from src.core.base_runner import BaseRunner
from src.models.search_planner import SearchPlan
from src.prompts.search_planner import PLANNER_PROMPT

logger = logging.getLogger(__name__)


class SearchPlannerRunner(BaseRunner[SearchPlannerAgent, SearchPlan]):
  """Runner that builds a `SearchPlan` for a user query.

  The `run` method formats the planner prompt using `max_sources`
  and forwards `query` and `instructions` to the agent execution.
  """

  agent_class = SearchPlannerAgent

  @classmethod
  async def run(cls, query: str, max_sources: int):
    """Generate a structured search plan for `query`.

    Args:
      query: The user's research query string.
      max_sources: Maximum number of sources the planner should return.

    Returns:
      A `SearchPlan` instance produced by the agent.
    """
    logger.info("Planning for searches...")
    formatted_instructions = PLANNER_PROMPT.format(MAX_SOURCES=max_sources)

    result = await cls.execute(input_data=query, instructions=formatted_instructions)
    logger.info("Will perform %d searches", len(result.searches))

    return result
