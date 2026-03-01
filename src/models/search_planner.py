from pydantic import BaseModel

# Define structured output for each search time
class SearchTask(BaseModel):
  reason: str # Why this particular search matters
  query: str  # The actual web search string

# The full output schema from the planner
class SearchPlan(BaseModel):
  searches: list[SearchTask]
