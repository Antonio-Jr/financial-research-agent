"""Search planner agent.

Defines `SearchPlannerAgent`, which returns a `SearchPlan` describing
which sources and queries should be used for a given user query. When
no custom instructions are provided the module uses `PLANNER_PROMPT`
with a default maximum number of sources.
"""

from src.core.base_agent import BaseAgent
from src.models.search_planner import SearchPlan
from src.prompts.search_planner import PLANNER_PROMPT


class SearchPlannerAgent(BaseAgent):
    """Agent that creates a search plan for a user query.

    Defaults `output_type` to `SearchPlan` and fills `instructions`
    with the planner prompt (using `MAX_SOURCES=3`) when none are
    provided by the caller.
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("name", "Search Planner Agent")
        kwargs.setdefault("output_type", SearchPlan)

        if not kwargs.get("instructions"):
            kwargs["instructions"] = PLANNER_PROMPT.format(MAX_SOURCES=3)

        super().__init__(**kwargs)
