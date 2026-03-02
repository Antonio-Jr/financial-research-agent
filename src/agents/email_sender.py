"""Email sender agent.

This module exposes `EmailSenderAgent`, a small wrapper around
`BaseAgent` preconfigured to use the project's `send_email` tool and
the email prompt instructions.
"""

from src.core.base_agent import BaseAgent
from src.prompts.email_sender import INSTRUCTIONS
from src.tools.email_sender import send_email


class EmailSenderAgent(BaseAgent):
    """Agent responsible for sending emails using the project's tool.

    Defaults the agent `instructions` to the email prompt and exposes
    the `send_email` tool through the `tools` list.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("name", "Email Agent")
        kwargs.setdefault("instructions", INSTRUCTIONS)
        kwargs.setdefault("tools", [send_email])

        super().__init__(**kwargs)
