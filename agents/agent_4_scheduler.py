from crewai import Agent
from langchain_community.chat_models import ChatOpenAI


def timeline_agent():
    timeline_agent = Agent(
        role="Sprint Planner",
        goal="Schedule stories using agile sprint logic and create Gantt-style calendars",
        backstory="Experienced in project timelines and task velocity estimation.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
