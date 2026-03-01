"""Base task abstractions for research pipeline tasks.

This module defines `BaseTask`, the abstract base class that all
pipeline tasks must implement. Implementations should provide an
`execute` coroutine or async generator that yields progress strings.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator


class BaseTask(ABC):
  """Abstract base for pipeline tasks.

  Concrete tasks must implement `execute(self, context)` and yield
  progress messages as an asynchronous generator of strings.
  """

  @abstractmethod
  def execute(self, context) -> AsyncGenerator[str, None]:
    """Execute the task using `context` and yield progress updates.

    Args:
      context: The pipeline's shared context object.

    Yields:
      Progress messages as strings.
    """
    pass