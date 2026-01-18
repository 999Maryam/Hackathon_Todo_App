---
name: conversation-history-manager-skill
description: Handle loading and saving conversation history from/to database with user ownership validation and OpenAI message formatting.
version: 1.0.0
---

# Conversation History Manager Skill

This skill handles loading and saving conversation history from/to database.

## Purpose

Manages persistent conversation state including:
- Retrieving conversation history for a session
- Adding user and assistant messages
- Formatting messages for OpenAI agent consumption
- Enforcing user ownership on all operations
- Auto-creating conversations when needed

## Core Functions

### 1. get_conversation_history

Retrieves all messages for a conversation, formatted for OpenAI.

```python
from sqlmodel import Session, select
from typing import Optional
from app.models import Conversation, Message
from app.db import get_session

async def get_conversation_history(
    conversation_id: str,
    user_id: str,
    db: Session
) -> list[dict]:
    """
    Retrieve conversation history formatted for OpenAI agent.

    Args:
        conversation_id: UUID of the conversation
        user_id: Authenticated user ID for ownership validation
        db: Database session

    Returns:
        list[dict]: Messages in OpenAI format [{"role": ..., "content": ...}]

    Reference: Phase III Spec - Conversation Management
    """
    # Validate user authentication
    if not user_id:
        raise ValueError("User not authenticated")

    # Verify conversation ownership
    conversation = db.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    ).first()

    if not conversation:
        return []  # No history for non-existent/unauthorized conversation

    # Fetch messages ordered by creation time
    messages = db.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    ).all()

    # Format for OpenAI agent input
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

### 2. add_user_message

Adds a user message to the conversation.

```python
from datetime import datetime
from uuid import uuid4

async def add_user_message(
    conversation_id: Optional[str],
    user_id: str,
    content: str,
    db: Session
) -> dict:
    """
    Add a user message to conversation. Creates conversation if none exists.

    Args:
        conversation_id: UUID of conversation (None to create new)
        user_id: Authenticated user ID
        content: Message content from user
        db: Database session

    Returns:
        dict: {"conversation_id": str, "message_id": str}

    Reference: Phase III Spec - Message Storage
    """
    # Validate user authentication
    if not user_id:
        raise ValueError("User not authenticated")

    # Create new conversation if needed
    if not conversation_id:
        conversation = Conversation(
            id=str(uuid4()),
            user_id=user_id,
            title=content[:50] + "..." if len(content) > 50 else content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        conversation_id = conversation.id
    else:
        # Verify ownership of existing conversation
        conversation = db.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
        ).first()

        if not conversation:
            raise ValueError("Conversation not found or unauthorized")

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db.add(conversation)

    # Create user message
    message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        role="user",
        content=content,
        created_at=datetime.utcnow()
    )
    db.add(message)
    db.commit()

    return {
        "conversation_id": conversation_id,
        "message_id": message.id
    }
```

### 3. add_assistant_message

Adds an assistant response to the conversation.

```python
async def add_assistant_message(
    conversation_id: str,
    user_id: str,
    content: str,
    tool_calls: Optional[list] = None,
    db: Session = None
) -> dict:
    """
    Add an assistant message to conversation.

    Args:
        conversation_id: UUID of the conversation
        user_id: Authenticated user ID for ownership validation
        content: Assistant response content
        tool_calls: Optional list of tool calls made (for logging)
        db: Database session

    Returns:
        dict: {"message_id": str, "success": bool}

    Reference: Phase III Spec - Message Storage
    """
    # Validate user authentication
    if not user_id:
        raise ValueError("User not authenticated")

    # Verify conversation ownership
    conversation = db.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    ).first()

    if not conversation:
        raise ValueError("Conversation not found or unauthorized")

    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)

    # Create assistant message
    message = Message(
        id=str(uuid4()),
        conversation_id=conversation_id,
        role="assistant",
        content=content,
        metadata={"tool_calls": tool_calls} if tool_calls else None,
        created_at=datetime.utcnow()
    )
    db.add(message)
    db.commit()

    return {
        "message_id": message.id,
        "success": True
    }
```

## OpenAI Message Format

Messages are formatted for direct use with OpenAI's chat completion API:

```python
# Output format from get_conversation_history
[
    {"role": "user", "content": "Show my todos"},
    {"role": "assistant", "content": "Here are your todos:\n1. Buy groceries\n2. Call mom"},
    {"role": "user", "content": "Mark the first one done"},
    {"role": "assistant", "content": "Done! I've marked 'Buy groceries' as completed."}
]

# Usage with OpenAI agent
history = await get_conversation_history(conversation_id, user_id, db)
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,  # Spread conversation history
        {"role": "user", "content": new_message}
    ]
)
```

## Database Models Reference

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import json

class Conversation(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)  # Ownership filter
    title: str
    created_at: datetime
    updated_at: datetime

class Message(SQLModel, table=True):
    id: str = Field(primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str  # "user" | "assistant" | "system"
    content: str
    metadata: Optional[str] = None  # JSON string for tool_calls, etc.
    created_at: datetime
```

## Best Practices

- Always validate user_id before any database operation
- Use indexed queries on conversation_id and user_id
- Order messages by created_at for correct sequence
- Store tool_calls in metadata for debugging/audit
- Set conversation title from first user message
- Update conversation.updated_at on every new message
- Handle empty history gracefully (return empty list)
- Use transactions for multi-step operations
