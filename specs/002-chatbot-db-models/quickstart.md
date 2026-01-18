# Quickstart: Database Models & Persistence Layer

**Feature**: 001-chatbot-db-models
**Date**: 2026-01-14
**Time to Complete**: ~30 minutes

---

## Prerequisites

- Phase II backend running and functional
- Neon PostgreSQL database accessible
- Python virtual environment activated

---

## Step 1: Create Model Files

### 1.1 Create `backend/app/models/conversation.py`

```python
"""Conversation SQLModel entity for chat session persistence."""

from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """Conversation entity for chat session persistence.

    Task: T-001 | Spec: specs/001-chatbot-db-models/spec.md#FR-001
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    )

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
```

### 1.2 Create `backend/app/models/message.py`

```python
"""Message SQLModel entity for conversation history persistence."""

from datetime import datetime
from typing import Optional, Literal, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text, Index, CheckConstraint
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Message(SQLModel, table=True):
    """Message entity for conversation history persistence.

    Task: T-002 | Spec: specs/001-chatbot-db-models/spec.md#FR-002
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
    role: Literal["user", "assistant"] = Field(nullable=False)
    content: str = Field(sa_column=Column(Text, nullable=False), min_length=1)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

### 1.3 Update `backend/app/models/__init__.py`

Add the new imports:
```python
from app.models.conversation import Conversation
from app.models.message import Message

__all__ = [
    # ... existing exports ...
    "Conversation",
    "Message",
]
```

---

## Step 2: Create Service Layer

### 2.1 Create `backend/app/services/conversation_service.py`

```python
"""Conversation and message persistence service.

Task: T-003-T-008 | Spec: specs/001-chatbot-db-models/spec.md#FR-006-FR-010
"""

from sqlmodel import Session, select
from app.models.conversation import Conversation
from app.models.message import Message


def create_conversation(user_id: str, db: Session) -> Conversation:
    """Create a new conversation for a user."""
    conversation = Conversation(user_id=user_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation(conversation_id: int, user_id: str, db: Session) -> Conversation | None:
    """Get a conversation by ID with ownership validation."""
    return db.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
    ).first()


def get_or_create_conversation(user_id: str, db: Session) -> Conversation:
    """Get most recent conversation or create new one."""
    conversation = db.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    ).first()

    if not conversation:
        conversation = create_conversation(user_id, db)

    return conversation


def add_user_message(conversation_id: int, user_id: str, content: str, db: Session) -> Message:
    """Add a user message to a conversation."""
    return _add_message(conversation_id, user_id, "user", content, db)


def add_assistant_message(conversation_id: int, user_id: str, content: str, db: Session) -> Message:
    """Add an assistant message to a conversation."""
    return _add_message(conversation_id, user_id, "assistant", content, db)


def _add_message(conversation_id: int, user_id: str, role: str, content: str, db: Session) -> Message:
    """Internal: Add a message with validation."""
    if not content or not content.strip():
        raise ValueError("Message content cannot be empty")

    # Verify conversation ownership
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

    # Update conversation timestamp
    from datetime import datetime
    conversation.updated_at = datetime.utcnow()
    db.add(conversation)

    db.commit()
    db.refresh(message)
    return message


def get_conversation_history(conversation_id: int, user_id: str, db: Session) -> list[dict]:
    """Get ordered message history in OpenAI format."""
    messages = db.exec(
        select(Message)
        .where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        )
        .order_by(Message.created_at.asc())
    ).all()

    return [{"role": m.role, "content": m.content} for m in messages]
```

---

## Step 3: Sync Database Schema

Run the application to create tables:

```bash
cd backend
python -c "from app.database import create_db_and_tables; create_db_and_tables()"
```

Or start the server (tables created on startup):
```bash
uvicorn app.main:app --reload
```

---

## Step 4: Verify Setup

### 4.1 Quick Python Test

```python
# backend/verify_models.py
from app.database import SessionLocal
from app.services.conversation_service import (
    create_conversation,
    add_user_message,
    add_assistant_message,
    get_conversation_history
)

with SessionLocal() as db:
    # Use a test user_id (replace with actual user ID from your database)
    user_id = "test-user-id"

    # Create conversation
    conv = create_conversation(user_id, db)
    print(f"Created conversation: {conv.id}")

    # Add messages
    add_user_message(conv.id, user_id, "Hello!", db)
    add_assistant_message(conv.id, user_id, "Hi there! How can I help?", db)

    # Get history
    history = get_conversation_history(conv.id, user_id, db)
    print(f"History: {history}")
```

### 4.2 Expected Output

```
Created conversation: 1
History: [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there! How can I help?"}
]
```

---

## Step 5: Run Tests

```bash
cd backend
pytest tests/test_conversation.py -v
```

---

## Troubleshooting

### "relation 'conversations' does not exist"
- Run `create_db_and_tables()` or restart the server

### "FOREIGN KEY constraint failed"
- Ensure user_id exists in users table

### "CHECK constraint 'valid_message_role' violated"
- Role must be exactly "user" or "assistant"

---

## Next Steps

1. Run `/sp.tasks` to generate implementation task breakdown
2. Implement tasks via `/sp.implement`
3. Continue to Phase III - Spec 2 (MCP Tools)
