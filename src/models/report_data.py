"""Data models for generated reports.

This module defines `ReportData`, the structured output produced by the
report generation agent. Fields are annotated with types so downstream
components can rely on schema validation.
"""

from pydantic import BaseModel, Field


class ReportData(BaseModel):
    """Structured report data produced by the writer agent.

    Attributes:
      short_summary: A 2-3 sentence summary of the main findings.
      markdown_report: The final report in markdown format.
      follow_up_questions: Suggested follow-up research topics.
    """

    short_summary: str = Field(
        ..., description="A short 2-3 sentence summary of the findings"
    )
    markdown_report: str = Field(..., description="The final report in markdown format")
    follow_up_questions: list[str] = Field(
        default_factory=list, description="Suggested topics to research further"
    )
