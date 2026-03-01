"""Report generator agent.

Provides an agent configured to produce structured `ReportData`
objects from research summaries using the project's report
generation instructions.
"""

from agents import Agent
from src.core.base_agent import BaseAgent
from src.models.report_data import ReportData
from src.prompts.report_generator import INSTRUCTIONS
from src.core.factory.llm_factory import InitLLM


class ReportGeneratorAgent(BaseAgent):
    """Agent that generates `ReportData` instances from summaries.

    The agent uses `INSTRUCTIONS` to guide the LLM output formatting and
    sets `output_type` to `ReportData` so the upstream runner can parse
    the result accordingly.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("name", "Writer Agent")
        kwargs.setdefault("instructions", INSTRUCTIONS)
        kwargs.setdefault("output_type", ReportData)

        super().__init__(**kwargs)



