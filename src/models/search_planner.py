"""Models describing planner output: search tasks and plans.

`SearchTask` represents a single planned search and its rationale.
`SearchPlan` aggregates multiple `SearchTask` items returned by the
search planner agent.
"""


from pydantic import BaseModel, Field


class SearchTask(BaseModel):
  """A single search task produced by the planner.

  Attributes:
    reason: Explanation why this search is relevant.
    query: The web search query string to run.
  """

  reason: str = Field(..., description="Why this particular search matters")
  query: str = Field(..., description="The actual web search string")


class SearchPlan(BaseModel):
  """Collection of planned `SearchTask` instances.

  Attributes:
    searches: List of `SearchTask` items.
  """

  searches: list[SearchTask]
