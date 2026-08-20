
import os
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

from tools import (  # noqa: E402
    create_task,
    delete_task,
    get_task,
    list_tasks,
    patch_task,
    update_task,
    execute_readonly_sql
)

MODEL = os.getenv("MODEL", "gpt-4.1-mini")


todo_agent = create_agent(
    model=MODEL,
    tools=[
        list_tasks,
        get_task,
        create_task,
        update_task,
        patch_task,
        delete_task,
        execute_readonly_sql
    ],
    system_prompt=(
        "You are a helpful task manager. Manage the user's todo list through the "
        "provided tools: list, get, create, update (full replace), patch (partial "
        "update), delete tasks, and execute_readonly_sql for reporting. "
        "Use execute_readonly_sql only when the user asks for statistics, summaries, "
        "counts, or reports. Only generate SELECT queries with it; never modify the "
        "database through SQL. Priority must be one of low, medium, or high. "
        "When a user describes a task, use the appropriate tools to act on it. "
        "Keep answers concise and confirm what you did."
    ),
)