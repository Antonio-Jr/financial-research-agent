from src.agents.report_generator import ReportGeneratorAgent
from src.prompts.report_generator import INSTRUCTIONS
from src.models.report_data import ReportData


def test_report_generator_agent_initialization():
    agent = ReportGeneratorAgent()
    assert agent.name == "Writer Agent"
    assert agent.instructions == INSTRUCTIONS
    assert agent.output_type == ReportData
