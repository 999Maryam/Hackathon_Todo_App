"""Conversation and message persistence service.

Task: T010-T036 | Spec: specs/001-chatbot-db-models/spec.md#FR-006-FR-013

This module provides helper functions for conversation and message
management with strict multi-user isolation via user_id filtering.
"""

from datetime import datetime, timezone
from typing import Literal

from sqlmodel import Session, select

from app.models.conversation import Conversation
from app.models.message import Message

# =============================================================================
# User Story 1: Create and Persist a Conversation (T010-T012)
# =============================================================================


def create_conversation(user_id: str, db: Session) -> Conversation:
    """Create a new conversation for a user.

    Args:
        user_id: The ID of the user creating the conversation
        db: Database session

    Returns:
        Conversation: The newly created conversation object

    Raises:
        SQLAlchemyError: If database operation fails
    """
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(
    conversation_id: int, user_id: str, db: Session
) -> Conversation | None:
    """Get a conversation by ID with ownership validation.

    Args:
        conversation_id: The ID of the conversation to retrieve
        user_id: The ID of the requesting user (for ownership check)
        db: Database session

    Returns:
        Conversation | None: The conversation if found and owned by user,
                            None otherwise
    """
    return db.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    ).first()


# =============================================================================
# User Story 2: Add Messages to a Conversation (T018-T022)
# =============================================================================


def _add_message(
    conversation_id: int,
    user_id: str,
    role: Literal["user", "assistant"],
    content: str,
    db: Session
) -> Message:
    """Internal helper to add a message with validation.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user (for ownership validation)
        role: Message role ('user' or 'assistant')
        content: The message content
        db: Database session

    Returns:
        Message: The newly created message object

    Raises:
        ValueError: If content is empty or conversation not found/owned
    """
    # Validate content is not empty (FR-011)
    if not content or not content.strip():
        raise ValueError("Message content cannot be empty")

    # Verify conversation ownership (FR-013)
    conversation = get_conversation(conversation_id, user_id, db)
    if not conversation:
        raise ValueError("Conversation not found or access denied")

    # Create message
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content.strip()
    )
    db.add(message)

    # Update conversation timestamp for activity tracking
    conversation.updated_at = datetime.now(timezone.utc)
    db.add(conversation)

    db.commit()
    db.refresh(message)
    return message


def add_user_message(
    conversation_id: int, user_id: str, content: str, db: Session
) -> Message:
    """Add a user message to a conversation.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user
        content: The message content
        db: Database session

    Returns:
        Message: The newly created user message

    Raises:
        ValueError: If content is empty or conversation not found/owned
    """
    return _add_message(conversation_id, user_id, "user", content, db)


def add_assistant_message(
    conversation_id: int, user_id: str, content: str, db: Session
) -> Message:
    """Add an assistant message to a conversation.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user
        content: The message content
        db: Database session

    Returns:
        Message: The newly created assistant message

    Raises:
        ValueError: If content is empty or conversation not found/owned
    """
    return _add_message(conversation_id, user_id, "assistant", content, db)


# =============================================================================
# User Story 3: Retrieve Ordered Message History (T027-T030)
# =============================================================================


def get_conversation_history(
    conversation_id: int, user_id: str, db: Session
) -> list[dict]:
    """Get ordered message history in OpenAI-compatible format.

    Retrieves all messages for a conversation in chronological order
    (created_at ASC), formatted for direct use with OpenAI API.

    Args:
        conversation_id: The ID of the conversation
        user_id: The ID of the user (for ownership validation)
        db: Database session

    Returns:
        list[dict]: List of messages in format:
                   [{"role": "user", "content": "..."}, ...]
                   Returns empty list if conversation not found or not owned
    """
    messages = db.exec(
        select(Message)
        .where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        )
        .order_by(Message.created_at.asc())
    ).all()

    return [{"role": m.role, "content": m.content} for m in messages]


# =============================================================================
# User Story 4: Get or Create Conversation (T034-T035)
# =============================================================================


def get_or_create_conversation(user_id: str, db: Session) -> Conversation:
    """Get most recent conversation or create a new one.

    Retrieves the user's most recently updated conversation, or creates
    a new conversation if none exists. This provides a seamless chat UX
    where users don't need to explicitly create conversations.

    Args:
        user_id: The ID of the user
        db: Database session

    Returns:
        Conversation: The most recent or newly created conversation
    """
    conversation = db.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc(), Conversation.id.desc())
    ).first()

    if not conversation:
        conversation = create_conversation(user_id, db)

    return conversation
