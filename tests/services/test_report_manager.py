import pytest
from src.core.pipeline import ResearchPipeline
from src.models.report_data import ReportData
from src.services.report_manager import ReportManager
from src.services.tasks.base import BaseTask


class Task1(BaseTask):
    async def execute(self, context):
        context.query += " modified"
        yield "Step 1"


class Task2(BaseTask):
    async def execute(self, context):
        context.final_report = ReportData(short_summary="S", markdown_report="# R", follow_up_questions=[])
        yield "Step 2"


@pytest.mark.asyncio
async def test_report_manager_full_flow():
    pipeline = ResearchPipeline()
    manager = ReportManager(pipeline=pipeline, tasks=[Task1(), Task2()])

    msgs = []
    async for m in manager.execute("initial"):
        msgs.append(m)

    assert "Step 1" in msgs
    assert "Step 2" in msgs
    assert pipeline.context.query == "initial modified"
    assert pipeline.context.final_report is not None
    assert msgs[-1].startswith("#")


@pytest.mark.asyncio
async def test_report_manager_empty_tasks():
    pipeline = ResearchPipeline()
    manager = ReportManager(pipeline=pipeline, tasks=[])

    msgs = [m async for m in manager.execute("q")]

    assert msgs == []
    assert pipeline.context.final_report is None
