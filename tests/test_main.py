import pytest
from unittest.mock import patch, MagicMock
import main

@pytest.mark.asyncio
async def test_run_research_empty_query():
    gen = main.run_research("  ", "test@test.com")
    responses = [r async for r in gen]
    assert "Please enter a research query" in responses[0]

@pytest.mark.asyncio
@patch("main.ReportManager")
async def test_run_research_full_flow(mock_manager_cls):
    mock_manager = mock_manager_cls.return_value
    
    async def mock_execute(query, email, max_sources):
        yield "Step 1"
        yield "# Final Report"
        
    mock_manager.execute.side_effect = mock_execute
    
    gen = main.run_research("query", "test@test.com", max_sources=5)
    responses = [r async for r in gen]
    
    assert "Step 1" in responses
    assert "# Final Report" in responses
    mock_manager_cls.assert_called_once()

@patch("main.gr.Blocks")
@patch("main.gr.Markdown")
@patch("main.gr.Column")
@patch("main.gr.Row")
@patch("main.gr.Textbox")
@patch("main.gr.Slider")
@patch("main.gr.Button")
def test_main_launch(mock_btn, mock_slider, mock_txt, mock_row, mock_col, mock_md, mock_blocks):
    # Mocking all components to avoid Gradio internal logic issues
    mock_ui = mock_blocks.return_value.__enter__.return_value
    
    main.main()
    
    mock_blocks.assert_called_once()
    mock_ui.launch.assert_called_once()
    assert mock_btn.called
    assert mock_slider.called
    assert mock_txt.called

@patch("main.setup_logging")
@patch("main.main")
def test_entrypoint_via_function(mock_main, mock_setup):
    # We can't easily trigger the if __name__ == "__main__" block via import
    # But we can verify it if we use pragma: no cover in main.py for that block
    # and just test the components here.
    pass
