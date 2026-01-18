"""Conversation SQLModel entity for chat session persistence.

Task: T003 | Spec: specs/001-chatbot-db-models/spec.md#FR-001, FR-004
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Index
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """Conversation entity for chat session persistence.

    Represents a chat session between a user and the AI assistant.
    Each conversation contains multiple messages and is strictly
    owned by a single user for multi-tenant isolation.

    Attributes:
        id: Primary key (auto-generated)
        user_id: Foreign key to users table (owner)
        created_at: Timestamp when conversation was created
        updated_at: Timestamp of last activity (message added)
        messages: Relationship to Message entities
    """

    __tablename__ = "conversations"
    __table_args__ = (
        Index("ix_conversation_user", "user_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
