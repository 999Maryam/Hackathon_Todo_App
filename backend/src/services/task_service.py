from sqlmodel import Session, select
from typing import List, Optional
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


def get_user_tasks(session: Session, user_id: str) -> List[Task]:
    """Get all tasks for a specific user"""
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks


def create_task_for_user(session: Session, user_id: str, task_create: TaskCreate) -> Task:
    """Create a task for a specific user"""
    task = Task(
        user_id=user_id,
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID and user ID to ensure ownership"""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    return task


def update_task_for_user(session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a task for a specific user (ensures user owns the task)"""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        return None

    # Update fields if provided
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def delete_task_for_user(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a task for a specific user (ensures user owns the task)"""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        return False

    session.delete(task)
    session.commit()
    return True


def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Toggle the completion status of a task for a specific user"""
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        return None

    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task