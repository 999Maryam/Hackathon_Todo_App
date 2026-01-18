"""Message SQLModel entity for conversation history persistence.

Task: T004 | Spec: specs/001-chatbot-db-models/spec.md#FR-002, FR-005, FR-012
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import field_validator
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text, Index, CheckConstraint
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.conversation import Conversation

# Valid message roles
VALID_ROLES = ("user", "assistant")


class Message(SQLModel, table=True):
    """Message entity for conversation history persistence.

    Represents a single message in a conversation, either from
    the user or the AI assistant. Messages are stored with their
    role for proper context reconstruction.

    Attributes:
        id: Primary key (auto-generated)
        conversation_id: Foreign key to conversations table
        user_id: Foreign key to users table (for isolation queries)
        role: Either 'user' or 'assistant'
        content: The message text (unlimited length)
        created_at: Timestamp when message was created

    Indexes:
        - Composite index on (conversation_id, created_at) for ordered retrieval
        - Index on user_id for user isolation queries

    Constraints:
        - CHECK constraint ensures role is either 'user' or 'assistant'
    """

    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_message_conversation_created", "conversation_id", "created_at"),
        Index("ix_message_user", "user_id"),
        CheckConstraint("role IN ('user', 'assistant')", name="valid_message_role"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    role: str = Field(nullable=False)
    content: str = Field(sa_column=Column(Text, nullable=False))
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate that role is either 'user' or 'assistant'."""
        if v not in VALID_ROLES:
            raise ValueError(f"role must be one of {VALID_ROLES}, got '{v}'")
        return v
