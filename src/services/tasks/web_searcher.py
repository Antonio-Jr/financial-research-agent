"""Task that executes parallel web searches according to a plan.

`WebSearcherTask` runs the `WebSearcherRunner` for the plan contained
in the pipeline context and stores the collected summaries back into
the context. Progress messages are yielded during execution.
"""

from collections.abc import AsyncGenerator

from src.models.research_context import ResearchContext
from src.runners.web_searcher import WebSearcherRunner
from src.services.tasks.base import BaseTask


class WebSearcherTask(BaseTask):
    """Pipeline task that performs web searches in parallel.

    The task expects `context.search_plan` to be present and will set
    `context.search_results` with the returned summaries.
    """

    async def execute(self, context: ResearchContext) -> AsyncGenerator[str, None]:
        """Run the web searches defined in `context.search_plan`.

        Args:
           context: Pipeline context containing `search_plan`.

        Yields:
           Progress messages as strings.
        """
        if not context.search_plan:
            yield "Search plan is missing..."
            return

        yield "🌐 Searching for sources in parallel"
        context.search_results = await WebSearcherRunner.run(search_plan=context.search_plan)
        yield f"✅ Collected {len(context.search_results)} summaries from sources."
