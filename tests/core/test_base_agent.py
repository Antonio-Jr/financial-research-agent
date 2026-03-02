from src.core import base_agent as mod


def test_base_agent_present():
    assert hasattr(mod, "BaseAgent")
