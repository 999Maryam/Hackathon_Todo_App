"""Pydantic request and response schemas."""

from datetime import datetime
from typing import List, Optional
import uuid

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task via POST /api/{user_id}/tasks.

    Does NOT include id, timestamps, or user_id (assigned by backend).
    Phase V: Extended with priority, due_date, recurring, and tag support.
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

    # Phase V: Advanced Features
    priority: Optional[str] = Field(
        default="medium",
        description="Task priority: high, medium, low (default: medium)",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline (optional, UTC timestamp)",
    )

    is_recurring: Optional[bool] = Field(
        default=False,
        description="Whether this task repeats on a schedule",
    )

    recurring_frequency: Optional[str] = Field(
        default=None,
        description="Recurrence frequency: daily, weekly, monthly (required if is_recurring=true)",
    )

    tag_ids: Optional[List[int]] = Field(
        default=None,
        description="List of tag IDs to assign to this task",
    )

    reminder_minutes_before: Optional[int] = Field(
        default=None,
        description="Minutes before due_date to send reminder (e.g., 60 for 1 hour before)",
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task via PUT /api/{user_id}/tasks/{id}.

    All fields are optional; only provided fields are updated.
    Phase V: Extended with priority, due_date, recurring, and tag support.
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

    # Phase V: Advanced Features
    priority: Optional[str] = Field(
        default=None,
        description="Task priority: high, medium, low",
    )

    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline (UTC timestamp)",
    )

    is_recurring: Optional[bool] = Field(
        default=None,
        description="Whether this task repeats on a schedule",
    )

    recurring_frequency: Optional[str] = Field(
        default=None,
        description="Recurrence frequency: daily, weekly, monthly",
    )

    tag_ids: Optional[List[int]] = Field(
        default=None,
        description="List of tag IDs to assign (replaces existing tags)",
    )

    reminder_minutes_before: Optional[int] = Field(
        default=None,
        description="Minutes before due_date to send reminder",
    )


class TagResponse(BaseModel):
    """Embedded tag response for TaskResponse."""

    id: int = Field(description="Unique tag identifier")
    name: str = Field(description="Tag name")

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class ReminderResponse(BaseModel):
    """Embedded reminder response for TaskResponse."""

    id: int = Field(description="Unique reminder identifier")
    remind_at: datetime = Field(description="When reminder will be sent (UTC)")
    sent: bool = Field(description="Whether reminder has been sent")

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class RecurringConfigResponse(BaseModel):
    """Embedded recurring config response for TaskResponse."""

    id: int = Field(description="Unique recurring config identifier")
    frequency: str = Field(description="Recurrence frequency: daily, weekly, monthly")
    next_occurrence: datetime = Field(description="Next scheduled occurrence (UTC)")

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class TaskResponse(BaseModel):
    """Schema for task responses in all endpoints.

    Includes all task fields including id, timestamps, user_id.
    Phase V: Extended with priority, due_date, recurring config, tags, and reminder.
    """

    id: uuid.UUID = Field(description="Unique task identifier")
    user_id: str = Field(description="Task owner (from JWT user_id)")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description")
    completed: bool = Field(description="Completion status")

    # Phase V: Advanced Features
    priority: str = Field(default="medium", description="Task priority: high, medium, low")
    due_date: Optional[datetime] = Field(default=None, description="Task deadline (UTC)")
    is_recurring: bool = Field(default=False, description="Whether this task repeats")

    # Phase V: Related objects (populated from joins)
    tags: List[TagResponse] = Field(default_factory=list, description="Tags assigned to this task")
    recurring_config: Optional[RecurringConfigResponse] = Field(default=None, description="Recurring configuration")
    reminder: Optional[ReminderResponse] = Field(default=None, description="Reminder for this task")

    # Timestamps
    created_at: datetime = Field(description="When task was created (UTC)")
    updated_at: datetime = Field(description="When task was last updated (UTC)")

    class Config:
        """Pydantic configuration."""

        from_attributes = True  # Enable ORM mode for SQLModel


class TaskListResponse(BaseModel):
    """Response for GET /api/{user_id}/tasks (list all tasks).

    Phase V: Extended with pagination and filter metadata.
    """

    tasks: List[TaskResponse] = Field(description="List of tasks for user")
    total: Optional[int] = Field(default=None, description="Total count (for pagination)")
    page: Optional[int] = Field(default=None, description="Current page number")
    page_size: Optional[int] = Field(default=None, description="Items per page")

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
