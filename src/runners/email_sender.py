from typing import Union
import logging
from src.core.base_runner import BaseRunner
from src.models.report_data import ReportData
from src.agents.email_sender import EmailSenderAgent


logger = logging.getLogger(__name__)


class EmailSenderRunner(BaseRunner[EmailSenderAgent, ReportData]):
  agent_class = EmailSenderAgent

  @classmethod
  async def run(cls, report: ReportData, email: Union[str, None]):
    """Use the EmailAgent to send the formatted report via HTML email."""
    logger.info("Preparing email...")

    prompt_input = (
      f"RECIPIENT_EMAIL: {email}\n\n"
      f"REPORT_CONTENT: \n{report.markdown_report}"
    )

    result = await cls.execute(prompt_input)
    logger.info("Email sent successfully!")
    return result