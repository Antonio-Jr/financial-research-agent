from typing import List

from src.core.base_runner import BaseRunner
from src.models.report_data import ReportData
from src.agents.report_generator import ReportGeneratorAgent


class ReportGeneratorRunner(BaseRunner[ReportGeneratorAgent, ReportData]):
  agent_class = ReportGeneratorAgent

  @classmethod
  async def run(cls, user_query: str, search_summaries: List[str]) -> ReportData:
    """Use the WriterAgent to compile a structured, markdown-based research report"""
    print("Thinking deeply about the report...")
    prompt_input = f"Original query: {user_query}\nSummarized search results: {search_summaries}"
    result = await cls.execute(prompt_input)
    print("Finished writing the report!")

    return result