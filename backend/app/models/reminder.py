"""Reminder SQLModel entity for task reminders."""

from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import SQLModel, Field
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Reminder(SQLModel, table=True):
    """Reminder entity for task due date notifications.

    Users can set reminders for tasks with due dates.
    When remind_at time is reached, a reminder event is published to Kafka.
    """

    __tablename__ = "reminders"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique reminder identifier",
    )

    # Task Reference (Foreign Key) - matches tasks.id UUID type
    task_id: uuid.UUID = Field(
        description="Task UUID reference",
        index=True,
        sa_column_args=[ForeignKey("tasks.id", ondelete="CASCADE")],
    )

    # Reminder Time
    remind_at: datetime = Field(
        description="When to send reminder (UTC timestamp)",
        index=True,
    )

    # Status
    sent: bool = Field(
        default=False,
        description="Whether reminder has been sent",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When reminder was created (UTC timestamp)",
    )
