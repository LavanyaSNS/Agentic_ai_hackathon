import streamlit as st
import json
from tasks.task_manager import run_task_assignment_with_llm   
from config import TOGETHER_API
import fitz  # PyMuPDF

# --- Config ---
st.set_page_config(page_title="Agentic AI Co-Pilot", layout="wide")
st.title("🚀 Agentic AI Co-Pilot for Agile Project Execution")
st.subheader("Turn a vague product idea + team metadata into an autonomous sprint plan")

# --- Input Section ---
st.markdown("### 🧠 Enter Your Product Idea")
product_idea = st.text_area(
    "Describe your idea vaguely, and let AI do the rest!",
    placeholder="e.g., A platform where remote teams can track updates using voice check-ins...",
    height=180
)

# --- Default Team Metadata
default_team = {
    "team_name": "Velocity Devs",
    "team_members": [
        {"name": "Riya", "role": "Frontend Developer", "skills": ["React", "TypeScript", "Figma"], "availability": 25},
        {"name": "Karan", "role": "Backend Developer", "skills": ["Node.js", "MongoDB", "Express"], "availability": 30},
        {"name": "Sneha", "role": "AI/ML Engineer", "skills": ["Python", "Whisper", "LLMs", "FastAPI"], "availability": 20},
        {"name": "Vikram", "role": "DevOps Engineer", "skills": ["Docker", "Kubernetes", "AWS", "CI/CD"], "availability": 15}
    ]
}

st.markdown("### 👥 Enter Team Metadata (JSON)")
team_metadata_input = st.text_area(
    "Paste your team metadata (JSON format)",
    value=json.dumps(default_team, indent=2),
    height=300
)

# --- 📄 Upload RAG Document ---
st.markdown("### 📄 Upload Agile Docs or Playbook for RAG (Optional)")
uploaded_file = st.file_uploader(
    "Upload a `.txt`, `.md`, or `.pdf` file to enrich context with Agile knowledge:",
    type=["txt", "md", "pdf"]
)

rag_text = None

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]

    try:
        if file_type in ["txt", "md"]:
            rag_text = uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            # Extract text using PyMuPDF
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                rag_text = "\n".join(page.get_text() for page in doc)

        if rag_text:
            st.success(f"✅ {uploaded_file.name} uploaded and processed successfully!")
            with st.expander("📘 View Extracted RAG Content"):
                st.text_area("Extracted Content", rag_text, height=250)
        else:
            st.warning("❌ Could not extract content from the uploaded file.")
    except Exception as e:
        st.error(f"Error reading file: {e}")


# --- API Key Section
together_api_key = TOGETHER_API

# --- Action Button ---
if st.button("✨ Run Agentic AI Workflow"):
    if not product_idea.strip():
        st.warning("Please enter a product idea.")
    elif not together_api_key.strip():
        st.warning("Please enter your Together API Key.")
    else:
        try:
            team_metadata = json.loads(team_metadata_input)
            st.success("✅ Inputs captured. Running Agentic AI...")

            with st.spinner("Thinking with Llama-3..."):
                result = run_task_assignment_with_llm(
                    product_idea=product_idea,
                    team_metadata=team_metadata,
                    together_api_key=together_api_key,
                    rag_text=rag_text  # Pass the uploaded text here
                )

            st.markdown("### ✅ Output from LLM Task Allocator")
            st.markdown(result)

        except json.JSONDecodeError:
            st.error("Invalid JSON format in team metadata.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
