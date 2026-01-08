"""Task service with business logic."""

from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.task import Task
from app.models.schemas import TaskCreate, TaskUpdate
from app.utils.errors import NotFoundException


class TaskService:
    """Service for task business logic and database operations."""

    @staticmethod
    def get_all_tasks(session: Session, user_id: str) -> List[Task]:
        """Get all tasks for a specific user.

        Args:
            session: Database session.
            user_id: User ID to filter tasks by.

        Returns:
            List of Task objects for the user.
        """
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def get_task(session: Session, user_id: str, task_id: uuid.UUID) -> Task:
        """Get a single task by ID with ownership validation.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to retrieve.

        Returns:
            Task object if found and owned by user.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException("Task not found")
        return task

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_create: TaskCreate,
    ) -> Task:
        """Create a new task for a user.

        Args:
            session: Database session.
            user_id: Task owner (from JWT).
            task_create: Task creation data.

        Returns:
            Created Task object.
        """
        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        task_update: TaskUpdate,
    ) -> Task:
        """Update an existing task with partial fields.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to update.
            task_update: Partial task update data.

        Returns:
            Updated Task object.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = TaskService.get_task(session, user_id, task_id)

        # Update only provided fields
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description

        # Update modified timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def toggle_complete(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> Task:
        """Toggle task completion status.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to toggle.

        Returns:
            Task with toggled completion status.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = TaskService.get_task(session, user_id, task_id)
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> None:
        """Delete a task permanently.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to delete.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = TaskService.get_task(session, user_id, task_id)
        session.delete(task)
        session.commit()
