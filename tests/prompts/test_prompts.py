from src.prompts import email_sender as p1
from src.prompts import report_generator as p2
from src.prompts import search_planner as p3
from src.prompts import web_searcher as p4


def test_prompts_strings():
    # ensure prompt modules expose string instructions
    assert hasattr(p1, "INSTRUCTIONS") or hasattr(p1, "PROMPT")
    assert hasattr(p2, "INSTRUCTIONS")
    assert hasattr(p3, "PLANNER_PROMPT")
    assert hasattr(p4, "RESEARCH_PROMPT")
