from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import Column
import sqlalchemy.dialects.postgresql as pg


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields
    """
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), nullable=False))


class Task(TaskBase, table=True):
    """
    Task model representing a todo item with properties for title, description,
    completion status, timestamps, and user association
    """
    id: Optional[UUID] = Field(default_factory=uuid4, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))


class TaskRead(TaskBase):
    """
    Schema for reading Task data
    """
    id: UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """
    Schema for creating Task data
    """
    pass


class TaskUpdate(SQLModel):
    """
    Schema for updating Task data
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    user_id: Optional[UUID] = None