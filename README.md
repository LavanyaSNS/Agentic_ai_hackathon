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

## 🧠 Architecture Diagram

flowchart TD
    A[User Input:<br>Product Idea & Team Metadata] --> B[define_tasks()]
    B --> C[Create Agents & Tasks]
    C --> D[Prompt Generator]
    D --> E[Llama 3.3 via Together API]
    E --> F[LLM Assigns Task to Agent Sequentially]
    F --> G[Final Output: task[] and agent[]]
    G --> H[UI Displays Results (e.g. Streamlit)]
