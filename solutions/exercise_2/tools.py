"""
Exercise 2: Custom Tools for the Research Agent

This module contains custom tools that extend the agent's capabilities
for web research tasks.
"""

import aiohttp
from bs4 import BeautifulSoup
from typing import Optional


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


def summarize_text(text: str, max_points: int = 5) -> dict:
    """
    Creates a structured summary request for a given text.

    Use this tool when you have a large amount of text and need to
    create a concise summary with key points.

    Args:
        text: The text content to summarize
        max_points: Maximum number of key points to extract (default: 5)

    Returns:
        A dictionary with the text prepared for summarization
    """
    if not text or len(text.strip()) == 0:
        return {
            "status": "error",
            "error_message": "No text provided to summarize"
        }

    # Truncate very long text
    if len(text) > 15000:
        text = text[:15000] + "\n\n[Text truncated for summarization...]"

    return {
        "status": "success",
        "text_to_summarize": text,
        "instructions": f"Please summarize this text into {max_points} or fewer key points."
    }


def save_research_notes(topic: str, notes: str) -> dict:
    """
    Saves research notes for a given topic to the session state.

    Use this tool to save important findings during research so they
    can be referenced later in the conversation.

    Args:
        topic: The topic or title for these notes
        notes: The research notes to save

    Returns:
        Confirmation that notes were saved
    """
    return {
        "status": "success",
        "message": f"Research notes saved for topic: {topic}",
        "topic": topic,
        "notes_length": len(notes),
        "preview": notes[:200] + "..." if len(notes) > 200 else notes
    }


def format_research_report(
    title: str,
    summary: str,
    key_findings: list[str],
    sources: Optional[list[str]] = None
) -> dict:
    """
    Formats research findings into a structured report.

    Use this tool when you've completed research and want to present
    the findings in a clean, organized format.

    Args:
        title: The title of the research report
        summary: A brief summary of the research
        key_findings: A list of key findings from the research
        sources: Optional list of source URLs used in the research

    Returns:
        A formatted research report as a dictionary
    """
    report = f"""
# {title}

## Summary
{summary}

## Key Findings
"""
    for i, finding in enumerate(key_findings, 1):
        report += f"{i}. {finding}\n"

    if sources:
        report += "\n## Sources\n"
        for source in sources:
            report += f"- {source}\n"

    return {
        "status": "success",
        "report": report,
        "findings_count": len(key_findings),
        "has_sources": bool(sources)
    }
