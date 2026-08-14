import os

from dotenv import load_dotenv

load_dotenv()

from agents import Agent  # noqa: E402

from tools import (  # noqa: E402
    create_task,
    delete_task,
    get_task,
    list_tasks,
    patch_task,
    update_task,
)

MODEL = os.getenv("MODEL", "gpt-5.6")

todo_agent = Agent(
    name="Todo",
    instructions=(
        "You are a helpful task manager. Manage the user's todo list through the "
        "provided tools: list, get, create, update (full replace), patch (partial "
        "update), and delete tasks. Priority must be one of low, medium, or high. "
        "When a user describes a task, use the tools to act on it. Keep answers "
        "concise and confirm what you did."
    ),
    model=MODEL,
    tools=[
        list_tasks,
        get_task,
        create_task,
        update_task,
        patch_task,
        delete_task,
    ],
)