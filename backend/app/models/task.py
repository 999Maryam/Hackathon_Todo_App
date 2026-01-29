"""Task SQLModel entity for database storage."""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
import uuid

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey

# Don't import User here to avoid circular imports during table creation
# User will be referenced by string in the relationship

if TYPE_CHECKING:
    from app.models.tag import Tag
    from app.models.recurring_config import RecurringConfig
    from app.models.reminder import Reminder


class Task(SQLModel, table=True):
    """Task entity for database storage.

    Represents a single todo item with multi-user isolation via user_id.
    Phase V: Extended with priority, due_date, recurring, and reminder support.
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

    # === Phase V: Advanced Features ===

    # Priority (US1)
    priority: str = Field(
        default="medium",
        max_length=10,
        description="Task priority: high, medium, low",
        index=True,
    )

    # Due Date (US2)
    due_date: Optional[datetime] = Field(
        default=None,
        description="Task deadline (UTC timestamp, optional)",
        index=True,
    )

    # Recurring (US7)
    is_recurring: bool = Field(
        default=False,
        description="Whether this task repeats on a schedule",
    )

    recurring_config_id: Optional[int] = Field(
        default=None,
        description="Reference to recurring configuration",
        sa_column_args=[ForeignKey("recurring_configs.id")],
    )

    # === Timestamps ===

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was created (UTC timestamp)",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was last modified (UTC timestamp)",
    )

    # === Relationships (for ORM queries) ===
    # Note: These are commented out to avoid circular import issues
    # They can be enabled when using proper lazy imports
    # tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
    # recurring_config: Optional["RecurringConfig"] = Relationship()
    # reminders: List["Reminder"] = Relationship(back_populates="task")

