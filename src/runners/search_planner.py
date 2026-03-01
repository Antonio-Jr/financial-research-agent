
from src.core.base_runner import BaseRunner
from src.models.search_planner import SearchPlan
from src.agents.search_planner import SearchPlannerAgent


class SearchPlannerRunner(BaseRunner[SearchPlannerAgent, SearchPlan]):
  agent_class = SearchPlannerAgent

  @classmethod
  async def run(cls, query: str):
    """Use planner_agent to generate a structured list of web searches for a given research query."""
    print("Planning for searches...")
    result = await cls.execute(query)
    print(f"Will perform {len(result.searches)} searches")

    return result