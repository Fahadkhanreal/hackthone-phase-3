from typing import Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Task
from uuid import UUID
from sqlmodel import select
from fastapi import HTTPException


async def complete_task_tool(session: AsyncSession, user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Mark a task as completed

    Args:
        session: Async database session
        user_id: ID of the user who owns the task
        task_id: ID of the task to complete

    Returns:
        Dictionary with task_id, status, and title
    """
    # Find the task owned by the user
    query = select(Task).where(
        Task.id == UUID(task_id),
        Task.user_id == UUID(user_id)
    )

    result = await session.exec(query)
    task = result.first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or does not belong to user")

    # Update task completion status
    task.completed = True
    await session.commit()
    await session.refresh(task)

    return {
        "task_id": str(task.id),
        "status": "completed",
        "title": task.title
    }