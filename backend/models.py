from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column


def generate_uuid():
    return uuid4()


class User(SQLModel, table=True):
    """
    User model for authentication
    """
    id: Optional[UUID] = Field(default_factory=generate_uuid, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    email: str = Field(..., unique=True, nullable=False)
    password_hash: str = Field(..., nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))


class Task(SQLModel, table=True):
    """
    Task model representing a todo item with properties for title, description,
    completion status, timestamps, and user association
    """
    id: Optional[UUID] = Field(default_factory=generate_uuid, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    user_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), nullable=False))


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a user's chat session with the AI chatbot
    """
    id: Optional[UUID] = Field(default_factory=generate_uuid, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    user_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))


class Message(SQLModel, table=True):
    """
    Message model representing individual messages exchanged between user and chatbot
    """
    id: Optional[UUID] = Field(default_factory=generate_uuid, sa_column=Column(pg.UUID(as_uuid=True), primary_key=True))
    user_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), nullable=False))
    conversation_id: UUID = Field(sa_column=Column(pg.UUID(as_uuid=True), nullable=False))
    role: str = Field(..., max_length=20)  # "user" or "assistant"
    content: str = Field(..., max_length=5000)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))