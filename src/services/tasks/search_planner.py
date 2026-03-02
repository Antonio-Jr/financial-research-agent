"""Pipeline task that produces a search plan for a query.

`SearchPlannerTask` invokes the `SearchPlannerRunner` to obtain a
`SearchPlan` for the provided `context` and yields progress messages
while executing.
"""

from collections.abc import AsyncGenerator

from src.runners.search_planner import SearchPlannerRunner
from src.services.tasks.base import BaseTask


class SearchPlannerTask(BaseTask):
    """Task that creates and attaches a `SearchPlan` to the context.

    The task yields a starting message, requests a search plan from the
    planner runner and then yields a completion message including the
    number of planned searches.
    """

    async def execute(self, context) -> AsyncGenerator[str, None]:
        """Generate a search plan and attach it to `context`.

        Args:
            context: Pipeline context containing `query` and
                `max_sources`.

        Yields:
            Progress messages as strings.
        """
        yield "🔍 Starting the planning phase..."

        context.search_plan = await SearchPlannerRunner.run(context.query, max_sources=context.max_sources)

        yield f"✅ Planning created with com {len(context.search_plan.searches)} searches."
