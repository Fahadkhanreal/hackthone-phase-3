from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskCreate(BaseModel):
    """
    Schema for creating new tasks
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = False


class TaskUpdate(BaseModel):
    """
    Schema for updating existing tasks
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TaskRead(TaskCreate):
    """
    Schema for returning task data
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID