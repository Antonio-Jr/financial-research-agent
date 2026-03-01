import asyncio
import logging
from src.core.base_runner import BaseRunner
from src.agents.web_searcher import WebSearcherAgent
from src.models.search_planner import SearchPlan, SearchTask

logger = logging.getLogger(__name__)

class WebSearcherRunner(BaseRunner[WebSearcherAgent, str]):
  agent_class = WebSearcherAgent

  @classmethod
  async def run(cls, search_plan: SearchPlan):
    logger.info("Performing Parallel Searching...")

    tasks = [
      asyncio.create_task(cls.__search(task))
      for task in search_plan.searches
    ]

    results = await asyncio.gather(*tasks)
    logger.info("Searches finished.")

    return results
  
  @classmethod
  async def __search(cls, search_task: SearchTask): 
    input = f"Search term: {search_task.query}\nReason for searching: {search_task.reason}"
    return await cls.execute(input)