from agents import function_tool
from langchain_community.tools import DuckDuckGoSearchRun

@function_tool
def web_search(query: str):
    """Stable DuckDuckGo wrapper via LangChain Community."""
    search = DuckDuckGoSearchRun()
    return search.run(query)