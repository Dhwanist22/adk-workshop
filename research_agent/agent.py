"""
ADK Workshop - Research Agent

This is your starting point for the workshop exercises.
Follow the instructions in the README to progressively build
your Research Agent from a simple single agent to a full
multi-agent system.

Current Exercise: 1 (Simple Single Agent)
"""

from google.adk.agents import Agent

root_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="A research assistant that helps users find and understand information.",
    instruction="""You are a helpful research assistant. Your goal is to help users
find information and answer their questions clearly and accurately.

When responding to questions:
1. Provide clear, well-structured answers
2. If you're not sure about something, say so
3. Break down complex topics into understandable parts

You're currently running as a test deployment. Say hello and confirm you're working!""",
)
