from pydantic import ValidationError
import pytest
from src.models.report_data import ReportData


def test_report_data_valid():
    data = {
        "short_summary": "Summary",
        "markdown_report": "# Report",
        "follow_up_questions": ["Q1"]
    }
    rd = ReportData(**data)
    assert rd.short_summary == "Summary"
    assert rd.markdown_report == "# Report"
    assert rd.follow_up_questions == ["Q1"]


def test_report_data_defaults():
    rd = ReportData(short_summary="S", markdown_report="R")
    assert rd.follow_up_questions == []


def test_report_data_invalid():
    with pytest.raises(ValidationError):
        ReportData(short_summary="S") # Missing markdown_report
