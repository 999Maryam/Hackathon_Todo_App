"""Pydantic schemas for RecurringConfig operations."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.enums import RecurringFrequency


class RecurringConfigCreate(BaseModel):
    """Schema for creating a recurring configuration."""

    frequency: str = Field(
        description="Recurrence frequency: daily, weekly, monthly",
    )
    next_occurrence: Optional[datetime] = Field(
        default=None,
        description="First occurrence date (defaults to due_date if not provided)",
    )


class RecurringConfig(BaseModel):
    """Schema for recurring config responses."""

    id: int = Field(description="Unique recurring config identifier")
    frequency: str = Field(description="Recurrence frequency: daily, weekly, monthly")
    next_occurrence: datetime = Field(description="Next scheduled occurrence (UTC)")
    created_at: datetime = Field(description="When config was created (UTC)")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
