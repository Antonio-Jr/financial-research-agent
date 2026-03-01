# from agents import Agent, ModelSettings, Runner
# from src.core.factory.llm_factory import InitLLM
# from src.tools.web_searcher import web_search
# from src.prompts.web_searcher import RESEARCH_PROMPT

# class WebSearcherAgent:
#   @staticmethod
#   def get() -> Agent:
#     web_search_agent = Agent(
#       name="Web Research Agent",
#       instructions=RESEARCH_PROMPT,
#       tools=[web_search],
#       model=InitLLM.configure(),
#       model_settings=ModelSettings(
#         temperature=0,
#         # tool_choice="required" is excellent for forcing action
#          tool_choice="required"
#       )
#   )

#     return web_search_agent

# # search = "Best performing index funds in the US market in current quarter"
# # result = await Runner.run(web_search_agent, search)

from src.core.base_agent import BaseAgent
from src.prompts.web_searcher import RESEARCH_PROMPT
from src.tools.web_searcher import web_search
from agents import ModelSettings

class WebSearcherAgent(BaseAgent):
  def __init__(self, **kwargs):
    kwargs.setdefault("name", "Web Research Agent")
    kwargs.setdefault("instructions", RESEARCH_PROMPT)
    kwargs.setdefault("tools", [web_search])
    kwargs.setdefault("model_settings", ModelSettings(temperature=0, tool_choice="required"))

    super().__init__(**kwargs)