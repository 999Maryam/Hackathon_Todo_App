"""API endpoints for task management."""

import logging
import uuid
from typing import List

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
from app.services.task_service import TaskService
from app.utils.errors import ForbiddenException, NotFoundException

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
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TaskListResponse:
    """List all tasks for authenticated user.

    Args:
        user_id: User ID from URL.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TaskListResponse with list of user's tasks.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tasks"
        )

    logger.info(f"Listing tasks for user {user_id}")
    tasks = TaskService.get_all_tasks(session, user_id)
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
