from agents import Agent

from src.core.base_agent import BaseAgent
from src.models.search_planner import SearchPlan
from src.prompts.search_planner import PLANNER_PROMPT


class SearchPlannerAgent(BaseAgent):
  def __init__(self, **kwargs):
    kwargs.setdefault("name", "Search Planner Agent")
    kwargs.setdefault("instructions", PLANNER_PROMPT)
    kwargs.setdefault("output_type", SearchPlan)
    
    super().__init__(**kwargs)