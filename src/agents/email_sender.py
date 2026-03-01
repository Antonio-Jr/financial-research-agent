
from src.core.base_agent import BaseAgent
from src.prompts.email_sender import INSTRUCTIONS
from src.tools.email_sender import send_email


class EmailSenderAgent(BaseAgent):
  def __init__(self, **kwargs):
    kwargs.setdefault("name", "Email Agent")
    kwargs.setdefault("instructions", INSTRUCTIONS)
    kwargs.setdefault("tools", [send_email])

    super().__init__(**kwargs)
