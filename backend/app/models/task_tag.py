"""TaskTag SQLModel entity for many-to-many relationship between tasks and tags."""

import uuid

from sqlmodel import SQLModel, Field
from sqlalchemy import ForeignKey


class TaskTag(SQLModel, table=True):
    """TaskTag junction table for Task-Tag many-to-many relationship.

    Represents the association between a task and a tag.
    Composite primary key on (task_id, tag_id).
    """

    __tablename__ = "task_tags"

    # Composite Primary Key - task_id matches tasks.id UUID type
    task_id: uuid.UUID = Field(
        primary_key=True,
        description="Task UUID reference",
        sa_column_args=[ForeignKey("tasks.id", ondelete="CASCADE")],
    )

    tag_id: int = Field(
        primary_key=True,
        description="Tag ID reference",
        sa_column_args=[ForeignKey("tags.id", ondelete="CASCADE")],
        index=True,  # Index for reverse lookups (find tasks by tag)
    )
