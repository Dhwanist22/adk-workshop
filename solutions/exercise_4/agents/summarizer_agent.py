"""
Summarizer Agent - Specialized agent for content analysis and summarization.

This agent is responsible for:
- Analyzing raw research content
- Extracting key points and insights
- Creating concise, structured summaries
"""

from google.adk.agents import Agent


def extract_key_points(text: str, max_points: int = 7) -> dict:
    """
    Prepares text for key point extraction.

    Args:
        text: The text to analyze
        max_points: Maximum number of key points to extract

    Returns:
        Instructions for extracting key points
    """
    if len(text) > 12000:
        text = text[:12000] + "\n[Truncated for analysis...]"

    return {
        "status": "success",
        "text": text,
        "instruction": f"Extract up to {max_points} key points from this text."
    }


def compare_sources(sources: list[dict]) -> dict:
    """
    Prepares multiple sources for comparison analysis.

    Args:
        sources: List of source dictionaries with 'content' and 'url' keys

    Returns:
        Instructions for comparing the sources
    """
    return {
        "status": "success",
        "source_count": len(sources),
        "instruction": "Compare these sources and identify: agreements, disagreements, and unique insights from each."
    }


def identify_gaps(summary: str, original_query: str) -> dict:
    """
    Identifies gaps in the research based on the original query.

    Args:
        summary: The current summary of findings
        original_query: The original research question

    Returns:
        Analysis of what might be missing
    """
    return {
        "status": "success",
        "summary": summary,
        "query": original_query,
        "instruction": "Identify any aspects of the original query that haven't been fully addressed."
    }


summarizer_agent = Agent(
    name="summarizer_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for analyzing and summarizing research content. Use this agent to condense information and extract key insights.",
    instruction="""You are a specialized summarization agent. Your job is to analyze
research content and create clear, structured summaries.

Your capabilities:
1. extract_key_points - Identify the most important points in text
2. compare_sources - Analyze multiple sources for consistency
3. identify_gaps - Find what's missing in the research

When summarizing content:
1. Focus on the most relevant and important information
2. Organize information logically by theme or topic
3. Preserve important details, statistics, and quotes
4. Note any contradictions between sources
5. Highlight areas of uncertainty or debate

Output Format:
- Use clear headings and bullet points
- Lead with the most important findings
- Include source attribution for key claims
- Note confidence levels when appropriate

Be concise but comprehensive. Aim to reduce content by 70-80% while
preserving all essential information.""",
    tools=[extract_key_points, compare_sources, identify_gaps],
)
