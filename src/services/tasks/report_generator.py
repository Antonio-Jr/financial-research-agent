"""Task that generates a final report from search summaries.

This task is implemented as an asynchronous generator that yields
progress messages during long-running operations.
"""

from typing import AsyncGenerator

from src.runners.report_generator import ReportGeneratorRunner
from src.models.research_context import ResearchContext
from src.services.tasks.base import BaseTask


class ReportGeneratorTask(BaseTask):
    """Task wrapper that generates and attaches a final report to context.

    The task reads `context.search_results` and, if present, invokes the
    `ReportGeneratorRunner` to produce the final report. Progress messages
    are yielded to the caller.
    """

    async def execute(self, context: ResearchContext) -> AsyncGenerator[str, None]:
        """Run the report generation flow.

        Args:
            context: ResearchContext containing `query` and
                `search_results` used to generate the report.

        Yields:
            Progress messages (strings) describing execution stages.
        """
        if not context.search_results:
            return

        yield "✍️ Generating the final report..."

        context.final_report = await ReportGeneratorRunner.run(
            user_query=context.query, search_summaries=context.search_results
        )

        yield "✅ Report generated successfully!"