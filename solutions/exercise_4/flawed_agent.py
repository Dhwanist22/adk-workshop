"""
Exercise 4: Flawed Agent for Evaluation Demo

This orchestrator has intentional issues in its instruction prompt:
1. Skips the summarizer_agent, going directly from search to report
2. Doesn't verify information quality before reporting
3. Lacks explicit workflow steps

Use this agent to demonstrate how evaluation catches these issues.
"""

from google.adk.agents import Agent

from .agents import search_agent, summarizer_agent, report_agent


root_agent = Agent(
    name="research_orchestrator",
    model="gemini-2.0-flash",
    description="An orchestrator agent that coordinates sub-agents to perform research.",
    instruction="""You are a research assistant. You have access to some helper agents.

Your helpers:
- search_agent: Can search the web
- summarizer_agent: Can summarize content
- report_agent: Can format reports

When a user asks you to research something, use search_agent to find information,
then use report_agent to format the results. Try to be helpful and give good answers.

If the user wants a report, make sure it looks nice.""",
    sub_agents=[search_agent, summarizer_agent, report_agent],
)
