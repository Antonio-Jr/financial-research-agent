from src.core.factory import llm_factory as mod


def test_llm_factory_exists():
    assert hasattr(mod, "InitLLM")
