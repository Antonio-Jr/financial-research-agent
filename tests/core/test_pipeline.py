import pytest
from src.core.pipeline import ResearchPipeline
from src.models.research_context import ResearchContext
from src.services.tasks.base import BaseTask


class MockTask(BaseTask):
    def __init__(self, name, should=True):
        self.name = name
        self.should = should
        self.executed = False

    def should_run(self, context):
        return self.should

    async def execute(self, context):
        self.executed = True
        yield f"Executed {self.name}"


@pytest.mark.parametrize("task_names", [
    (["T1", "T2"]),
    (["T1"]),
    ([]),
])
@pytest.mark.asyncio
async def test_pipeline_execution_sequence(task_names):
    p = ResearchPipeline()
    p.set_context(ResearchContext(query="q"))
    tasks = [MockTask(name) for name in task_names]
    for t in tasks:
        p.add_task(t)

    msgs = []
    async for m in p.run():
        msgs.append(m)

    assert msgs == [f"Executed {name}" for name in task_names]
    assert all(t.executed for t in tasks)


@pytest.mark.asyncio
async def test_pipeline_skipping_logic():
    p = ResearchPipeline()
    p.set_context(ResearchContext(query="q"))
    t1 = MockTask("T1", should=False)
    t2 = MockTask("T2", should=True)
    p.add_task(t1).add_task(t2)

    msgs = []
    async for m in p.run():
        msgs.append(m)

    assert msgs == ["Executed T2"]
    assert not t1.executed
    assert t2.executed


@pytest.mark.asyncio
async def test_pipeline_missing_context():
    p = ResearchPipeline()
    # No context set
    with pytest.raises(ValueError, match="Context must be set"):
        results = [m async for m in p.run()]
