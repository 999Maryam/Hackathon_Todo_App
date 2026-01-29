"""Pydantic schemas for Kafka event publishing."""

from datetime import datetime
from typing import Dict, Any, Optional, List

from pydantic import BaseModel, Field


class TaskEvent(BaseModel):
    """Schema for task lifecycle events published to Kafka.

    Events: task_created, task_updated, task_completed, task_deleted
    Topic: task-events
    """

    event_type: str = Field(
        description="Event type: created, updated, completed, deleted",
    )
    task_id: str = Field(
        description="Task UUID",
    )
    task_data: Dict[str, Any] = Field(
        description="Task data snapshot at event time",
    )
    user_id: str = Field(
        description="Task owner (from JWT user_id)",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Event timestamp (UTC)",
    )

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskUpdateEvent(TaskEvent):
    """Extended event for task updates with change details."""

    changed_fields: List[str] = Field(
        default_factory=list,
        description="List of fields that were modified",
    )
    previous_values: Dict[str, Any] = Field(
        default_factory=dict,
        description="Previous values of changed fields",
    )


class ReminderEvent(BaseModel):
    """Schema for reminder events published to Kafka.

    Event: reminder_due
    Topic: reminders
    """

    task_id: str = Field(
        description="Task UUID",
    )
    title: str = Field(
        description="Task title for notification",
    )
    due_at: datetime = Field(
        description="Task due date (UTC)",
    )
    remind_at: datetime = Field(
        description="Scheduled reminder time (UTC)",
    )
    user_id: str = Field(
        description="Task owner (from JWT user_id)",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Event timestamp (UTC)",
    )

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
