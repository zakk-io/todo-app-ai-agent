import os
import re
from typing import Literal

import httpx


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


Priority = Literal["low", "medium", "high"]





def list_tasks():
    """List all tasks in the todo app."""
    response = httpx.get(f"{API_BASE_URL}/tasks/")
    response.raise_for_status()
    return response.json()



def get_task(task_id: int):
    """Get a single task by its id. Raises an error if the task does not exist."""
    response = httpx.get(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()
    return response.json()



def create_task(
    title: str,
    description: str,
    priority: Priority,
    assigned_to: str,
    completed: bool,
):
    """Create a new task. priority must be one of: low, medium, high. Empty
    description/assigned_to are treated as unset."""
    body = {
        "title": title,
        "description": description or None,
        "priority": priority,
        "assigned_to": assigned_to or None,
        "completed": completed,
    }
    response = httpx.post(f"{API_BASE_URL}/tasks/", json=body)
    response.raise_for_status()
    return response.json()



def update_task(
    task_id: int,
    title: str,
    description: str,
    priority: Priority,
    assigned_to: str,
    completed: bool,
):
    """Fully replace a task with the given fields. All fields are required and
    overwrite the existing values. priority must be one of: low, medium, high."""
    body = {
        "title": title,
        "description": description or None,
        "priority": priority,
        "assigned_to": assigned_to or None,
        "completed": completed,
    }
    response = httpx.put(f"{API_BASE_URL}/tasks/{task_id}", json=body)
    response.raise_for_status()
    return response.json()


def patch_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    priority: Priority | None = None,
    assigned_to: str | None = None,
    completed: bool | None = None,
):
    """Partially update a task. Only the provided fields are changed; omitted
    fields keep their current value. priority must be one of: low, medium, high."""
    body = {k: v for k, v in {
        "title": title,
        "description": description,
        "priority": priority,
        "assigned_to": assigned_to,
        "completed": completed,
    }.items() if v is not None}
    response = httpx.patch(f"{API_BASE_URL}/tasks/{task_id}", json=body)
    response.raise_for_status()
    return response.json()



def delete_task(task_id: int):
    """Delete a task by its id. The API returns no body on success."""
    response = httpx.delete(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()
    return {"deleted": True, "task_id": task_id}