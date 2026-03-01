"""Lightweight research pipeline for executing ordered tasks.

The pipeline holds a shared `ResearchContext` and a sequence of
`BaseTask` instances. Tasks are executed sequentially and may yield
progress updates which are forwarded by the pipeline's async
generator.
"""

from typing import AsyncGenerator, List, Self
from src.services.tasks.base import BaseTask
from src.models.research_context import ResearchContext


class ResearchPipeline:
    """Container that runs pipeline tasks against a shared context.

    Usage example:
        pipeline = ResearchPipeline().set_context(context)
        pipeline.add_task(SearchPlannerTask())
        async for msg in pipeline.run():
            print(msg)
    """

    def __init__(self) -> None:
        """Create an empty pipeline without a context or tasks.

        The `context` must be set via `set_context` before calling
        `run`.
        """
        self.tasks: List[BaseTask] = []
        self.context: ResearchContext

    def set_context(self, context: ResearchContext) -> Self:
        """Attach a shared `ResearchContext` to the pipeline.

        Returns:
            The pipeline instance to allow fluent chaining.
        """
        self.context = context
        return self

    def add_task(self, task: BaseTask) -> Self:
        """Append a `BaseTask` to the pipeline and return self.

        Tasks are executed in the order they are added.
        """
        self.tasks.append(task)
        return self

    async def run(self) -> AsyncGenerator[str, None]:
        """Execute all tasks sequentially, yielding progress messages.

        Raises:
            ValueError: If no context has been set prior to running.
        """
        if not hasattr(self, "context") or self.context is None:
            raise ValueError("Context must be set before running the pipeline.")

        for task in self.tasks:
            async for update in task.execute(self.context):
                yield update
    