from pydantic import BaseModel
from typing import List

class ReportData(BaseModel):
  """A short 2-3 sentence summary of the findings"""
  short_summary: str

  """The final report"""
  markdown_report: str

  follow_up_questions: List[str]
  """Suggested topics to research further"""