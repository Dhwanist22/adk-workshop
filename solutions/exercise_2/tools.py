"""
Exercise 2: Custom Tools for the Research Agent

This module contains a custom tool that extends the agent's capabilities
for fetching and reading web pages.
"""

import aiohttp
from bs4 import BeautifulSoup


async def fetch_webpage(url: str) -> dict:
    """
    Fetches the content of a webpage and extracts the main text.

    Use this tool when you need to read the content of a specific webpage
    that the user has provided or that you found through search.

    Args:
        url: The full URL of the webpage to fetch (must include http:// or https://)

    Returns:
        A dictionary with status and either the page content or an error message
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    return {
                        "status": "error",
                        "error_message": f"Failed to fetch URL. HTTP status: {response.status}"
                    }

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Remove script and style elements
                for element in soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()

                # Get text content
                text = soup.get_text(separator="\n", strip=True)

                # Truncate if too long
                if len(text) > 10000:
                    text = text[:10000] + "\n\n[Content truncated...]"

                return {
                    "status": "success",
                    "content": text,
                    "title": soup.title.string if soup.title else "No title"
                }

    except aiohttp.ClientError as e:
        return {
            "status": "error",
            "error_message": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching webpage: {str(e)}"
        }
