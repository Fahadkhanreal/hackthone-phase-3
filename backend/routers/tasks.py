from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from uuid import UUID
from database import engine
from models import Task
from auth.dependencies import get_current_user
from schemas.task_schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(prefix="/{user_id}/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
async def list_tasks(user_id: str, current_user_id: str = Depends(get_current_user)):
    """
    List all tasks for a specific user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Query the database for tasks belonging to this user
    async with AsyncSession(engine) as session:
        statement = select(Task).where(Task.user_id == user_uuid)
        result = await session.exec(statement)
        tasks = result.all()
        return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Create a new task for a specific user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Create a new task with the authenticated user's ID
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_uuid
    )

    # Save the task to the database
    async with AsyncSession(engine) as session:
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Get a specific task by ID for the specified user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id and task_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID or task ID format"
        )

    # Query the database for the specific task belonging to this user
    async with AsyncSession(engine) as session:
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        result = await session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    task_id: str,
    task_data: TaskUpdate,
    current_user_id: str = Depends(get_current_user)
):
    """
    Update a specific task by ID for the specified user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id and task_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID or task ID format"
        )

    # Query the database for the specific task belonging to this user
    async with AsyncSession(engine) as session:
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        result = await session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the task with provided data
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Delete a specific task by ID for the specified user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id and task_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID or task ID format"
        )

    # Query the database for the specific task belonging to this user
    async with AsyncSession(engine) as session:
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        result = await session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        await session.delete(task)
        await session.commit()
        return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion(
    user_id: str,
    task_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """
    Toggle the completion status of a specific task for the specified user
    """
    # Verify that the user_id in the path matches the authenticated user's ID
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this user"
        )

    # Convert user_id and task_id to UUID for database query
    try:
        user_uuid = UUID(user_id)
        task_uuid = UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID or task ID format"
        )

    # Query the database for the specific task belonging to this user
    async with AsyncSession(engine) as session:
        statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        result = await session.exec(statement)
        task = result.first()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle the completion status
        task.completed = not task.completed
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task