import subprocess
import json
from crewai import Crew
from tasks.task_manager import define_tasks  # This must support rag_text

def run_task_assignment_with_llm(product_idea: str, team_metadata: dict, together_api_key: str = None, rag_text: str = None, use_together_llm: bool = False):
    tasks, agents = define_tasks(
        product_idea=product_idea,
        team_metadata=team_metadata,
        rag_text=rag_text
    )

    if not use_together_llm:
        # ✅ Run via CrewAI (autonomous agentic execution)
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            planning=True
        )
        return crew.kickoff()

    # ✅ Run via LLM orchestration simulation with Together API
    prompt_lines = [
        "You are a task orchestrator AI responsible for managing an agentic workflow involving 7 agents and 7 interdependent tasks.",
        "",
        "Each agent has a specialized role and must be assigned a specific task. Your job is to:",
        "- Understand the description of each task and its expected output.",
        "- Sequentially assign each task to the correct agent based on their role.",
        "- Wait for the output of dependent tasks before continuing.",
        "- Ensure each agent completes their assigned task and returns structured output.",
        "",
        "TASK & AGENT LIST:\n"
    ]

    for i, (task, agent) in enumerate(zip(tasks, agents), start=1):
        prompt_lines.append(f"**Task {i} (Agent{i})**")
        prompt_lines.append(f"🧠 Agent Role: {agent.role}")
        prompt_lines.append(f"📝 Task Description: {task.description}")
        if hasattr(task, 'depends_on') and task.depends_on:
            deps = ', '.join([f'Task {tasks.index(dep)+1}' for dep in task.depends_on])
            prompt_lines.append(f"🔁 Depends on: {deps}")
        prompt_lines.append(f"🎯 Expected Output: {task.expected_output}")
        prompt_lines.append("")

    if rag_text:
        prompt_lines.append("📚 Additional RAG Context Provided:\n")
        prompt_lines.append(rag_text)
        prompt_lines.append("")

    prompt_lines.append(
        "🎯 FINAL INSTRUCTION TO MODEL:\n"
        "1. Sequentially assign each task to its corresponding agent.\n"
        "2. For each assignment, invoke the LLM with the task's description, agent role, and any depends_on input.\n"
        "3. After all tasks are complete, return:\n"
        "```python\nreturn [task1, task2, task3, task4, task5, task6, task7], [agent1, agent2, agent3, agent4, agent5, agent6, agent7]\n```"
    )

    full_prompt = "\n".join(prompt_lines)

    # Create JSON payload
    payload = {
        "model": "meta-llama/Llama-3-70B-Instruct",
        "messages": [{"role": "user", "content": full_prompt}]
    }

    # Save prompt to file
    with open("tmp_payload.json", "w", encoding="utf-8") as f:
        json.dump(payload, f)

    curl_command = f'''
    curl -s -X POST "https://api.together.xyz/v1/chat/completions" \\
      -H "Authorization: Bearer {together_api_key}" \\
      -H "Content-Type: application/json" \\
      -d @tmp_payload.json
    '''

    print("[INFO] Sending request to Together API...")
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")

    try:
        output = json.loads(result.stdout)
        return output["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Invalid response format from Together API: {e}\n\n{result.stdout}")
