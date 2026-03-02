"""High-level orchestration for report generation.

`ReportManager` is a small dependency-injection friendly orchestrator
that composes a `ResearchPipeline` with a pre-defined ordered list of
`BaseTask` instances. The manager is intentionally minimal: it
attaches a `ResearchContext` to the pipeline, registers the provided
tasks (in order) and streams progress messages produced by each task.

This module focuses on clarity for reviewers and consumers of the
project — the manager does not make implicit decisions about which
tasks to run (for example, it will not add an email-sending task
automatically based on the presence of an `email` argument). To enable
conditional execution, implement `should_run()` on individual tasks or
manage the `tasks` list before constructing `ReportManager`.

Usage example:

```py
from src.core.pipeline import ResearchPipeline
from src.services.tasks.search_planner import SearchPlannerTask
from src.services.tasks.web_searcher import WebSearcherTask
from src.services.tasks.report_generator import ReportGeneratorTask

pipeline = ResearchPipeline()
tasks = [SearchPlannerTask(), WebSearcherTask(), ReportGeneratorTask()]
manager = ReportManager(pipeline=pipeline, tasks=tasks)

async for update in manager.execute("my query"):
    print(update)
```
"""

from collections.abc import AsyncGenerator

from src.core.pipeline import ResearchPipeline
from src.models.research_context import ResearchContext
from src.services.tasks.base import BaseTask


class ReportManager:
    """Manager that orchestrates the research pipeline using DI.

    Construct this manager with a concrete `ResearchPipeline` and the
    sequence of `BaseTask` instances to execute. The instance method
    `execute` sets the pipeline context, registers the tasks and then
    streams progress messages produced by each task.
    """

    def __init__(self, pipeline: ResearchPipeline, tasks: list[BaseTask]) -> None:
        self.pipeline = pipeline
        self.tasks = tasks

    async def execute(self, query: str, email: str = "", max_sources: int = 3) -> AsyncGenerator[str, None]:
        """Run the configured pipeline and stream progress updates.

        This instance method creates a `ResearchContext` for the provided
        `query` and optional `email`, attaches it to the pipeline and
        registers the `tasks` that were supplied when the manager was
        constructed. The method yields progress messages produced by the
        tasks and finally the markdown report when available.

        Note: `ReportManager` does not implicitly add tasks based on
        the `email` argument. If you want an email to be sent include an
        `EmailSenderTask` instance in the `tasks` list when constructing
        the manager.

        Args:
            query: The user's research query.
            email: Optional recipient email address (stored in the
                context for tasks that need it).
            max_sources: Maximum number of sources to request from the
                planner.

        Yields:
            Progress messages (strings) from pipeline tasks and finally
            the markdown report when available.
        """
        context = ResearchContext(query=query, email=email, max_sources=max_sources)
        self.pipeline.set_context(context)

        for task in self.tasks:
            self.pipeline.add_task(task)

        async for update in self.pipeline.run():
            yield update

        if context.final_report:
            yield context.final_report.markdown_report
