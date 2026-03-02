import pytest
import types
from src.services.tasks.search_planner import SearchPlannerTask
from src.models.research_context import ResearchContext
from src.models.search_planner import SearchPlan


@pytest.mark.asyncio
async def test_search_planner_task_execute(monkeypatch):
    # Mocking SearchPlannerRunner.run
    async def fake_run(query, max_sources=3):
        return SearchPlan(searches=[{"reason": "test", "query": "test query"}])

    monkeypatch.setattr("src.services.tasks.search_planner.SearchPlannerRunner", types.SimpleNamespace(run=fake_run))

    ctx = ResearchContext(query="test")
    task = SearchPlannerTask()

    msgs = []
    async for m in task.execute(ctx):
        msgs.append(m)

    assert any("Starting" in m for m in msgs)
    assert any("Planning created" in m for m in msgs)
    assert ctx.search_plan is not None
    assert len(ctx.search_plan.searches) == 1
