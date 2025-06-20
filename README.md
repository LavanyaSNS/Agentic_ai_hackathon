# 🤖 Agentic AI Co-Pilot for Agile Execution

> An LLM-powered agentic system that transforms a vague product idea into a full agile sprint plan with tasks, timelines, assignments, and progress monitoring—autonomously!

## 🚀 Live Workflow (Demo URL)
🔗 [View the Agentic AI Workflow](https://your-deployment-url.com)  
*Replace with actual hosted URL (Streamlit, Hugging Face, or Vercel)*

---

## 🧩 What This Project Does

This project uses **agent-based workflow orchestration** and **LLM coordination** (via [Together AI](https://www.together.ai/)) to simulate a product manager. It breaks down a raw product idea using 7 agents, each with a specific role, and automatically executes the agile cycle.

### 🎯 Input
- A vague product idea (text)
- Team metadata (JSON)

### ⚙️ Output
- Extracted domain, personas, features
- User stories and epics
- Skill-matched assignments
- Gantt-style timeline
- Mock progress report and blocker detection
- Dynamic timeline adjustments
- Email + markdown sprint summary

---
## Project Structure

agentic_ai_copilot/
├── agents/
│   ├── agent_1_idea_extractor.py
│   ├── agent_2_epic_story_generator.py
│   └── ... (up to agent_7_notifier.py)
├── tasks/
│   └── task_manager.py
├── ui/
│   └── streamlit_app.py
├── llm/
│   └── together_llm_runner.py
├── main.py
└── README.md


## 🧠 Architecture Diagram

```mermaid
graph TD
    A[User Input: Product Idea & Team JSON] --> B[define_tasks()]
    B --> C[7 Agents + 7 Tasks Created]
    C --> D[Prompt Generated for LLM]
    D --> E[Llama-3.3 70B via Together API]
    E --> F[LLM Assigns Tasks to Agents Sequentially]
    F --> G[Final Return: task[], agent[]]
    G --> H[Streamlit Frontend Displays Output]


