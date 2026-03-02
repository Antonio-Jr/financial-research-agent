import pytest
from unittest.mock import patch, MagicMock
from src.runners.report_generator import ReportGeneratorRunner
from src.models.report_data import ReportData


@pytest.mark.asyncio
async def test_report_generator_runner_run():
    with patch("src.core.base_runner.Runner.run") as mock_run:
        expected_report = ReportData(short_summary="S", markdown_report="M", follow_up_questions=[])
        mock_result = MagicMock()
        mock_result.final_output = expected_report
        mock_run.return_value = mock_result
        
        result = await ReportGeneratorRunner.run(user_query="q", search_summaries=["s1"])
        
        assert result == expected_report
        mock_run.assert_called_once()
        args, _ = mock_run.call_args
        assert "Original query: q" in args[1]
