from src.agents.web_searcher import WebSearcherAgent
from src.prompts.web_searcher import RESEARCH_PROMPT


def test_web_searcher_agent_initialization():
    agent = WebSearcherAgent()
    assert agent.name == "Web Research Agent"
    assert agent.instructions == RESEARCH_PROMPT
    assert any(tool.name == "web_search" for tool in agent.tools)
