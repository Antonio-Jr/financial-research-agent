import pytest
import types
from src.services.tasks.web_searcher import WebSearcherTask
from src.models.research_context import ResearchContext
from src.models.search_planner import SearchPlan


@pytest.mark.asyncio
async def test_web_searcher_task_execute(monkeypatch):
    # Mocking WebSearcherRunner.run
    async def fake_run(search_plan):
        return ["Summary 1", "Summary 2"]

    monkeypatch.setattr("src.services.tasks.web_searcher.WebSearcherRunner", types.SimpleNamespace(run=fake_run))

    ctx = ResearchContext(query="test", search_plan=SearchPlan(searches=[{"reason":"r", "query":"q"}]))
    task = WebSearcherTask()

    msgs = []
    async for m in task.execute(ctx):
        msgs.append(m)

    assert any("Searching for sources" in m for m in msgs)
    assert any("Collected 2" in m for m in msgs)
    assert ctx.search_results == ["Summary 1", "Summary 2"]


@pytest.mark.asyncio
async def test_web_searcher_task_missing_plan():
    ctx = ResearchContext(query="test", search_plan=None)
    task = WebSearcherTask()
    
    msgs = []
    async for m in task.execute(ctx):
        msgs.append(m)
        
    assert any("Search plan is missing" in m for m in msgs)
    assert ctx.search_results == []
