"""API endpoints for tag management.

Phase V US3: Tag CRUD endpoints with user isolation.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import current_user
from app.database import get_session
from app.schemas.tag import (
    Tag,
    TagCreate,
    TagUpdate,
    TagWithCount,
    TagListResponse,
)
from app.models.schemas import ErrorResponse
from app.services.tag_service import TagService
from app.utils.errors import ForbiddenException


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Tags"])


@router.get(
    "/{user_id}/tags",
    response_model=TagListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
def list_tags(
    user_id: str,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TagListResponse:
    """List all tags for authenticated user with task counts.

    Args:
        user_id: User ID from URL.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TagListResponse with list of user's tags including task counts.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tags"
        )

    logger.info(f"Listing tags for user {user_id}")
    tags = TagService.get_user_tags(session, user_id)
    return TagListResponse(tags=tags)


@router.post(
    "/{user_id}/tags",
    response_model=Tag,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
)
def create_tag(
    user_id: str,
    tag_create: TagCreate,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> Tag:
    """Create a new tag.

    Args:
        user_id: User ID from URL.
        tag_create: Tag creation data.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Created Tag.

    Raises:
        400 Bad Request: If tag name already exists for user.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to create tags for this user"
        )

    logger.info(f"Creating tag for user {user_id}: {tag_create.name}")
    tag = TagService.create_tag(session, user_id, tag_create)
    return tag


@router.get(
    "/{user_id}/tags/{tag_id}",
    response_model=TagWithCount,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def get_tag(
    user_id: str,
    tag_id: int,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> TagWithCount:
    """Get a single tag by ID with task count.

    Args:
        user_id: User ID from URL.
        tag_id: Tag ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        TagWithCount for the requested tag.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If tag doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tags"
        )

    logger.info(f"Getting tag {tag_id} for user {user_id}")
    return TagService.get_tag_with_count(session, user_id, tag_id)


@router.put(
    "/{user_id}/tags/{tag_id}",
    response_model=Tag,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def update_tag(
    user_id: str,
    tag_id: int,
    tag_update: TagUpdate,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> Tag:
    """Update a tag name.

    Args:
        user_id: User ID from URL.
        tag_id: Tag ID.
        tag_update: Partial tag update data.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Returns:
        Updated Tag.

    Raises:
        400 Bad Request: If new name already exists for user.
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If tag doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tags"
        )

    logger.info(f"Updating tag {tag_id} for user {user_id}")
    return TagService.update_tag(session, user_id, tag_id, tag_update)


@router.delete(
    "/{user_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
    },
)
def delete_tag(
    user_id: str,
    tag_id: int,
    authenticated_user: str = Depends(current_user),
    session: Session = Depends(get_session),
) -> None:
    """Delete a tag permanently.

    Note: All task associations are removed automatically.

    Args:
        user_id: User ID from URL.
        tag_id: Tag ID.
        authenticated_user: User ID from JWT token.
        session: Database session.

    Raises:
        403 Forbidden: If user_id in URL doesn't match authenticated user.
        404 Not Found: If tag doesn't exist.
    """
    if user_id != authenticated_user:
        raise ForbiddenException(
            "You do not have permission to access these tags"
        )

    logger.info(f"Deleting tag {tag_id} for user {user_id}")
    TagService.delete_tag(session, user_id, tag_id)
