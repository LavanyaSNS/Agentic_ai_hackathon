from crewai import Agent
from langchain_community.chat_models import ChatOpenAI



def recovery_agent():
    recovery_agent = Agent(
        role="Timeline Recovery Specialist",
        goal="Adjust schedules automatically when delays are detected",
        backstory="Knows how to reallocate work and shift sprints efficiently.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
