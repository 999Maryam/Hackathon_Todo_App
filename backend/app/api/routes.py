"""API endpoints for task management.

Phase V: Extended with tag management endpoints.
"""

import logging
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import current_user
from app.database import get_session
from app.models.schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TaskListResponse,
    ErrorResponse,
)
from app.schemas.tag import Tag as TagSchema
from app.services.task_service import TaskService
from app.services.tag_service import TagService
from app.utils.errors import ForbiddenException, NotFoundException


# Import auth routes
try:
    from app.api.auth_routes import router as auth_router
except ImportError:
    # Create a placeholder if auth_routes module doesn't exist
    from fastapi import APIRouter
    auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get(
    "/{user_id}/tasks",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
def list_tasks(
    user_id: str,
    # Phase V: Search parameter (US4)
    search: Optional[str] = None,
    # Phase V: Filter parameters (US5)
    priority: Optional[str] = None,
    completed: Optional[bool] = None,
    due_from: Optional[str] = None,
    due_to: Optional[str] = None,
    tag_ids: Optional[str] = None,
    # Phase V: Sort parameters (US6)
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "desc",
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskListResponse:
    """List all tasks for authenticated user with optional search, filter, and sort.

    Phase V: Extended with search, filter, and sort query parameters.

    Args:
        user_id: User ID from URL.
        search: Search term for title/description (ILIKE).
        priority: Comma-separated priority values to filter by (e.g., "high,medium").
        completed: Filter by completion status (true/false).
        due_from: Filter tasks due after this date (ISO format).
        due_to: Filter tasks due before this date (ISO format).
        tag_ids: Comma-separated tag IDs to filter by (e.g., "1,2,3").
        sort_by: Sort field (due_date, priority, created_at, title).
        sort_order: Sort order (asc, desc).
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TaskListResponse with list of user's tasks.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
    """
    from datetime import datetime

    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    # Parse priority filter (comma-separated string to list)
    priority_list = priority.split(",") if priority else None

    # Parse due date filters (ISO format strings to datetime)
    due_from_dt = datetime.fromisoformat(due_from) if due_from else None
    due_to_dt = datetime.fromisoformat(due_to) if due_to else None

    # Parse tag_ids filter (comma-separated string to list of ints)
    tag_ids_list = [int(t) for t in tag_ids.split(",")] if tag_ids else None

    # Phase V US6: Validate sort parameters (T076)
    valid_sort_fields = {"due_date", "priority", "created_at", "title"}
    valid_sort_orders = {"asc", "desc"}

    if sort_by and sort_by not in valid_sort_fields:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by value: {sort_by}. Must be one of: {', '.join(valid_sort_fields)}"
        )

    if sort_order and sort_order not in valid_sort_orders:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_order value: {sort_order}. Must be one of: {', '.join(valid_sort_orders)}"
        )

    logger.info(f"Listing tasks for user {user_id} (search={search}, priority={priority_list}, tags={tag_ids_list}, sort_by={sort_by}, sort_order={sort_order})")
    tasks = TaskService.get_all_tasks(
        session,
        user_id,
        search=search,
        priority=priority_list,
        completed=completed,
        due_from=due_from_dt,
        due_to=due_to_dt,
        tag_ids=tag_ids_list,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return TaskListResponse(tasks=tasks)


@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
def create_task(
    user_id: str,
    task_create: TaskCreate,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Create a new task.

    Args:
        user_id: User ID from URL.
        task_create: Task creation data.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Created TaskResponse.

    Raises:
        400 Bad Request: If validation fails.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to create tasks for this user"
        )

    logger.info(f"Creating task for user {user_id}: {task_create.title}")
    task = TaskService.create_task(session, user_id, task_create)
    return task


@router.get(
    "/{user_id}/tasks/{id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def get_task(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Get a single task by ID.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TaskResponse for the requested task.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Getting task {id} for user {user_id}")
    task = TaskService.get_task(session, user_id, id)
    return task


@router.put(
    "/{user_id}/tasks/{id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def update_task(
    user_id: str,
    id: uuid.UUID,
    task_update: TaskUpdate,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Update a task (title and/or description).

    Args:
        user_id: User ID from URL.
        id: Task ID.
        task_update: Partial task update data.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Updated TaskResponse.

    Raises:
        400 Bad Request: If validation fails.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Updating task {id} for user {user_id}")
    task = TaskService.update_task(session, user_id, id, task_update)
    return task


@router.delete(
    "/{user_id}/tasks/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def delete_task(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> None:
    """Delete a task permanently.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Deleting task {id} for user {user_id}")
    TaskService.delete_task(session, user_id, id)


@router.patch(
    "/{user_id}/tasks/{id}/complete",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def toggle_task_complete(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    """Toggle task completion status.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TaskResponse with toggled completion status.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Toggling completion for task {id} for user {user_id}")
    task = TaskService.toggle_complete(session, user_id, id)
    return task


# Phase V US3: Task tag management endpoints (T047)


@router.get(
    "/{user_id}/tasks/{id}/tags",
    response_model=List[TagSchema],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def get_task_tags(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> List[TagSchema]:
    """Get all tags assigned to a task.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        List of tags assigned to the task.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    # Verify task exists and belongs to user
    TaskService.get_task(session, user_id, id)

    logger.info(f"Getting tags for task {id}")
    return TagService.get_task_tags(session, user_id, id)


@router.post(
    "/{user_id}/tasks/{id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def add_tag_to_task(
    user_id: str,
    id: uuid.UUID,
    tag_id: int,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> None:
    """Add a tag to a task.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        tag_id: Tag ID to add.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Raises:
        400 Bad Request: If tag is already assigned to task.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task or tag doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    # Verify task exists and belongs to user
    TaskService.get_task(session, user_id, id)

    logger.info(f"Adding tag {tag_id} to task {id}")
    TagService.add_tag_to_task(session, user_id, id, tag_id)


@router.delete(
    "/{user_id}/tasks/{id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def remove_tag_from_task(
    user_id: str,
    id: uuid.UUID,
    tag_id: int,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> None:
    """Remove a tag from a task.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        tag_id: Tag ID to remove.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task, tag, or association doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    # Verify task exists and belongs to user
    TaskService.get_task(session, user_id, id)

    logger.info(f"Removing tag {tag_id} from task {id}")
    TagService.remove_tag_from_task(session, user_id, id, tag_id)


# Phase V US8: Task reminder endpoints (T097)


from pydantic import BaseModel, Field
from app.services.reminder_service import ReminderService
from app.schemas.reminder import Reminder as ReminderSchema


class SetReminderRequest(BaseModel):
    """Request body for setting a reminder."""
    minutes_before: int = Field(
        ...,
        gt=0,
        description="Minutes before due_date to send reminder (e.g., 60 for 1 hour, 1440 for 1 day)"
    )


@router.post(
    "/{user_id}/tasks/{id}/reminder",
    response_model=ReminderSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - no due date or invalid time"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def set_task_reminder(
    user_id: str,
    id: uuid.UUID,
    request: SetReminderRequest,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> ReminderSchema:
    """Set a reminder for a task.

    Creates or updates a reminder that will trigger N minutes before the task's due date.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        request: Reminder configuration (minutes_before due date).
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Created or updated Reminder.

    Raises:
        400 Bad Request: If task has no due date or reminder time is invalid.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Setting reminder for task {id}: {request.minutes_before} minutes before")
    reminder = ReminderService.set_reminder_minutes_before(
        session, user_id, id, request.minutes_before
    )
    return reminder


@router.get(
    "/{user_id}/tasks/{id}/reminder",
    response_model=Optional[ReminderSchema],
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def get_task_reminder(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> Optional[ReminderSchema]:
    """Get the reminder for a task.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Reminder if exists, null otherwise.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    # Verify task exists and belongs to user
    TaskService.get_task(session, user_id, id)

    return ReminderService.get_reminder_by_task(session, id)


@router.delete(
    "/{user_id}/tasks/{id}/reminder",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def delete_task_reminder(
    user_id: str,
    id: uuid.UUID,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> None:
    """Delete the reminder for a task.

    Args:
        user_id: User ID from URL.
        id: Task ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If task doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Deleting reminder for task {id}")
    ReminderService.delete_reminder(session, user_id, id)
