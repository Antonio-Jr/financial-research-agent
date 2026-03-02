"""Lightweight research pipeline for executing ordered tasks.

This module provides `ResearchPipeline`, a minimal orchestrator that
runs an ordered list of `BaseTask` instances against a shared
`ResearchContext`. Tasks are executed sequentially and may yield
progress updates which are forwarded by the pipeline's asynchronous
generator. Tasks may opt out of execution by implementing
`BaseTask.should_run(context) -> bool`; the pipeline will log and skip
tasks when the condition is not satisfied.
"""

import logging
from collections.abc import AsyncGenerator
from typing import Self

from src.models.research_context import ResearchContext
from src.services.tasks.base import BaseTask

logger = logging.getLogger(__name__)


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
        self.tasks: list[BaseTask] = []
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
            # Allow tasks to opt out of execution based on the current
            # context. When `should_run` returns False the pipeline will
            # log the decision and continue to the next task.
            if not task.should_run(self.context):
                logger.info(
                    "Task %s skipped (condition not satisfied).",
                    task.__class__.__name__,
                )
                continue

            async for update in task.execute(self.context):
                yield update
