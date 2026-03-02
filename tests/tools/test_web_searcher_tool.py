import pytest
import importlib
from unittest.mock import patch

# Patch function_tool before importing the tool
with patch("agents.function_tool", lambda x: x):
    import src.tools.web_searcher
    importlib.reload(src.tools.web_searcher)
    from src.tools.web_searcher import web_search

@patch("src.tools.web_searcher.DuckDuckGoSearchRun")
def test_web_search_calls_duckduckgo(mock_ddg):
    mock_instance = mock_ddg.return_value
    mock_instance.run.return_value = "Search Results"
    
    result = web_search(query="test query")
    
    assert result == "Search Results"
    mock_instance.run.assert_called_once_with("test query")
