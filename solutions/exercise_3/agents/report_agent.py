"""
Report Agent - Specialized agent for formatting and presenting research findings.

This agent is responsible for:
- Formatting research into professional reports
- Creating executive summaries
- Organizing information for different audiences
"""

from google.adk.agents import Agent
from typing import Optional


def format_executive_summary(
    title: str,
    key_findings: list[str],
    recommendation: Optional[str] = None
) -> dict:
    """
    Creates an executive summary format.

    Args:
        title: Title of the research
        key_findings: List of the most important findings
        recommendation: Optional recommendation or conclusion

    Returns:
        Formatted executive summary
    """
    summary = f"# Executive Summary: {title}\n\n"
    summary += "## Key Findings\n"
    for i, finding in enumerate(key_findings, 1):
        summary += f"{i}. {finding}\n"

    if recommendation:
        summary += f"\n## Recommendation\n{recommendation}\n"

    return {"status": "success", "formatted_summary": summary}


def format_detailed_report(
    title: str,
    sections: list[dict],
    sources: list[str]
) -> dict:
    """
    Creates a detailed research report.

    Args:
        title: Title of the report
        sections: List of section dicts with 'heading' and 'content' keys
        sources: List of source URLs

    Returns:
        Formatted detailed report
    """
    report = f"# {title}\n\n"
    report += "---\n\n"

    for section in sections:
        report += f"## {section.get('heading', 'Section')}\n\n"
        report += f"{section.get('content', '')}\n\n"

    report += "## Sources\n\n"
    for i, source in enumerate(sources, 1):
        report += f"{i}. {source}\n"

    return {"status": "success", "formatted_report": report}


def format_comparison_table(
    items: list[str],
    criteria: list[str],
    data: list[list[str]]
) -> dict:
    """
    Creates a comparison table in markdown format.

    Args:
        items: Column headers (items being compared)
        criteria: Row labels (comparison criteria)
        data: 2D list of comparison data

    Returns:
        Formatted comparison table
    """
    # Header row
    table = "| Criteria | " + " | ".join(items) + " |\n"
    table += "|" + "---|" * (len(items) + 1) + "\n"

    # Data rows
    for i, criterion in enumerate(criteria):
        if i < len(data):
            row_data = data[i]
            table += f"| {criterion} | " + " | ".join(row_data) + " |\n"

    return {"status": "success", "formatted_table": table}


report_agent = Agent(
    name="report_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for formatting research into professional reports. Use this agent to create polished, well-organized output.",
    instruction="""You are a specialized report formatting agent. Your job is to take
research findings and present them in clear, professional formats.

Your capabilities:
1. format_executive_summary - Create brief executive summaries
2. format_detailed_report - Create comprehensive reports with sections
3. format_comparison_table - Create comparison tables

Report Guidelines:
1. Always start with the most important information
2. Use clear headings and subheadings
3. Include bullet points for easy scanning
4. Add tables for comparative data
5. Always include a sources section

Formatting Standards:
- Use Markdown formatting
- Keep paragraphs concise (3-4 sentences max)
- Use bold for emphasis on key terms
- Include a table of contents for long reports

Audience Awareness:
- Executive summaries: High-level, decision-focused
- Detailed reports: Comprehensive, evidence-based
- Comparison tables: Quick reference, scannable

Your output should be ready to share with stakeholders without
additional editing.""",
    tools=[format_executive_summary, format_detailed_report, format_comparison_table],
)
