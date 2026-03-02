import pytest
import types
from email_validator import EmailNotValidError

from src.models.report_data import ReportData
from src.models.research_context import ResearchContext
from src.services.tasks.email_sender import EmailSenderTask

@pytest.mark.asyncio
async def test_email_sender_task_should_run_scenarios():
    task = EmailSenderTask()
    
    # Valid case
    ctx_valid = ResearchContext(
        query="q", 
        email="test@example.com", 
        final_report=ReportData(short_summary="s", markdown_report="m", follow_up_questions=[])
    )
    assert task.should_run(ctx_valid) is True

    # Missing email
    ctx_no_email = ResearchContext(query="q", email=None, final_report=ctx_valid.final_report)
    assert task.should_run(ctx_no_email) is False

    # Missing report
    ctx_no_report = ResearchContext(query="q", email="test@example.com", final_report=None)
    assert task.should_run(ctx_no_report) is False

    # Invalid email format
    ctx_bad_email = ResearchContext(query="q", email="invalid-email", final_report=ctx_valid.final_report)
    assert task.should_run(ctx_bad_email) is False

    # None context
    assert task.should_run(None) is False

@pytest.mark.asyncio
async def test_email_sender_task_execute_delegates(monkeypatch):
    called = []

    async def fake_run(report, email=None):
        called.append((report, email))

    monkeypatch.setattr("src.services.tasks.email_sender.EmailSenderRunner", types.SimpleNamespace(run=fake_run))

    ctx = ResearchContext(
        query="q", 
        email="a@b.com", 
        final_report=ReportData(short_summary="s", markdown_report="m", follow_up_questions=[])
    )

    task = EmailSenderTask()
    async for _ in task.execute(ctx):
        pass

    assert len(called) == 1
    assert called[0][1] == "a@b.com"
