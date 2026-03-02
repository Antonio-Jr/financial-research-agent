import pytest
from unittest.mock import patch, MagicMock
from src.runners.email_sender import EmailSenderRunner
from src.models.report_data import ReportData


@pytest.mark.asyncio
async def test_email_sender_runner_run():
    with patch("src.core.base_runner.Runner.run") as mock_run:
        mock_result = MagicMock()
        mock_result.final_output = "Email Sent"
        mock_run.return_value = mock_result
        
        report = ReportData(short_summary="s", markdown_report="m", follow_up_questions=[])
        result = await EmailSenderRunner.run(report=report, email="test@example.com")
        
        assert result == "Email Sent"
        mock_run.assert_called_once()
