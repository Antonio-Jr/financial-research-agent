
import logging

from src.prompts.search_planner import PLANNER_PROMPT
from src.core.base_runner import BaseRunner
from src.models.search_planner import SearchPlan
from src.agents.search_planner import SearchPlannerAgent


logger = logging.getLogger(__name__)


class SearchPlannerRunner(BaseRunner[SearchPlannerAgent, SearchPlan]):
  agent_class = SearchPlannerAgent

  @classmethod
  async def run(cls, query: str, max_sources: int):
    """Use planner_agent to generate a structured list of web searches for a given research query."""
    logger.info("Planning for searches...")
    formatted_instructions = PLANNER_PROMPT.format(MAX_SOURCES=max_sources)

    result = await cls.execute(input_data=query, instructions=formatted_instructions)
    logger.info("Will perform %d searches", len(result.searches))

    return result