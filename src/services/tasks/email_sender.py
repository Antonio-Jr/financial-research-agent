"""Pipeline task that sends the final report by email when appropriate.

This task validates the recipient address and delegates the actual
sending operation to `EmailSenderRunner`. It is safe to include this
task in the pipeline unconditionally because `should_run` will opt out
when there is no recipient, the email is invalid, or there is no
generated report.

Invariants and typing notes:
- The pipeline is expected to call `should_run` before `execute`.
  `should_run` guarantees both `context.email` and `context.final_report`
  are present when `execute` runs.
- To help static analyzers, `execute` casts `context.final_report` to
  `ReportData` before delegating to the runner.

Operational note:
- Deliverability checks are disabled to avoid external network calls
  during validation. Ensure email provider credentials (e.g. SendGrid
  API key) and the configured sender address are available in the
  runtime environment so `EmailSenderRunner` can deliver messages.
"""

from collections.abc import AsyncGenerator
from typing import cast

from email_validator import EmailNotValidError, validate_email

from models.report_data import ReportData
from src.models.research_context import ResearchContext
from src.runners.email_sender import EmailSenderRunner
from src.services.tasks.base import BaseTask


class EmailSenderTask(BaseTask):
  """Pipeline task responsible for sending the final report by email.

  Behavior:
    - `should_run` performs a lightweight syntactic validation of
      `context.email` and returns False when the value is missing or
      invalid.
    - `execute` yields an informational message and returns early if
      there is no recipient or no report; otherwise it delegates to
      `EmailSenderRunner.run` which performs the actual send.
  """

  def should_run(self, context: ResearchContext) -> bool:
    """Return True when the task should attempt to send an email.

    This method only checks presence and syntactic validity of the
    email address. Deliverability checks are intentionally disabled.
    """
    if not context or not context.email or not context.final_report:
      return False

    try:
      validate_email(context.email, check_deliverability=False)
      return True
    except EmailNotValidError:
      return False


  async def execute(self, context: ResearchContext) -> AsyncGenerator[str, None]:
    """Run the email sending step using the provided `ResearchContext`.

    The method assumes the pipeline has already invoked `should_run` and
    that `context.final_report` is a `ReportData` instance. For the
    benefit of static type checkers we cast the value before calling
    the runner.

    Yields:
      Human-readable progress messages suitable for UI streaming.
    """
    yield "Stating Email Runner..."
    report = cast(ReportData, context.final_report)
    await EmailSenderRunner.run(report, email=context.email)

