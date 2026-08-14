from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

PriorityValue = Literal["low", "medium", "high"]


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: PriorityValue = "medium"
    assigned_to: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityValue] = None
    assigned_to: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)