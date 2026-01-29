"""Pydantic schemas for Reminder operations."""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field, ConfigDict


class ReminderCreate(BaseModel):
    """Schema for setting a reminder via POST /api/{user_id}/tasks/{task_id}/reminder."""

    remind_at: datetime = Field(
        description="When to send reminder (UTC timestamp, must be before due_date)",
    )


class Reminder(BaseModel):
    """Schema for reminder responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="Unique reminder identifier")
    task_id: uuid.UUID = Field(description="Task UUID reference")
    remind_at: datetime = Field(description="When reminder will be sent (UTC)")
    sent: bool = Field(description="Whether reminder has been sent")
    created_at: datetime = Field(description="When reminder was created (UTC)")


class ReminderPreset(BaseModel):
    """Preset reminder options for frontend."""

    label: str = Field(description="Display label (e.g., '1 hour before')")
    minutes_before: int = Field(description="Minutes before due_date")
