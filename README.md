# Google Agent Development Kit (ADK) Workshop

Welcome to the hands-on workshop for building AI agents with Google's Agent Development Kit! In this workshop, you'll progressively build a Research Agent, starting from a simple single agent and evolving to a multi-agent hierarchical system.

## Workshop Overview

| Exercise | Description | Skills Learned |
|----------|-------------|----------------|
| **Exercise 1** | Simple Single Agent | ADK basics, Agent class, deployment |
| **Exercise 2** | Agent with Tools | Custom tools, Google Search, web scraping |
| **Exercise 3** | Multi-Agent System | Agent hierarchies, delegation, orchestration |

## Prerequisites

- Python 3.10+
- Google Cloud account with billing enabled
- Google API Key (from [AI Studio](https://aistudio.google.com/apikey)) or Vertex AI access
- Git

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd adk-workshop-q126

# Create your workshop branch
git checkout -b workshop/<your-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run Locally

```bash
# Start the ADK development server
adk web

# Or run with Python directly
python main.py
```

Open http://localhost:8080 to interact with your agent.

### 3. Deploy

```bash
# Push your branch to trigger deployment
git add .
git commit -m "My research agent"
git push -u origin workshop/<your-name>
```

Your agent will be deployed to a unique Cloud Run URL. Check the GitHub Actions output for your deployment URL.

---

## Exercise 1: Simple Single Agent

**Goal:** Create a basic research agent that can answer questions using its built-in knowledge.

### Instructions

1. Open `research_agent/agent.py`
2. Replace `root_agent = None` with an Agent definition:

```python
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
4. Cite your reasoning when making claims""",
)
```

### Test Your Agent

```bash
adk web
```

Try these prompts:
- "What is machine learning?"
- "Explain the difference between AI and ML"
- "How does a neural network work?"

### Key Concepts

- **Agent**: The main class for creating an AI agent
- **name**: Unique identifier for the agent
- **model**: The LLM to use (e.g., `gemini-2.0-flash`)
- **description**: Brief description of what the agent does
- **instruction**: System prompt that guides the agent's behavior

### Solution

See `solutions/exercise_1/agent.py` for the complete solution.

---

## Exercise 2: Agent with Tools

**Goal:** Extend your agent with tools for web search, content fetching, and report generation.

### Instructions

1. Create a new file `research_agent/tools.py` with custom tools
2. Update `research_agent/agent.py` to use the tools

### Step 1: Create Tools

Create `research_agent/tools.py`:

```python
import aiohttp
from bs4 import BeautifulSoup

async def fetch_webpage(url: str) -> dict:
    """
    Fetches the content of a webpage and extracts the main text.

    Args:
        url: The full URL of the webpage to fetch

    Returns:
        A dictionary with status and the page content or error message
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    return {"status": "error", "error_message": f"HTTP {response.status}"}

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                # Remove non-content elements
                for element in soup(["script", "style", "nav", "footer"]):
                    element.decompose()

                text = soup.get_text(separator="\n", strip=True)

                return {
                    "status": "success",
                    "content": text[:10000],  # Truncate long content
                    "title": soup.title.string if soup.title else "No title"
                }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def format_research_report(title: str, summary: str, key_findings: list[str], sources: list[str] = None) -> dict:
    """
    Formats research findings into a structured report.

    Args:
        title: The title of the research report
        summary: A brief summary of the research
        key_findings: A list of key findings
        sources: Optional list of source URLs

    Returns:
        A formatted research report
    """
    report = f"# {title}\n\n## Summary\n{summary}\n\n## Key Findings\n"
    for i, finding in enumerate(key_findings, 1):
        report += f"{i}. {finding}\n"

    if sources:
        report += "\n## Sources\n"
        for source in sources:
            report += f"- {source}\n"

    return {"status": "success", "report": report}
```

### Step 2: Update Agent

Update `research_agent/agent.py`:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

from .tools import fetch_webpage, format_research_report

root_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="A research assistant with web search and content analysis tools.",
    instruction="""You are an advanced research assistant with web search capabilities.

Available Tools:
1. google_search - Search the web for information
2. fetch_webpage - Retrieve content from a URL
3. format_research_report - Create formatted reports

Research Workflow:
1. Use google_search to find relevant sources
2. Use fetch_webpage to read promising articles
3. Use format_research_report to present findings

Always cite your sources and cross-reference information.""",
    tools=[google_search, fetch_webpage, format_research_report],
)
```

### Test Your Agent

```bash
adk web
```

Try these prompts:
- "Research the latest developments in quantum computing"
- "Find information about climate change solutions and create a report"
- "What are the top AI trends in 2025?"

### Key Concepts

- **Tools**: Functions that extend agent capabilities
- **google_search**: Built-in tool for web search
- **Custom tools**: Python functions with docstrings become tools automatically
- **Async tools**: Use `async def` for I/O-bound operations

### Solution

See `solutions/exercise_2/` for the complete solution.

---

## Exercise 3: Multi-Agent Hierarchy

**Goal:** Build a multi-agent system with specialized agents for search, summarization, and reporting.

### Architecture

```
research_orchestrator (root)
├── search_agent      - Web search and content retrieval
├── summarizer_agent  - Content analysis and summarization
└── report_agent      - Report formatting and presentation
```

### Instructions

1. Create specialized agents in `research_agent/agents/`
2. Create an orchestrator agent that coordinates them
3. Update the root agent to use the orchestrator

### Step 1: Create Agent Directory

```bash
mkdir -p research_agent/agents
touch research_agent/agents/__init__.py
```

### Step 2: Create Search Agent

Create `research_agent/agents/search_agent.py`:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search
# Import fetch_webpage from your tools.py

search_agent = Agent(
    name="search_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for web search and content retrieval.",
    instruction="""You are a search specialist. Find relevant information
and retrieve webpage content. Focus on authoritative sources.""",
    tools=[google_search],  # Add fetch_webpage too
)
```

### Step 3: Create Summarizer Agent

Create `research_agent/agents/summarizer_agent.py`:

```python
from google.adk.agents import Agent

summarizer_agent = Agent(
    name="summarizer_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for analyzing and summarizing content.",
    instruction="""You are a summarization specialist. Analyze content
and extract key insights. Be concise but comprehensive.""",
)
```

### Step 4: Create Report Agent

Create `research_agent/agents/report_agent.py`:

```python
from google.adk.agents import Agent

report_agent = Agent(
    name="report_agent",
    model="gemini-2.0-flash",
    description="Specialized agent for formatting research reports.",
    instruction="""You are a report formatting specialist. Create clear,
professional reports with proper structure and citations.""",
)
```

### Step 5: Create Orchestrator

Update `research_agent/agent.py`:

```python
from google.adk.agents import Agent

from .agents.search_agent import search_agent
from .agents.summarizer_agent import summarizer_agent
from .agents.report_agent import report_agent

root_agent = Agent(
    name="research_orchestrator",
    model="gemini-2.0-flash",
    description="Orchestrator that coordinates specialized research agents.",
    instruction="""You coordinate a team of specialized agents:

1. search_agent - Finds information on the web
2. summarizer_agent - Analyzes and summarizes content
3. report_agent - Formats findings into reports

Workflow:
1. Delegate search tasks to search_agent
2. Pass results to summarizer_agent for analysis
3. Send summaries to report_agent for formatting
4. Present the final report to the user

Keep the user informed of progress.""",
    sub_agents=[search_agent, summarizer_agent, report_agent],
)
```

### Test Your Multi-Agent System

```bash
adk web
```

Try these prompts:
- "Research the pros and cons of electric vehicles and create a comprehensive report"
- "Compare different cloud providers and their AI services"
- "Investigate recent breakthroughs in renewable energy"

### Key Concepts

- **sub_agents**: List of agents that this agent can delegate to
- **Delegation**: Parent agents can transfer control to sub-agents
- **Orchestration**: Coordinating multiple agents for complex tasks
- **Specialization**: Each agent focuses on what it does best

### Solution

See `solutions/exercise_3/` for the complete solution.

---

## Deployment

### Branch Naming Convention

Create branches with the pattern `workshop/<your-name>` to trigger automatic deployment:

```bash
git checkout -b workshop/john-doe
```

### GitHub Secrets Required

The repository needs these secrets configured:

| Secret | Description |
|--------|-------------|
| `GCP_PROJECT_ID` | Your Google Cloud project ID |
| `GCP_REGION` | Deployment region (default: us-central1) |
| `WIF_PROVIDER` | Workload Identity Federation provider |
| `WIF_SERVICE_ACCOUNT` | Service account for deployment |
| `GOOGLE_API_KEY` | (Optional) API key stored in Secret Manager |

### Manual Deployment

If you prefer manual deployment:

```bash
# Using ADK CLI
adk deploy cloud_run \
  --project=YOUR_PROJECT \
  --region=us-central1 \
  --with_ui \
  ./research_agent

# Using gcloud
gcloud run deploy research-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python GitHub](https://github.com/google/adk-python)
- [Google Cloud Run](https://cloud.google.com/run)
- [Gemini API](https://ai.google.dev/)

## Troubleshooting

### Agent returns `None`

Make sure your `agent.py` exports `root_agent` and it's not `None`.

### Tools not working

- Check that tool functions have proper docstrings
- Ensure async tools use `async def`
- Verify tool parameter types are correct

### Deployment fails

- Check GitHub Actions logs for details
- Verify all secrets are configured
- Ensure your branch name matches `workshop/*`

### API key errors

- Verify `GOOGLE_API_KEY` is set in `.env` for local development
- For Cloud Run, ensure the secret is created in Secret Manager

---

## Workshop Support

Having issues? Ask your workshop facilitator or check the solutions folder for reference implementations.
