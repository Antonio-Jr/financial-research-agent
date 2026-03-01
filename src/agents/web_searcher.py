"""Web searcher agent definitions.

This module defines `WebSearcherAgent`, a small wrapper around the
project `BaseAgent` preconfigured to execute web research tasks. The
agent is set up with the research prompt, the web search tool and
deterministic model settings.
"""

from src.core.base_agent import BaseAgent
from src.prompts.web_searcher import RESEARCH_PROMPT
from src.tools.web_searcher import web_search
from agents import ModelSettings


class WebSearcherAgent(BaseAgent):
  """Agent that performs web research and returns search summaries.

  Defaults:
    - name: "Web Research Agent"
    - instructions: `RESEARCH_PROMPT`
    - tools: `[web_search]`
    - model_settings: deterministic (`temperature=0`) and requires tool usage
  """

  def __init__(self, **kwargs):
    kwargs.setdefault("name", "Web Research Agent")
    kwargs.setdefault("instructions", RESEARCH_PROMPT)
    kwargs.setdefault("tools", [web_search])
    kwargs.setdefault(
      "model_settings", ModelSettings(temperature=0, tool_choice="required")
    )

    super().__init__(**kwargs)