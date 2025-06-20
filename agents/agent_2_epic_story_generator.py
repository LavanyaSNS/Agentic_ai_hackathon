from crewai import Agent
from langchain_community.chat_models import ChatOpenAI
def story_agent():
    story_agent = Agent(
        role="Agile Story Architect",
        goal="Convert features into epics and detailed user stories using Gherkin format",
        backstory="Trained on agile playbooks and Jira story design best practices.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
