from crewai import Agent
from langchain_community.chat_models import ChatOpenAI


def tracker_agent():
    tracker_agent = Agent(
        role="Task Monitor",
        goal="Track status of tasks and identify blockers using developer inputs",
        backstory="Tracks developer check-ins and GitHub commits to forecast delivery delays.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
