"""Web search tool integrations.

This module exposes `web_search`, a thin wrapper around the
LangChain Community `DuckDuckGoSearchRun` tool, decorated as a
project `function_tool` for use by agents.
"""

from langchain_community.tools import DuckDuckGoSearchRun

from agents import function_tool


@function_tool
def web_search(query: str):
    """Perform a web search for `query` using DuckDuckGo.

    Args:
        query: Search string passed to the external search tool.

    Returns:
        The raw search results produced by `DuckDuckGoSearchRun.run`.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)
