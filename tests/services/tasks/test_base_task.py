import pytest
from src.services.tasks.base import BaseTask
from src.models.research_context import ResearchContext

class ConcreteTask(BaseTask):
    async def execute(self, context):
        yield "Done"

@pytest.mark.asyncio
async def test_base_task_default_should_run():
    task = ConcreteTask()
    ctx = ResearchContext(query="test")
    assert task.should_run(ctx) is True
    
    # Call execute to cover the generator
    results = [m async for m in task.execute(ctx)]
    assert results == ["Done"]
