"""
Search Agent - Specialized agent for web search and content retrieval.

This agent is responsible for:
- Searching the web for relevant information
- Fetching and extracting content from web pages
- Returning raw research data to the orchestrator
"""

import aiohttp
from bs4 import BeautifulSoup
from google.adk.agents import Agent
from google.adk.tools import google_search


async def fetch_webpage(url: str) -> dict:
    """
    Fetches the content of a webpage and extracts the main text.

    Args:
        url: The full URL of the webpage to fetch

    Returns:
        A dictionary with the page content or an error message
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    return {
                        "status": "error",
                        "error_message": f"HTTP {response.status}"
                    }

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()

                text = soup.get_text(separator="\n", strip=True)

                if len(text) > 8000:
                    text = text[:8000] + "\n[Truncated...]"

                return {
                    "status": "success",
                    "content": text,
                    "title": soup.title.string if soup.title else "No title",
                    "url": url
                }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for web search and content retrieval. Use this agent to find information on the web and retrieve webpage content.",
    instruction="""You are a specialized search agent. Your job is to find relevant
information on the web for research queries.

Your capabilities:
1. google_search - Search the web for information
2. fetch_webpage - Retrieve content from specific URLs

When given a research query:
1. Perform targeted searches to find relevant sources
2. Fetch the most promising pages to get detailed content
3. Return the raw information you find - another agent will summarize it

Focus on finding high-quality, authoritative sources. Prefer:
- Official documentation and websites
- Academic or research sources
- Reputable news outlets
- Expert blogs and articles

Always include the source URLs with any information you provide.""",
    tools=[google_search, fetch_webpage],
)
