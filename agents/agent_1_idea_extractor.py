from crewai import Agent
from langchain_community.chat_models import ChatOpenAI

def idea_agent(product_idea, team_metadata):
    prompt = (
        f"You are a Product Idea Analyst.\n"
        f"Analyze the following product idea and extract domain, features, modules, personas, and risks.\n\n"
        f"Product Idea:\n{product_idea}\n\n"
        f"Team Metadata:\n{team_metadata}\n\n"
        f"Please provide a structured JSON output including:\n"
        f"- domain\n- personas\n- feature list\n- risks\n- modules\n"
    )
    
    return Agent(
        role="Product Idea Analyst",
        goal="Understand the vague product idea and extract domain, features, modules, personas, and risks.",
        backstory=prompt,  # pass the input inside backstory/prompt for context
        verbose=True,
        llm=ChatOpenAI(model_name="gpt-4o", temperature=0)
    )
