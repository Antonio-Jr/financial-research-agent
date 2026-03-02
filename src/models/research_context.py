"""Pipeline context model used across research tasks.

`ResearchContext` centralizes shared state for the pipeline, validated
by Pydantic. It contains the original query, optional email, the
search plan, collected search summaries, and the final report object.
"""


from pydantic import BaseModel, Field

from src.models.report_data import ReportData
from src.models.search_planner import SearchPlan


class ResearchContext(BaseModel):
    """Shared pipeline state for research execution.

    Attributes:
        query: The original user query string.
        max_sources: Maximum number of sources requested from the planner.
        email: Optional recipient email address.
        search_plan: The `SearchPlan` produced by the planner task.
        search_results: List of text summaries collected from searches.
        final_report: Optional `ReportData` produced by the report task.
    """

    query: str
    max_sources: int = 3
    email: str | None = None
    search_plan: SearchPlan | None = None
    search_results: list[str] = Field(default_factory=list)
    final_report: ReportData | None = None

    class Config:
        arbitrary_types_allowed = True
