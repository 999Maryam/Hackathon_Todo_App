"""Task SQLModel entity for database storage."""

from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey
# Don't import User here to avoid circular imports during table creation
# User will be referenced by string in the relationship


class Task(SQLModel, table=True):
    """Task entity for database storage.

    Represents a single todo item with multi-user isolation via user_id.
    """

    __tablename__ = "tasks"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique task identifier",
    )

    # User Reference (Foreign Key)
    user_id: str = Field(
        description="Owner of this task (from JWT user_id claim)",
        index=True,
        sa_column_args=[ForeignKey("users.id")],
    )

    # Task Content
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required)",
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional)",
    )

    # Status
    completed: bool = Field(
        default=False,
        description="Completion status: False (open) or True (completed)",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was created (UTC timestamp)",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was last modified (UTC timestamp)",
    )

