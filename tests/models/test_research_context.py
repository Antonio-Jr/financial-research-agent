from src.models.research_context import ResearchContext


def test_research_context_defaults():
    ctx = ResearchContext(query="x")
    assert ctx.query == "x"
    assert ctx.max_sources == 3
