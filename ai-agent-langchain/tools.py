import os
import re
from typing import Literal
import psycopg2
import httpx
from langchain.tools import tool

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DATABASE_URL = os.getenv("DATABASE_URL")

Priority = Literal["low", "medium", "high"]




@tool
def list_tasks():
    """List all tasks in the todo app."""
    response = httpx.get(f"{API_BASE_URL}/tasks/")
    response.raise_for_status()
    return response.json()


@tool
def get_task(task_id: int):
    """Get a single task by its id. Raises an error if the task does not exist."""
    response = httpx.get(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()
    return response.json()


@tool
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


@tool
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


@tool()
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


@tool()
def delete_task(task_id: int):
    """Delete a task by its id. The API returns no body on success."""
    response = httpx.delete(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()
    return {"deleted": True, "task_id": task_id}





@tool
def execute_readonly_sql(sql: str):
    """Execute a read-only SQL query for reporting."""

    if not sql.strip().lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed."}

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_session(readonly=True)

        with conn.cursor() as cur:
            cur.execute(sql)

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()

            return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        return {"error": str(e)}

    finally:
        if conn:
            conn.close()