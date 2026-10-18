"""Pydantic models for the TaskFlow API."""
from typing import Literal, Optional

from pydantic import BaseModel, Field

TaskStatus = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: Optional[TaskStatus] = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: str
