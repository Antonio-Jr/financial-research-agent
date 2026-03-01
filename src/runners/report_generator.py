"""Runner that generates structured reports using the report agent.

Provides a thin wrapper to prepare the prompt for the `ReportGeneratorAgent`
and return the resulting `ReportData`.
"""

from typing import List
import logging

from src.core.base_runner import BaseRunner
from src.models.report_data import ReportData
from src.agents.report_generator import ReportGeneratorAgent

logger = logging.getLogger(__name__)


class ReportGeneratorRunner(BaseRunner[ReportGeneratorAgent, ReportData]):
  """Runner that composes agent input and returns a `ReportData`.

  The `run` method formats a prompt containing the original query and
  a list of summarized search results, then delegates to
  `BaseRunner.execute` to obtain the final `ReportData`.
  """

  agent_class = ReportGeneratorAgent

  @classmethod
  async def run(cls, user_query: str, search_summaries: List[str]) -> ReportData:
    """Generate a report from the user query and search summaries.

    Args:
      user_query: The original user query string.
      search_summaries: A list of short summaries from web searches.

    Returns:
      A `ReportData` instance containing the generated report.
    """
    logger.info("Thinking deeply about the report...")
    prompt_input = f"Original query: {user_query}\nSummarized search results: {search_summaries}"
    result = await cls.execute(prompt_input)
    logger.info("Finished writing the report!")

    return result