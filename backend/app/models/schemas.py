"""Pydantic request and response schemas."""

from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task via POST /api/{user_id}/tasks.

    Does NOT include id, timestamps, or user_id (assigned by backend).
    """

    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required, 1-255 characters)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional, max 2000 characters)",
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task via PUT /api/{user_id}/tasks/{id}.

    All fields are optional; only provided fields are updated.
    Note: 'completed' is NOT updatable via PUT (only via PATCH /complete).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New task title (optional, 1-255 characters if provided)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="New task description (optional, max 2000 characters if provided)",
    )


class TaskResponse(BaseModel):
    """Schema for task responses in all endpoints.

    Includes all task fields including id, timestamps, user_id.
    """

    id: uuid.UUID = Field(description="Unique task identifier")
    user_id: str = Field(description="Task owner (from JWT user_id)")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description")
    completed: bool = Field(description="Completion status")
    created_at: datetime = Field(description="When task was created (UTC)")
    updated_at: datetime = Field(description="When task was last updated (UTC)")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel


class TaskListResponse(BaseModel):
    """Response for GET /api/{user_id}/tasks (list all tasks)."""

    tasks: List[TaskResponse] = Field(description="List of tasks for user")

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response for all HTTP error status codes (400, 401, 403, 404, 500)."""

    error: str = Field(description="Human-readable error message")
    status: int = Field(description="HTTP status code")
    detail: Optional[str] = Field(
        default=None,
        description="Optional additional error details",
    )
