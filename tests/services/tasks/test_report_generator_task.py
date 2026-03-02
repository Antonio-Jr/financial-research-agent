import pytest
import types
from src.services.tasks.report_generator import ReportGeneratorTask
from src.models.research_context import ResearchContext
from src.models.report_data import ReportData


@pytest.mark.asyncio
async def test_report_generator_task_execute(monkeypatch):
    # Mocking ReportGeneratorRunner.run
    async def fake_run(user_query, search_summaries):
        return ReportData(short_summary="S", markdown_report="# R", follow_up_questions=[])

    monkeypatch.setattr("src.services.tasks.report_generator.ReportGeneratorRunner", types.SimpleNamespace(run=fake_run))

    ctx = ResearchContext(query="test", search_results=["result"])
    task = ReportGeneratorTask()

    msgs = []
    async for m in task.execute(ctx):
        msgs.append(m)

    assert any("Generating the final report" in m for m in msgs)
    assert any("successfully" in m for m in msgs)
    assert ctx.final_report is not None
    assert ctx.final_report.short_summary == "S"


@pytest.mark.asyncio
async def test_report_generator_task_missing_results(monkeypatch):
    ctx = ResearchContext(query="test", search_results=[])
    task = ReportGeneratorTask()
    
    msgs = [m async for m in task.execute(ctx)]
        
    assert len(msgs) == 0
    assert ctx.final_report is None


@pytest.mark.asyncio
async def test_report_generator_task_no_results():
    ctx = ResearchContext(query="test", search_results=[])
    task = ReportGeneratorTask()

    msgs = [m async for m in task.execute(ctx)]

    assert len(msgs) == 0
    assert ctx.final_report is None
