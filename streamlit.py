# --------------------------------------------
# Agentic AI Co-Pilot: Main Workflow with Notion + Google Calendar + Streamlit
# --------------------------------------------

# Step 1: Install required packages
# pip install crewai[tools] langchain openai notion-client google-api-python-client streamlit

import os
import streamlit as st
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain.chat_models import ChatOpenAI
from notion_client import Client as NotionClient
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

# ----------------------
# Config: API Keys & Clients
# ----------------------
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
os.environ["SERPER_API_KEY"] = "your-serper-api-key"
NOTION_TOKEN = "your-notion-token"
NOTION_DB_ID = "your-database-id"
notion = NotionClient(auth=NOTION_TOKEN)

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'calendar-credentials.json'
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
calendar_service = build('calendar', 'v3', credentials=creds)

llm = ChatOpenAI(model="gpt-4o", temperature=0)
search_tool = SerperDevTool()

# ----------------------
# Define AI Agents (same as earlier)
# ----------------------
idea_agent = Agent(
    role="Product Idea Analyst",
    goal="Understand vague product idea and extract features, modules, personas.",
    tools=[search_tool],
    verbose=True, llm=llm
)

story_agent = Agent(
    role="Agile Story Generator",
    goal="Convert extracted features into epics and Gherkin-style user stories.",
    verbose=True, llm=llm
)

# ... [Repeat for allocator_agent, planner_agent, tracker_agent, adjuster_agent, notifier_agent]

# ----------------------
# Notion Integration
# ----------------------
def log_task_to_notion(story_data: dict):
    notion.pages.create(
        parent={"database_id": NOTION_DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": story_data["title"]}}]},
            "Assigned To": {"rich_text": [{"text": {"content": story_data["developer"]}}]},
            "Status": {"select": {"name": story_data["status"]}}
        }
    )

# ----------------------
# Google Calendar Integration
# ----------------------
def schedule_sprint_event(title: str, start_date: str, end_date: str):
    event = {
        'summary': title,
        'start': {'dateTime': start_date, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_date, 'timeZone': 'Asia/Kolkata'}
    }
    calendar_service.events().insert(calendarId='primary', body=event).execute()

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="Agentic AI Co-Pilot", layout="wide")
st.title("🚀 Agentic AI Co-Pilot for Agile Execution")

product_idea = st.text_area("Enter Vague Product Idea")

if st.button("Run Agentic Workflow"):
    with st.spinner("Analyzing idea and executing agents..."):
        # Simulate the workflow
        result_idea = "Remote check-in tool with voice input, dashboard, and summaries. Personas: PM, Dev. Risks: Privacy."
        st.success("✅ Idea Extracted")

        epics_and_stories = [{
            "title": "Submit daily voice check-in",
            "developer": "Karan",
            "status": "To Do"
        }, {
            "title": "Summarize check-ins with AI",
            "developer": "Riya",
            "status": "In Progress"
        }]

        st.markdown("### 🧩 User Stories")
        for story in epics_and_stories:
            st.write(f"**{story['title']}** - Assigned to {story['developer']} [{story['status']}]")
            log_task_to_notion(story)

        # Schedule dummy sprint dates
        today = datetime.datetime.now()
        for i, story in enumerate(epics_and_stories):
            start = (today + datetime.timedelta(days=i)).isoformat()
            end = (today + datetime.timedelta(days=i+1)).isoformat()
            schedule_sprint_event(story['title'], start, end)

        st.success("✅ Tasks logged in Notion and scheduled in Google Calendar")
