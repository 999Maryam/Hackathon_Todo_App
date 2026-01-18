# Data Model: Database Models & Persistence Layer

**Feature**: 001-chatbot-db-models
**Date**: 2026-01-14
**Spec**: [spec.md](./spec.md)

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                                │
│  │    users     │ (existing from Phase II)                       │
│  ├──────────────┤                                                │
│  │ id (PK)      │◄───────────────────────────────────────┐       │
│  │ email        │                                        │       │
│  │ name         │                                        │       │
│  │ password_hash│                                        │       │
│  │ created_at   │                                        │       │
│  └──────────────┘                                        │       │
│         │                                                │       │
│         │ 1:N                                            │       │
│         ▼                                                │       │
│  ┌──────────────┐         ┌──────────────┐               │       │
│  │    tasks     │         │conversations │               │       │
│  ├──────────────┤         ├──────────────┤               │       │
│  │ id (PK,UUID) │         │ id (PK,int)  │               │       │
│  │ user_id (FK) │◄────────│ user_id (FK) │───────────────┤       │
│  │ title        │         │ created_at   │               │       │
│  │ description  │         │ updated_at   │               │       │
│  │ completed    │         └──────────────┘               │       │
│  │ created_at   │                │                       │       │
│  │ updated_at   │                │ 1:N                   │       │
│  └──────────────┘                ▼                       │       │
│   (existing)              ┌──────────────┐               │       │
│                           │   messages   │               │       │
│                           ├──────────────┤               │       │
│                           │ id (PK,int)  │               │       │
│                           │ conv_id (FK) │               │       │
│                           │ user_id (FK) │───────────────┘       │
│                           │ role         │                       │
│                           │ content      │                       │
│                           │ created_at   │                       │
│                           └──────────────┘                       │
│                            (new)                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Entity Definitions

### User (Existing - DO NOT MODIFY)

**Table**: `users`
**Source**: `backend/app/models/user.py`

| Field         | Type         | Constraints                    | Description                    |
| ------------- | ------------ | ------------------------------ | ------------------------------ |
| id            | str (UUID)   | PK                             | Unique user identifier         |
| email         | str          | UNIQUE, INDEX                  | User email address             |
| name          | str          | max_length=100                 | Display name                   |
| password_hash | str          | max_length=255                 | Hashed password                |
| created_at    | datetime     | default=now()                  | Account creation timestamp     |

---

### Task (Existing - DO NOT MODIFY)

**Table**: `tasks`
**Source**: `backend/app/models/task.py`

| Field       | Type         | Constraints                    | Description                    |
| ----------- | ------------ | ------------------------------ | ------------------------------ |
| id          | UUID         | PK                             | Unique task identifier         |
| user_id     | str          | FK→users.id, INDEX             | Owner reference                |
| title       | str          | min=1, max=255                 | Task title                     |
| description | str (opt)    | max=2000                       | Task description               |
| completed   | bool         | default=False                  | Completion status              |
| created_at  | datetime     | default=now()                  | Creation timestamp             |
| updated_at  | datetime     | default=now()                  | Last modification timestamp    |

---

### Conversation (NEW)

**Table**: `conversations`
**Source**: `backend/app/models/conversation.py` (to be created)

| Field      | Type     | Constraints                              | Description                    |
| ---------- | -------- | ---------------------------------------- | ------------------------------ |
| id         | int      | PK, auto-increment                       | Unique conversation identifier |
| user_id    | str      | FK→users.id, INDEX, NOT NULL             | Owner reference                |
| created_at | datetime | server_default=func.now(), NOT NULL      | Conversation start timestamp   |
| updated_at | datetime | server_default=func.now(), onupdate=now  | Last activity timestamp        |

**Indexes**:
- `ix_conversation_user_id` on `user_id` (for fast user lookup)

**Relationships**:
- `user: User` - Many-to-one relationship to User
- `messages: list[Message]` - One-to-many relationship to Message

---

### Message (NEW)

**Table**: `messages`
**Source**: `backend/app/models/message.py` (to be created)

| Field           | Type                         | Constraints                              | Description                    |
| --------------- | ---------------------------- | ---------------------------------------- | ------------------------------ |
| id              | int                          | PK, auto-increment                       | Unique message identifier      |
| conversation_id | int                          | FK→conversations.id, NOT NULL            | Parent conversation reference  |
| user_id         | str                          | FK→users.id, INDEX, NOT NULL             | Owner for access validation    |
| role            | Literal["user","assistant"]  | CHECK constraint, NOT NULL               | Message sender role            |
| content         | Text                         | NOT NULL, min_length=1                   | Message content                |
| created_at      | datetime                     | server_default=func.now(), NOT NULL      | Message timestamp              |

**Indexes**:
- `ix_message_conversation_created` on `(conversation_id, created_at)` - Composite for ordered retrieval
- `ix_message_user` on `user_id` - For ownership validation

**Constraints**:
- CHECK: `role IN ('user', 'assistant')`
- NOT NULL on content (enforced via Pydantic min_length=1)

**Relationships**:
- `conversation: Conversation` - Many-to-one relationship to Conversation
- `user: User` - Many-to-one relationship to User

---

## Validation Rules

### Conversation

| Field    | Rule                                     | Error Message                          |
| -------- | ---------------------------------------- | -------------------------------------- |
| user_id  | Required, must exist in users table      | "User not found"                       |

### Message

| Field    | Rule                                     | Error Message                          |
| -------- | ---------------------------------------- | -------------------------------------- |
| role     | Must be "user" or "assistant"            | "Role must be 'user' or 'assistant'"  |
| content  | Non-empty string (min_length=1)          | "Message content cannot be empty"     |
| user_id  | Must match conversation.user_id          | "Access denied"                        |

---

## State Transitions

### Conversation Lifecycle

```
                    ┌─────────────┐
                    │   ACTIVE    │
                    │ (messages   │
  create() ───────► │  can be     │ ◄──── add_message()
                    │  added)     │
                    └─────────────┘
```

Note: No explicit "closed" state in Phase III. Conversations remain active indefinitely.

### Message Lifecycle

```
  add_user_message()      add_assistant_message()
         │                        │
         ▼                        ▼
    ┌─────────┐              ┌───────────┐
    │  USER   │              │ ASSISTANT │
    │ MESSAGE │              │  MESSAGE  │
    └─────────┘              └───────────┘
         │                        │
         └────────────────────────┘
                    │
                    ▼
              ┌───────────┐
              │ PERSISTED │
              │ (immutable│
              │ in DB)    │
              └───────────┘
```

Note: Messages are immutable once created. No edit/delete in Phase III scope.

---

## SQLModel Class Definitions

### Conversation Model

```python
# backend/app/models/conversation.py

from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Index
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """Conversation entity for chat session persistence.

    Represents a single chat session for a user. One user can have
    multiple conversations. Each conversation contains ordered messages.

    Task: T-001 | Spec: specs/001-chatbot-db-models/spec.md#FR-001
    """

    __tablename__ = "conversations"

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # User Reference (Foreign Key with index)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Owner of this conversation"
    )

    # Timestamps with server-side defaults
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
        description="When conversation was created"
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        ),
        description="When conversation was last updated"
    )

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
# backend/app/models/message.py

from datetime import datetime
from typing import Optional, Literal, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Text, Index, CheckConstraint
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from app.models.conversation import Conversation
    from app.models.user import User


class Message(SQLModel, table=True):
    """Message entity for conversation history persistence.

    Represents a single message in a conversation. Role distinguishes
    between user input and assistant responses.

    Task: T-002 | Spec: specs/001-chatbot-db-models/spec.md#FR-002
    """

    __tablename__ = "messages"
    __table_args__ = (
        # Composite index for fast ordered retrieval
        Index("ix_message_conversation_created", "conversation_id", "created_at"),
        # Index for user ownership validation
        Index("ix_message_user", "user_id"),
        # Check constraint for role validation
        CheckConstraint("role IN ('user', 'assistant')", name="valid_message_role"),
    )

    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Conversation Reference (Foreign Key)
    conversation_id: int = Field(
        foreign_key="conversations.id",
        nullable=False,
        description="Parent conversation"
    )

    # User Reference (Foreign Key for ownership validation)
    user_id: str = Field(
        foreign_key="users.id",
        nullable=False,
        description="Owner of this message (for access validation)"
    )

    # Message Role (user or assistant)
    role: Literal["user", "assistant"] = Field(
        nullable=False,
        description="Message sender role"
    )

    # Message Content (Text type for unlimited length)
    content: str = Field(
        sa_column=Column(Text, nullable=False),
        min_length=1,
        description="Message content"
    )

    # Timestamp with server-side default
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        ),
        description="When message was created"
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
```

---

## Migration Strategy

### Approach: SQLModel Metadata Sync

For Phase III, use `SQLModel.metadata.create_all(engine)` which will:
1. Detect existing tables (users, tasks) - no changes
2. Create new tables (conversations, messages) with indexes and constraints

### Alternative: Alembic Migration

If more control needed:
```bash
cd backend
alembic revision --autogenerate -m "Add conversation and message tables"
alembic upgrade head
```

---

## Query Patterns

### Get Conversations for User
```sql
SELECT * FROM conversations
WHERE user_id = :user_id
ORDER BY updated_at DESC;
```
Uses index: `ix_conversation_user_id`

### Get Ordered Messages for Conversation
```sql
SELECT * FROM messages
WHERE conversation_id = :conversation_id
  AND user_id = :user_id
ORDER BY created_at ASC;
```
Uses index: `ix_message_conversation_created`

### Add Message to Conversation
```sql
INSERT INTO messages (conversation_id, user_id, role, content)
VALUES (:conversation_id, :user_id, :role, :content)
RETURNING *;
```
Also updates `conversations.updated_at` via helper function.
