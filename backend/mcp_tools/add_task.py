from typing import Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Task
import uuid
from uuid import UUID


async def add_task_tool(session: AsyncSession, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Add a new task for the user

    Args:
        session: Async database session
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task_id, status, and title
    """
    # Create new task instance
    task = Task(
        title=title,
        description=description,
        completed=False,
        user_id=UUID(user_id)
    )

    # Add to session and commit
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return {
        "task_id": str(task.id),
        "status": "created",
        "title": task.title
    }