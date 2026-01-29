"""Pydantic schemas for Tag operations."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    """Schema for creating a new tag via POST /api/{user_id}/tags."""

    name: str = Field(
        min_length=1,
        max_length=50,
        description="Tag name (required, 1-50 characters, unique per user)",
    )


class TagUpdate(BaseModel):
    """Schema for updating an existing tag via PUT /api/{user_id}/tags/{id}."""

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="New tag name (optional, 1-50 characters if provided)",
    )


class Tag(BaseModel):
    """Schema for tag responses."""

    id: int = Field(description="Unique tag identifier")
    user_id: str = Field(description="Tag owner (from JWT user_id)")
    name: str = Field(description="Tag name")
    created_at: datetime = Field(description="When tag was created (UTC)")

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class TagWithCount(Tag):
    """Tag with associated task count."""

    task_count: int = Field(
        default=0,
        description="Number of tasks with this tag",
    )


class TagWithTasks(Tag):
    """Tag with list of associated task IDs."""

    task_ids: List[str] = Field(
        default_factory=list,
        description="List of task UUIDs with this tag",
    )


class TagListResponse(BaseModel):
    """Response for GET /api/{user_id}/tags (list all tags)."""

    tags: List[TagWithCount] = Field(description="List of tags with task counts")

    class Config:
        """Pydantic configuration."""
        from_attributes = True
