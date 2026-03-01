from agents import Agent
from src.core.base_agent import BaseAgent
from src.models.report_data import ReportData
from src.prompts.report_generator import INSTRUCTIONS
from src.core.factory.llm_factory import InitLLM

class ReportGeneratorAgent(BaseAgent):
  def __init__(self, **kwargs):
    kwargs.setdefault("name", "Writer Agent")
    kwargs.setdefault("instructions", INSTRUCTIONS)
    kwargs.setdefault("output_type", ReportData)

    super().__init__(**kwargs)
    

    
  