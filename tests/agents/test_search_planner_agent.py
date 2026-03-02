from src.agents.search_planner import SearchPlannerAgent
from src.prompts.search_planner import PLANNER_PROMPT
from src.models.search_planner import SearchPlan


def test_search_planner_agent_initialization():
    agent = SearchPlannerAgent()
    assert agent.name == "Search Planner Agent"
    assert agent.instructions == PLANNER_PROMPT.format(MAX_SOURCES=3)
    assert agent.output_type == SearchPlan
