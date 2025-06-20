from agents.agent_1_idea_extractor import idea_agent
from agents.agent_2_epic_story_generator import story_agent
from agents.agent_3_skill_matcher import assignment_agent
from agents.agent_4_scheduler import timeline_agent
from agents.agent_5_progress_tracker import tracker_agent
from agents.agent_6_timeline_adjuster import recovery_agent
from agents.agent_7_notifier import notifier_agent
from crewai import Task

def define_tasks(product_idea: str, team_metadata: dict):
    # Agents don't take parameters at init; context is passed through task descriptions
    agent1 = idea_agent()
    agent2 = story_agent()
    agent3 = assignment_agent()
    agent4 = timeline_agent()
    agent5 = tracker_agent()
    agent6 = recovery_agent()
    agent7 = notifier_agent()

    task1 = Task(
        description=(
            f"Analyze the following product idea and extract:\n"
            f"- domain\n- feature list\n- personas\n- risks\n- modules\n\n"
            f"Product Idea: {product_idea}\n\n"
            f"Team Metadata: {team_metadata}"
        ),
        expected_output="Structured JSON with domain, personas, features, modules, and risks.",
        agent=agent1
    )

    task2 = Task(
        description=(
            "Use the extracted features from Task 1 to create epics and detailed user stories "
            "in Gherkin or SMART format."
        ),
        expected_output="List of epics and user stories in Markdown and JSON format.",
        agent=agent2,
        depends_on=[task1]
    )

    task3 = Task(
        description=(
            "Using the user stories from Task 2 and the team metadata, "
            "match each story to team members based on skills and availability."
        ),
        expected_output="JSON or CSV task allocation matrix with story-to-member mapping.",
        agent=agent3,
        depends_on=[task2]
    )

    task4 = Task(
        description=(
            "Generate a Gantt-style calendar and sprint plan using the task assignments from Task 3. "
            "Include estimated dates and durations."
        ),
        expected_output="Sprint calendar with scheduled stories and deadline information.",
        agent=agent4,
        depends_on=[task3]
    )

    task5 = Task(
        description=(
            "Simulate monitoring developer progress using mock updates (e.g., JSON check-ins). "
            "Identify any blockers or delays."
        ),
        expected_output="Live status report and blocker list in structured JSON.",
        agent=agent5,
        depends_on=[task4]
    )

    task6 = Task(
        description=(
            "If delays or blockers are detected from Task 5, dynamically adjust the sprint plan, "
            "recalculate timelines, and reassign tasks if necessary."
        ),
        expected_output="Updated timeline and story allocation reflecting any adjustments.",
        agent=agent6,
        depends_on=[task5]
    )

    task7 = Task(
        description=(
            "Summarize the current sprint progress, including delay risks, blockers, and "
            "next steps for stakeholders. Generate a markdown report and email content."
        ),
        expected_output="Markdown + email summary of sprint progress with attached charts or JSON.",
        agent=agent7,
        depends_on=[task6]
    )

    return [task1, task2, task3, task4, task5, task6, task7], [
        agent1, agent2, agent3, agent4, agent5, agent6, agent7
    ]


'''

import os
import requests

def run_agent_task_allocation(product_idea, team_metadata, together_api_key):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }

    # Construct the full prompt
    prompt = f"""
    You are a task orchestrator AI responsible for managing an agentic workflow involving 7 agents and 7 interdependent tasks.

    Each agent has a specialized role and must be assigned a specific task. Your job is to:
    - Understand the description of each task and its expected output.
    - Sequentially assign each task to the correct agent based on their role.
    - Wait for the output of dependent tasks before continuing.
    - Ensure each agent completes their assigned task and returns structured output.

    Below is the complete setup from a function `define_tasks(product_idea, team_metadata)`:

    ---

    AGENTS:

    1. Agent1 - Role: Product Idea Analyst
    2. Agent2 - Role: Epic Story Generator
    3. Agent3 - Role: Skill Matcher
    4. Agent4 - Role: Sprint Scheduler
    5. Agent5 - Role: Progress Tracker
    6. Agent6 - Role: Timeline Adjuster
    7. Agent7 - Role: Stakeholder Notifier

    ---

    TASK FLOW:

    Task 1 (Agent1): Analyze the product idea and extract domain, feature list, personas, risks, and modules.
    Output: JSON with domain, personas, features, modules, risks.

    Task 2 (Agent2): Use Task 1 output to write user stories in Gherkin or SMART format.
    Depends on: Task 1
    Output: List of epics and user stories in Markdown/JSON.

    Task 3 (Agent3): Assign user stories to team members using team metadata and Task 2.
    Depends on: Task 2
    Output: CSV/JSON allocation matrix.

    Task 4 (Agent4): Create a sprint schedule based on assignments from Task 3.
    Depends on: Task 3
    Output: Sprint calendar with dates and duration.

    Task 5 (Agent5): Simulate progress with mock updates and identify blockers.
    Depends on: Task 4
    Output: JSON report on progress and blockers.

    Task 6 (Agent6): Adjust sprint plan if blockers from Task 5 exist.
    Depends on: Task 5
    Output: Updated schedule in JSON.

    Task 7 (Agent7): Summarize sprint progress and notify stakeholders.
    Depends on: Task 6
    Output: Markdown/email summary report.

    ---

    Given this setup, assign the following product idea and team metadata:

    Product Idea:
    {product_idea}

    Team Metadata:
    {team_metadata}

    Return the result as:
    return [task1, task2, task3, task4, task5, task6, task7], [agent1, agent2, agent3, agent4, agent5, agent6, agent7]
    """

    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error: {response.status_code}\n{response.text}")
'''



import subprocess
import json
from tasks.task_manager import define_tasks  # assuming your task manager is defined here

def run_task_assignment_with_llm(product_idea: str, team_metadata: dict, together_api_key: str):
    tasks, agents = define_tasks(product_idea, team_metadata)

    # Step 1: Construct the agent + task prompt
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

    prompt_lines.append(
        "🎯 FINAL INSTRUCTION TO MODEL:\n"
        "1. Sequentially assign each task to its corresponding agent.\n"
        "2. For each assignment, invoke the LLM with the task's `description`, `agent role`, and any `depends_on` input.\n"
        "3. After all tasks are complete, return:\n"
        "```python\nreturn [task1, task2, task3, task4, task5, task6, task7], [agent1, agent2, agent3, agent4, agent5, agent6, agent7]\n```"
    )

    full_prompt = "\n".join(prompt_lines)

    # Step 2: Construct JSON payload for Together API
    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    }

    # Step 3: Write payload to temporary file
    with open("tmp_payload.json", "w", encoding="utf-8") as f:
        json.dump(payload, f)

    # Step 4: Call the Together API via curl
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

    # Step 5: Parse and return response
    try:
        output = json.loads(result.stdout)
        content = output["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        raise ValueError(f"Invalid response format from Together API: {e}\n\n{result.stdout}")
