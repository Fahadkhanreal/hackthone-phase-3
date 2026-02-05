from typing import Dict, Any, List
from sqlmodel.ext.asyncio.session import AsyncSession
from models import Task
from uuid import UUID
from sqlmodel import select


async def list_tasks_tool(session: AsyncSession, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    List tasks for the user based on status

    Args:
        session: Async database session
        user_id: ID of the user whose tasks to list
        status: Filter by status ("all", "pending", "completed")

    Returns:
        List of task dictionaries with id, title, and completed status
    """
    # Build query based on status filter
    query = select(Task).where(Task.user_id == UUID(user_id))

    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)

    # Execute query
    result = await session.exec(query)
    tasks = result.all()

    # Format response
    task_list = []
    for task in tasks:
        task_list.append({
            "id": str(task.id),
            "title": task.title,
            "completed": task.completed
        })

    return task_list