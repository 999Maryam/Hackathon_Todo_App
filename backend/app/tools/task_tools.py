"""MCP Tools for Todo Task Management.

This module implements MCP tools for the OpenAI agent to manage todo tasks:
- add_task: Create new tasks with priority, due_date, tags
- list_tasks: Retrieve user's tasks with search, filtering, sorting
- complete_task: Mark tasks as completed
- delete_task: Permanently remove tasks
- update_task: Modify task title, description, priority, due_date
- add_tag: Create new tags
- list_tags: Retrieve user's tags
- set_reminder: Set task reminders

Phase V: Extended with priority, due_date, tags, reminders, search, filter, sort.

Each tool enforces strict user ownership isolation to ensure data privacy.
"""

from datetime import datetime
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


def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    db: Session = None
) -> Dict[str, Any]:
    """Add a new task for the user.

    T110: Extended with priority, due_date, tag_ids parameters.

    Args:
        user_id: The ID of the user creating the task
        title: The title of the task (required)
        description: The description of the task (optional)
        priority: Task priority - "low", "medium", or "high" (default: "medium")
        due_date: Due date in ISO format, e.g. "2025-01-20T10:00:00" (optional)
        tag_ids: List of tag IDs to assign to the task (optional)
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

    # Validate priority
    valid_priorities = {"low", "medium", "high"}
    task_priority = (priority or "medium").lower()
    if task_priority not in valid_priorities:
        return {
            "error": f"Invalid priority '{priority}'. Must be one of: low, medium, high",
            "status": "error"
        }

    # Parse due_date if provided
    task_due_date = None
    if due_date:
        try:
            task_due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
        except ValueError:
            return {
                "error": f"Invalid due_date format. Use ISO format: YYYY-MM-DDTHH:MM:SS",
                "status": "error"
            }

    try:
        # Create new task
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            priority=task_priority,
            due_date=task_due_date,
            completed=False
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        # Assign tags if provided
        assigned_tags = []
        if tag_ids:
            from app.services.tag_service import TagService
            try:
                tags = TagService.set_task_tags(db, user_id, task.id, tag_ids)
                assigned_tags = [{"id": t.id, "name": t.name} for t in tags]
            except Exception as tag_error:
                logging.warning(f"Failed to assign tags: {tag_error}")

        return {
            "task_id": 1,  # New task is always #1 (ordered by newest first)
            "status": "created",
            "title": task.title,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": assigned_tags,
            "message": f"Task '{task.title}' created successfully as Task #1"
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error adding task for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to add task: {str(e)}",
            "status": "error"
        }


def list_tasks(
    user_id: str,
    status: str = "all",
    search: Optional[str] = None,
    priority: Optional[List[str]] = None,
    tag_ids: Optional[List[int]] = None,
    due_from: Optional[str] = None,
    due_to: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
    db: Session = None
) -> Dict[str, Any]:
    """List tasks for the user with search, filtering, and sorting.

    T111: Extended with search, filter (priority, tags, due dates), and sort.

    Args:
        user_id: The ID of the user whose tasks to list
        status: Filter by status ("all", "pending", "completed"; default: "all")
        search: Search term to filter by title/description (optional)
        priority: List of priorities to filter by, e.g. ["high", "medium"] (optional)
        tag_ids: List of tag IDs - tasks must have at least one of these tags (optional)
        due_from: Filter tasks due after this date (ISO format) (optional)
        due_to: Filter tasks due before this date (ISO format) (optional)
        sort_by: Sort field - "due_date", "priority", "created_at", "title" (optional)
        sort_order: Sort order - "asc" or "desc" (default: "asc")
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with tasks array, count, and applied filters
    """
    from sqlalchemy import case

    try:
        # Build query with user isolation
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        elif status != "all":
            logging.warning(f"Invalid status filter '{status}' for user {user_id}, defaulting to 'all'")

        # Search filter
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )

        # Priority filter
        if priority:
            valid_priorities = [p.lower() for p in priority if p.lower() in {"low", "medium", "high"}]
            if valid_priorities:
                query = query.where(Task.priority.in_(valid_priorities))

        # Due date range filter
        if due_from:
            try:
                from_date = datetime.fromisoformat(due_from.replace("Z", "+00:00"))
                query = query.where(Task.due_date >= from_date)
            except ValueError:
                logging.warning(f"Invalid due_from format: {due_from}")

        if due_to:
            try:
                to_date = datetime.fromisoformat(due_to.replace("Z", "+00:00"))
                query = query.where(Task.due_date <= to_date)
            except ValueError:
                logging.warning(f"Invalid due_to format: {due_to}")

        # Tag filter
        if tag_ids:
            from app.models.task_tag import TaskTag
            query = query.where(
                Task.id.in_(
                    select(TaskTag.task_id).where(TaskTag.tag_id.in_(tag_ids))
                )
            )

        # Sorting
        if sort_by:
            if sort_by == "priority":
                # Priority sort: high=1, medium=2, low=3
                priority_order = case(
                    (Task.priority == "high", 1),
                    (Task.priority == "medium", 2),
                    (Task.priority == "low", 3),
                    else_=2,
                )
                if sort_order == "desc":
                    query = query.order_by(priority_order.desc())
                else:
                    query = query.order_by(priority_order.asc())
            elif sort_by in {"due_date", "created_at", "title"}:
                order_column = getattr(Task, sort_by, Task.created_at)
                if sort_order == "desc":
                    query = query.order_by(order_column.desc().nulls_last())
                else:
                    query = query.order_by(order_column.asc().nulls_last())
            else:
                logging.warning(f"Invalid sort_by: {sort_by}, using default")
                query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.desc())

        # Execute query
        tasks = db.exec(query).all()

        # Get tags for each task
        from app.services.tag_service import TagService

        # Format response with simple numbered IDs (1, 2, 3...)
        task_list = []
        for index, task in enumerate(tasks, start=1):
            # Get task tags
            try:
                task_tags = TagService.get_task_tags(db, user_id, task.id)
                tags = [{"id": t.id, "name": t.name} for t in task_tags]
            except Exception:
                tags = []

            task_dict = {
                "id": index,  # Simple numbered ID for easy reference
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": tags,
                "is_recurring": task.is_recurring,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            task_list.append(task_dict)

        return {
            "tasks": task_list,
            "status": "success",
            "count": len(task_list),
            "filters_applied": {
                "status": status,
                "search": search,
                "priority": priority,
                "tag_ids": tag_ids,
                "due_from": due_from,
                "due_to": due_to,
                "sort_by": sort_by,
                "sort_order": sort_order,
            }
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


# =============================================================================
# Phase V MCP Tools: Tags (T112, T113)
# =============================================================================


def add_tag(user_id: str, name: str, db: Session = None) -> Dict[str, Any]:
    """Create a new tag for the user.

    T112: Add tag MCP tool.

    Args:
        user_id: The ID of the user creating the tag
        name: The name of the tag (required, must be unique per user)
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with tag_id, name, and status on success
        Error dictionary on failure
    """
    if not name or not name.strip():
        return {
            "error": "Tag name is required",
            "status": "error"
        }

    try:
        from app.services.tag_service import TagService
        from app.schemas.tag import TagCreate

        tag_create = TagCreate(name=name.strip())
        tag = TagService.create_tag(db, user_id, tag_create)

        return {
            "tag_id": tag.id,
            "name": tag.name,
            "status": "created",
            "message": f"Tag '{tag.name}' created successfully"
        }
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            return {
                "error": f"Tag '{name}' already exists",
                "status": "error"
            }
        logging.error(f"Error adding tag for user {user_id}: {error_msg}")
        return {
            "error": f"Failed to add tag: {error_msg}",
            "status": "error"
        }


def list_tags(user_id: str, db: Session = None) -> Dict[str, Any]:
    """List all tags for the user with task counts.

    T113: List tags MCP tool.

    Args:
        user_id: The ID of the user whose tags to list
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with tags array and count
    """
    try:
        from app.services.tag_service import TagService

        tags_with_counts = TagService.get_user_tags(db, user_id)

        tag_list = [
            {
                "id": tag.id,
                "name": tag.name,
                "task_count": tag.task_count,
            }
            for tag in tags_with_counts
        ]

        return {
            "tags": tag_list,
            "status": "success",
            "count": len(tag_list)
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Error listing tags for user {user_id}: {str(e)}")
        return {
            "error": f"Failed to list tags: {str(e)}",
            "status": "error"
        }


# =============================================================================
# Phase V MCP Tools: Reminders (T114)
# =============================================================================


def set_reminder(
    user_id: str,
    task_id: Union[str, int],
    minutes_before: Optional[int] = None,
    remind_at: Optional[str] = None,
    db: Session = None
) -> Dict[str, Any]:
    """Set a reminder for a task.

    T114: Set reminder MCP tool.

    Args:
        user_id: The ID of the user setting the reminder
        task_id: The task number (1, 2, 3...) or UUID to set reminder for
        minutes_before: Minutes before due_date to remind (e.g., 60 for 1 hour)
        remind_at: Specific reminder time in ISO format (alternative to minutes_before)
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with reminder details on success
        Error dictionary on failure

    Note:
        - Either minutes_before OR remind_at must be provided
        - Task must have a due_date set
        - Reminder time must be before the due_date
    """
    if not minutes_before and not remind_at:
        return {
            "error": "Either minutes_before or remind_at is required",
            "status": "error"
        }

    try:
        # Get task with ownership validation
        task = _get_task_if_owned(task_id, user_id, db)
        if not task:
            return {
                "error": f"Task #{task_id} not found. Use list_tasks to see your available tasks.",
                "status": "error"
            }

        if not task.due_date:
            return {
                "error": "Cannot set reminder for task without due date. Set a due_date first.",
                "status": "error"
            }

        from app.services.reminder_service import ReminderService

        if minutes_before:
            if minutes_before <= 0:
                return {
                    "error": "minutes_before must be a positive number",
                    "status": "error"
                }
            reminder = ReminderService.set_reminder_minutes_before(
                db, user_id, task.id, minutes_before
            )
        else:
            # Parse remind_at datetime
            try:
                remind_datetime = datetime.fromisoformat(remind_at.replace("Z", "+00:00"))
            except ValueError:
                return {
                    "error": "Invalid remind_at format. Use ISO format: YYYY-MM-DDTHH:MM:SS",
                    "status": "error"
                }
            reminder = ReminderService.set_reminder(
                db, user_id, task.id, remind_datetime
            )

        return {
            "task_id": task_id,
            "task_title": task.title,
            "remind_at": reminder.remind_at.isoformat(),
            "due_date": task.due_date.isoformat(),
            "status": "reminder_set",
            "message": f"Reminder set for task #{task_id} '{task.title}'"
        }
    except Exception as e:
        db.rollback()
        error_msg = str(e)
        logging.error(f"Error setting reminder for task {task_id}, user {user_id}: {error_msg}")
        return {
            "error": f"Failed to set reminder: {error_msg}",
            "status": "error"
        }


def delete_reminder(
    user_id: str,
    task_id: Union[str, int],
    db: Session = None
) -> Dict[str, Any]:
    """Delete a reminder from a task.

    Args:
        user_id: The ID of the user
        task_id: The task number (1, 2, 3...) or UUID to remove reminder from
        db: Database session (injected by MCP server)

    Returns:
        Dictionary with status on success
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

        from app.services.reminder_service import ReminderService

        deleted = ReminderService.delete_reminder(db, user_id, task.id)

        if deleted:
            return {
                "task_id": task_id,
                "task_title": task.title,
                "status": "reminder_deleted",
                "message": f"Reminder removed from task #{task_id} '{task.title}'"
            }
        else:
            return {
                "task_id": task_id,
                "status": "no_reminder",
                "message": f"Task #{task_id} has no reminder set"
            }
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting reminder for task {task_id}, user {user_id}: {str(e)}")
        return {
            "error": f"Failed to delete reminder: {str(e)}",
            "status": "error"
        }