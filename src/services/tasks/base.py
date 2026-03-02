"""Base task abstractions for research pipeline tasks.

This module defines `BaseTask`, the abstract base class that all
pipeline tasks must implement. Implementations should provide an
`execute` coroutine or async generator that yields progress strings.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from src.models.research_context import ResearchContext


class BaseTask(ABC):
    """Abstract base class for pipeline tasks.

    Implementations should provide an `execute(self, context)` method that
    may be an asynchronous generator yielding progress messages (strings).

    Optionally override `should_run(self, context)` to make task
    execution conditional on the pipeline context.
    """

    @abstractmethod
    def execute(self, context) -> AsyncGenerator[str, None]:
        """Run the task using the provided `context` and yield updates.

        Implementations may perform I/O-bound operations and yield human-
        readable progress strings that are forwarded by the pipeline.

        Args:
            context: Shared `ResearchContext` instance used across tasks.

        Yields:
            Progress messages as strings.
        """
        pass  # pragma: no cover

    def should_run(self, context: ResearchContext) -> bool:
        """Return True when the task should run for the given context.

        The default implementation always returns True. Subclasses can
        override this method to skip execution based on context state
        (for example, skip emailing when no recipient is configured).
        """
        return True
