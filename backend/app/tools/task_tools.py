"""MCP Tools for Todo Task Management.

This module implements 5 MCP tools for the OpenAI agent to manage todo tasks:
- add_task: Create new tasks
- list_tasks: Retrieve user's tasks with optional filtering
- complete_task: Mark tasks as completed
- delete_task: Permanently remove tasks
- update_task: Modify task title and/or description

Each tool enforces strict user ownership isolation to ensure data privacy.
"""

from typing import Dict, Any, List, Optional, Union
from sqlmodel import Session, select
from app.models import Task
from uuid import UUID
import logging


def _get_user_tasks_ordered(user_id: str, db: Session) -> List[Task]:
    """Get all user tasks ordered by created_at DESC.

    This establishes the task numbering order (1, 2, 3...).
    """
    return list(db.exec(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    ).all())


def _get_task_by_number(task_number: int, user_id: str, db: Session) -> Optional[Task]:
    """Get a task by its display number (1, 2, 3...).

    Task numbers are based on the order returned by list_tasks.
    """
    if task_number < 1:
        return None

    tasks = _get_user_tasks_ordered(user_id, db)
    if task_number > len(tasks):
        return None

    return tasks[task_number - 1]  # Convert 1-based to 0-based index


def _get_task_if_owned(task_id: Union[str, int], user_id: str, db: Session) -> Optional[Task]:
    """Helper function to get a task by number or UUID.

    Args:
        task_id: The task number (1, 2, 3...) or UUID string
        user_id: The ID of the user requesting the task
        db: Database session

    Returns:
        Task object if owned by user, None otherwise
    """
    # Try to parse as integer (task number like 1, 2, 3)
    try:
        task_number = int(task_id)
        return _get_task_by_number(task_number, user_id, db)
    except (ValueError, TypeError):
        pass

    # Try to parse as UUID
    if isinstance(task_id, str):
        try:
            uuid_id = UUID(task_id)
            task = db.exec(
                select(Task).where(
                    Task.id == uuid_id,
                    Task.user_id == user_id
                )
            ).first()
            return task
        except (ValueError, AttributeError):
            pass

    return None


def add_task(user_id: str, title: str, description: Optional[str] = None, db: Session = None) -> Dict[str, Any]:
    """Add a new task for the user.

    Args:
        user_id: The ID of the user creating the task
        title: The title of the task (required)
        description: The description of the task (optional)
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with task_id, status, and title on success
        Error dictionary on failure
    """
    if not title or not title.strip():
        return {
            "error": "Task title is required",
            "status": "error"
        }

    try:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "task_id": 1,  # New task is always #1 (ordered by newest first)
            "status": "created",
            "title": task.title,
            "message": f"Task '{task.title}' created successfully as Task #1"
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding task for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to add task: {str(e)}",
            "status": "error"
        }


def list_tasks(user_id: str, status: str = "all", db: Session = None) -> Dict[str, Any]:
    """List tasks for the user with optional status filtering.

    Args:
        user_id: The ID of the user whose tasks to list
        status: Filter by status ("all", "pending", "completed"; default: "all")
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with tasks array and status
    """
    try:
        # Build query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        elif status != "all":
            # Invalid status, default to "all" but log warning
            logging.warning(f"Invalid status filter '{status}' for user {user_id}, defaulting to 'all'")

        # Execute query
        tasks = db.exec(query.order_by(Task.created_at.desc())).all()

        # Format response with simple numbered IDs (1, 2, 3...)
        task_list = []
        for index, task in enumerate(tasks, start=1):
            task_dict = {
                "id": index,  # Simple numbered ID for easy reference
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_list.append(task_dict)

        return {
            "tasks": task_list,
            "status": "success",
            "count": len(task_list)
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error listing tasks for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to list tasks: {str(e)}",
            "status": "error"
        }


def complete_task(user_id: str, task_id: Union[str, int], db: Session = None) -> Dict[str, Any]:
    """Mark a task as completed.

    Args:
        user_id: The ID of the user requesting the operation
        task_id: The task number (1, 2, 3...) to complete
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with task_id, status, and title on success
        Error dictionary on failure
    """
    try:
        # Get task with ownership validation
        task = _get_task_if_owned(task_id, user_id, db)
        if not task:
            return {
                "error": f"Task #{task_id} not found. Use list_tasks to see your available tasks.",
                "status": "error"
            }

        # Update task completion status
        task.completed = True
        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "task_id": task_id,
            "status": "completed",
            "title": task.title,
            "message": f"Task #{task_id} '{task.title}' marked as complete"
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error completing task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to complete task: {str(e)}",
            "status": "error"
        }


def delete_task(user_id: str, task_id: Union[str, int], db: Session = None) -> Dict[str, Any]:
    """Delete a task permanently.

    Args:
        user_id: The ID of the user requesting the operation
        task_id: The task number (1, 2, 3...) to delete
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with task_id, status, and title on success
        Error dictionary on failure
    """
    try:
        # Get task with ownership validation
        task = _get_task_if_owned(task_id, user_id, db)
        if not task:
            return {
                "error": f"Task #{task_id} not found. Use list_tasks to see your available tasks.",
                "status": "error"
            }

        # Store title before deleting
        task_title = task.title

        # Delete task
        db.delete(task)
        db.commit()

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task_title,
            "message": f"Task #{task_id} '{task_title}' deleted successfully"
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to delete task: {str(e)}",
            "status": "error"
        }


def update_task(
    user_id: str,
    task_id: Union[str, int],
    title: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = None
) -> Dict[str, Any]:
    """Update a task's title and/or description.

    Args:
        user_id: The ID of the user requesting the operation
        task_id: The task number (1, 2, 3...) to update
        title: New title (optional)
        description: New description (optional)
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with task_id, status, and title on success
        Error dictionary on failure
    """
    try:
        # Get task with ownership validation
        task = _get_task_if_owned(task_id, user_id, db)
        if not task:
            return {
                "error": f"Task #{task_id} not found. Use list_tasks to see your available tasks.",
                "status": "error"
            }

        # Update fields if provided
        if title is not None:
            task.title = title.strip() if title.strip() else task.title
        if description is not None:
            task.description = description.strip() if description else description

        # Update timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        db.add(task)
        db.commit()
        db.refresh(task)

        return {
            "task_id": task_id,
            "status": "updated",
            "title": task.title,
            "message": f"Task #{task_id} updated successfully"
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error updating task {task_id} for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to update task: {str(e)}",
            "status": "error"
        }