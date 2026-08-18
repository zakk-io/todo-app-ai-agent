from google.adk.agents.llm_agent import Agent
from .tools import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    patch_task,
    update_task,
)

root_agent = Agent(
    model='gemini-3.5-flash',
    
    name='todo_agent',
    description='A helpful assistant for managing your todo list.',
    instruction=(
        "You are a helpful task manager. Manage the user's todo list through the "
        "provided tools: list, get, create, update (full replace), patch (partial "
        "update), and delete tasks. Priority must be one of low, medium, or high. "
        "When a user describes a task, use the tools to act on it. Keep answers "
        "concise and confirm what you did."
    ),
        
    tools=[
        list_tasks,
        get_task,
        create_task,
        update_task,
        patch_task,
        delete_task,
    ],
)