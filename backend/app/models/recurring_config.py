"""RecurringConfig SQLModel entity for recurring task patterns."""

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field

from app.models.enums import RecurringFrequency


class RecurringConfig(SQLModel, table=True):
    """RecurringConfig entity for recurring task patterns.

    Stores the recurrence pattern for tasks that repeat on a schedule.
    When a recurring task is completed, a new task instance is created
    with the next_occurrence date.
    """

    __tablename__ = "recurring_configs"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique recurring config identifier",
    )

    # Recurrence Pattern
    frequency: str = Field(
        max_length=20,
        description="Recurrence frequency: daily, weekly, monthly",
    )

    # Next Scheduled Date
    next_occurrence: datetime = Field(
        description="Next scheduled occurrence date (UTC timestamp)",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When config was created (UTC timestamp)",
    )
