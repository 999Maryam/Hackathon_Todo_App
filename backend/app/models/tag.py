"""Tag SQLModel entity for task categorization."""

from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
import uuid

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import ForeignKey, UniqueConstraint

if TYPE_CHECKING:
    from app.models.task import Task


class Tag(SQLModel, table=True):
    """Tag entity for task categorization.

    Users can create custom tags to organize their tasks.
    Each tag belongs to a single user (multi-tenant isolation).
    """

    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_tags_user_name"),
    )

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique tag identifier",
    )

    # User Reference (Foreign Key)
    user_id: str = Field(
        description="Owner of this tag (from JWT user_id claim)",
        index=True,
        sa_column_args=[ForeignKey("users.id")],
    )

    # Tag Content
    name: str = Field(
        min_length=1,
        max_length=50,
        description="Tag name (unique per user, 1-50 characters)",
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When tag was created (UTC timestamp)",
    )

    # Relationships (for ORM queries)
    # tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)
