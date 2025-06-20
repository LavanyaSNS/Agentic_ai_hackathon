from crewai import Agent
from langchain_community.chat_models import ChatOpenAI

def assignment_agent():
    assignment_agent = Agent(
        role="Team Skill Mapper",
        goal="Map user stories to team members based on skill, performance and bandwidth",
        backstory="Understands team structures and developer profiles to allocate tasks effectively.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
