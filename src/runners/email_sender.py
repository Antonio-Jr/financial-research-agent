"""Runner to send reports via email using the EmailSenderAgent.

This module wraps `EmailSenderAgent` and provides a `run` coroutine
that formats the email payload and delegates sending to the
`BaseRunner.execute` helper.
"""

import logging

from src.agents.email_sender import EmailSenderAgent
from src.core.base_runner import BaseRunner
from src.models.report_data import ReportData

logger = logging.getLogger(__name__)


class EmailSenderRunner(BaseRunner[EmailSenderAgent, ReportData]):
    """Runner that formats an email message and sends it via agent.

    The `run` method accepts a `ReportData` instance and a recipient
    email address, composes a prompt input and uses the agent to send
    the message.
    """

    agent_class = EmailSenderAgent

    @classmethod
    async def run(cls, report: ReportData, email: str | None):
        """Send the formatted `report` to `email` using the agent.

        Args:
            report: `ReportData` instance containing `markdown_report`.
            email: Recipient email address or `None`.

        Returns:
            The result of the agent execution.
        """
        logger.info("Preparing email...")

        prompt_input = (
            f"RECIPIENT_EMAIL: {email}\n\n" f"REPORT_CONTENT: \n{report.markdown_report}"
        )

        result = await cls.execute(prompt_input)
        logger.info("Email sent successfully!")
        return result
