import pytest
from unittest.mock import patch, MagicMock
from src.runners.web_searcher import WebSearcherRunner
from src.models.search_planner import SearchPlan, SearchTask

@pytest.mark.asyncio
async def test_web_searcher_runner_parallel_run():
    # Mock search plan with 2 searches
    plan = SearchPlan(searches=[
        SearchTask(query="query 1", reason="reason 1"),
        SearchTask(query="query 2", reason="reason 2")
    ])
    
    # Patch the execute method to avoid real agent calls
    with patch.object(WebSearcherRunner, "execute", new_callable=MagicMock) as mock_execute:
        # Mocking the async response
        async def mock_execute_side_effect(input_data):
            return f"Summary for {input_data}"
        
        mock_execute.side_effect = mock_execute_side_effect
        
        results = await WebSearcherRunner.run(plan)
        
        assert len(results) == 2
        assert "query 1" in results[0]
        assert "query 2" in results[1]
        assert mock_execute.call_count == 2
