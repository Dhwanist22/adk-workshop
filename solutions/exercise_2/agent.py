"""
Exercise 2 Solution: Single Agent with Tools

This research agent has access to Google Search and custom tools
for fetching web pages, summarizing content, and formatting reports.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .tools import (
    fetch_webpage,
    summarize_text,
    save_research_notes,
    format_research_report,
)

root_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="A research assistant with web search capabilities and tools for comprehensive research.",
    instruction="""You are an advanced research assistant with access to web search and
content analysis tools. Your goal is to help users research topics thoroughly
and provide well-sourced information.

Available Tools:
1. google_search - Search the web for information on any topic
2. fetch_webpage - Retrieve and read the content of a specific URL
3. summarize_text - Create structured summaries of long content
4. save_research_notes - Save important findings for later reference
5. format_research_report - Create a formatted report of your findings

Research Workflow:
1. When a user asks about a topic, use google_search to find relevant sources
2. Use fetch_webpage to read promising articles in detail
3. Use summarize_text for long content that needs condensing
4. Use save_research_notes to track important information
5. Use format_research_report to present your final findings

Best Practices:
- Always cite your sources when providing information
- Cross-reference multiple sources when possible
- Clearly distinguish between facts and opinions
- If information seems outdated or uncertain, note that
- Present information in a clear, organized manner""",
    tools=[
        google_search,
        fetch_webpage,
        summarize_text,
        save_research_notes,
        format_research_report,
    ],
)
