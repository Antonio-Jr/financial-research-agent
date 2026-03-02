import pytest
from unittest.mock import patch, MagicMock
from src.runners.search_planner import SearchPlannerRunner
from src.models.search_planner import SearchPlan


@pytest.mark.asyncio
async def test_search_planner_runner_run():
    with patch("src.core.base_runner.Runner.run") as mock_run:
        expected_plan = SearchPlan(searches=[])
        mock_result = MagicMock()
        mock_result.final_output = expected_plan
        mock_run.return_value = mock_result
        
        result = await SearchPlannerRunner.run(query="q", max_sources=2)
        
        assert result == expected_plan
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        # args[1] is input_data
        assert args[1] == "q"
        # The agent is instantiated with the instructions
        # But we mocked Runner.run, so we need to check how the agent was created if we want to be precise.
        # However, looking at BaseRunner.execute:
        # agent = cls.agent_class(**agent_kwargs)
        # result = await Runner.run(agent, input_data)
        # We can check that Runner.run was called with an agent that has the right instructions.
        agent = args[0]
        assert "identify 2 distinct search terms" in agent.instructions
