from src.models.search_planner import SearchPlan


def test_search_plan_model():
    sp = SearchPlan(searches=[{"reason": "a", "query": "s"}])
    assert hasattr(sp, "searches")
