"""Runners for parallel web searching.

This module implements `WebSearcherRunner`, a helper that executes a
`WebSearcherAgent` across a `SearchPlan` in parallel and aggregates
the results.
"""

import asyncio
import logging

from src.agents.web_searcher import WebSearcherAgent
from src.core.base_runner import BaseRunner
from src.models.search_planner import SearchPlan, SearchTask

logger = logging.getLogger(__name__)


class WebSearcherRunner(BaseRunner[WebSearcherAgent, str]):
    """Runner that performs parallel web searches using the agent.

    The `run` method accepts a `SearchPlan` and schedules concurrent
    searches for each `SearchTask` contained in the plan. The private
    `__search` coroutine formats the agent input for a single task and
    delegates execution to the generic `BaseRunner.execute` method.
    """

    agent_class = WebSearcherAgent

    @classmethod
    async def run(cls, search_plan: SearchPlan):
        """Execute searches in parallel and return aggregated results.

        Args:
            search_plan: A `SearchPlan` containing `SearchTask` items.

        Returns:
            A list of results returned by the agent for each search task.
        """
        logger.info("Performing Parallel Searching...")

        tasks = [
            asyncio.create_task(cls.__search(task)) for task in search_plan.searches
        ]

        results = await asyncio.gather(*tasks)
        logger.info("Searches finished.")

        return results

    @classmethod
    async def __search(cls, search_task: SearchTask):
        """Run a single search task through the agent.

        Args:
            search_task: `SearchTask` with `query` and `reason` attributes.

        Returns:
            Agent execution result for the given task.
        """
        input = f"Search term: {search_task.query}\nReason for searching: {search_task.reason}"
        return await cls.execute(input)
