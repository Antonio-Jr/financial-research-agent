"""High-level orchestration for report generation.

`ReportManager` exposes a simple static `execute` coroutine that builds
and runs the research pipeline for a given `query`. It yields progress
updates produced by pipeline tasks and finally yields the markdown
report when available.
"""

from src.services.tasks.report_generator import ReportGeneratorTask
from src.services.tasks.web_searcher import WebSearcherTask
from src.services.tasks.email_sender import EmailSenderTask
from src.models.research_context import ResearchContext
from src.services.tasks.search_planner import SearchPlannerTask
from src.core.pipeline import ResearchPipeline


class ReportManager:
    """Manager that orchestrates the research pipeline.

    The static `execute` coroutine builds a `ResearchPipeline` with the
    necessary tasks (planner, web searcher, report generator) and
    optionally the email sender. It yields progress messages from the
    pipeline and finally the generated report content.
    """

    @staticmethod
    async def execute(query: str, email: str = "", max_sources: int = 3):
        """Run the research pipeline and stream progress updates.

        Args:
            query: The user's research query.
            email: Optional recipient email address; when provided the
                pipeline will include the email sending task.
            max_sources: Maximum number of sources to request from the
                planner.

        Yields:
            Progress messages (strings) produced by pipeline tasks and
            finally the markdown report string when generation completes.
        """
        context = ResearchContext(
          query=query, email=email, max_sources=max_sources)
        pipeline = (
            ResearchPipeline()
            .set_context(context)
            .add_task(SearchPlannerTask())
            .add_task(WebSearcherTask())
            .add_task(ReportGeneratorTask())
        )

        if email:
            pipeline.add_task(EmailSenderTask())

        async for update in pipeline.run():
            yield update

        if context.final_report:
            yield context.final_report.markdown_report