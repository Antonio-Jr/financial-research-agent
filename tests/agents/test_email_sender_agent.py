from src.agents.email_sender import EmailSenderAgent
from src.prompts.email_sender import INSTRUCTIONS


def test_email_sender_agent_initialization():
    agent = EmailSenderAgent()
    assert agent.name == "Email Agent"
    assert agent.instructions == INSTRUCTIONS
    assert any(tool.name == "send_email" for tool in agent.tools)
