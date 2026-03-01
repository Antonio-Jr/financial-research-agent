"""Task that sends reports via email when a recipient is provided.

`EmailSenderTask` is a pipeline task that checks the research context
for a recipient email and a generated report, then delegates sending
to `EmailSenderRunner`.
"""

from typing import AsyncGenerator

from src.core.pipeline import ResearchPipeline
from src.models.research_context import ResearchContext
from src.runners.email_sender import EmailSenderRunner
from src.services.tasks.base import BaseTask


class EmailSenderTask(BaseTask):
  """Pipeline task responsible for sending the final report by email.

  The task yields an informational message when email sending is
  skipped (no recipient or no report) and otherwise invokes the
  `EmailSenderRunner` to perform the sending operation.
  """

  async def execute(self, context: ResearchContext) -> AsyncGenerator[str, None]:
    """Execute the email sending step using the provided context.

    Args:
      context: `ResearchContext` containing `email` and
        `final_report` attributes.

    Yields:
      Informational progress messages as strings.
    """
    if not context.email or not context.final_report:
      yield "ℹ️ Email skipped (no recipient or report generated)."
      return

    await EmailSenderRunner.run(context.final_report, email=context.email)

