from crewai import Agent
from langchain_community.chat_models import ChatOpenAI



def notifier_agent():
    notifier_agent = Agent(
        role="Project Reporter",
        goal="Generate summary reports for stakeholders and alert them via email/chat",
        backstory="Formats sprint summaries and sends updates to PMs, teams via email, Slack, etc.",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o")
    )
