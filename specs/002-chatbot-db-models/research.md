# Research: Database Models & Persistence Layer

**Feature**: 001-chatbot-db-models
**Date**: 2026-01-14
**Status**: Complete

---

## Research Questions & Decisions

### RQ-001: Timestamp Implementation Strategy

**Question**: How should timestamps be implemented for consistency and timezone safety?

**Decision**: Use `server_default=func.now()` with SQLAlchemy's `func.now()` for database-level defaults.

**Rationale**:
- Database-level defaults ensure consistency across all insert methods
- Timezone-safe when using PostgreSQL's `TIMESTAMP WITH TIME ZONE`
- More reliable than Python's `datetime.utcnow()` for concurrent operations
- Matches Phase II pattern while improving reliability

**Alternatives Considered**:
- `default_factory=datetime.utcnow`: Application-level, can drift from actual insert time
- `onupdate=datetime.utcnow`: Good for updated_at but SQLAlchemy-specific

**Implementation**:
```python
from sqlalchemy import func
from sqlalchemy import Column, DateTime

created_at: datetime = Field(
    sa_column=Column(DateTime(timezone=True), server_default=func.now())
)
```

---

### RQ-002: Message Content Field Type

**Question**: Should message.content use `String(n)` with length limit or `Text` type?

**Decision**: Use `Text` type (unlimited length).

**Rationale**:
- AI assistant responses can be very long (code blocks, explanations)
- User prompts can include pasted content
- PostgreSQL TEXT has no performance penalty vs VARCHAR
- Simplifies validation (no arbitrary truncation)

**Alternatives Considered**:
- `String(4000)`: Arbitrary limit that could truncate valid responses
- `String(65535)`: MySQL-style limit, unnecessary for PostgreSQL

**Implementation**:
```python
from sqlalchemy import Text

content: str = Field(sa_column=Column(Text, nullable=False))
```

---

### RQ-003: Role Field Validation

**Question**: How to enforce role is only "user" or "assistant"?

**Decision**: Use `Literal["user", "assistant"]` with Pydantic validation + database CHECK constraint.

**Rationale**:
- Pydantic `Literal` provides compile-time type safety
- Database CHECK constraint provides data integrity at storage level
- Double validation prevents invalid data from any source

**Alternatives Considered**:
- Python Enum: More complex, requires serialization handling
- String with validator: Runtime-only, no type hints
- Database ENUM type: PostgreSQL-specific, migration complexity

**Implementation**:
```python
from typing import Literal
from sqlalchemy import CheckConstraint

class Message(SQLModel, table=True):
    role: Literal["user", "assistant"]

    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant')", name="valid_role"),
    )
```

---

### RQ-004: Message Ordering Strategy

**Question**: How to ensure reliable message ordering for AI context?

**Decision**: Always order by `created_at ASC` with composite index on `(conversation_id, created_at)`.

**Rationale**:
- Chronological order is essential for natural language context
- Composite index enables efficient single-query retrieval
- ASC order means oldest first (correct for conversation flow)
- No need for explicit sequence number (timestamps sufficient)

**Alternatives Considered**:
- Sequence number column: Extra complexity, timestamps sufficient
- Order by ID: IDs may not reflect actual creation order in concurrent scenarios

**Implementation**:
```python
from sqlalchemy import Index

__table_args__ = (
    Index("ix_message_conversation_created", "conversation_id", "created_at"),
)
```

---

### RQ-005: Index Strategy

**Question**: Which indexes are needed for optimal query performance?

**Decision**: Three indexes:
1. `conversation.user_id` - Fast user conversation lookup
2. `message.conversation_id + message.created_at` - Fast ordered message retrieval
3. `message.user_id` - Fast user message ownership validation

**Rationale**:
- Primary query patterns: get conversations for user, get messages for conversation
- Composite index covers both filtering and ordering in single scan
- user_id indexes enable efficient ownership validation

**Implementation**:
```python
# Conversation model
user_id: str = Field(index=True, foreign_key="users.id")

# Message model
__table_args__ = (
    Index("ix_message_conversation_created", "conversation_id", "created_at"),
    Index("ix_message_user", "user_id"),
)
```

---

### RQ-006: Helper Function Return Types

**Question**: Should helpers return model objects or dictionaries?

**Decision**: Return full model objects for mutations, `list[dict]` for `get_conversation_history()`.

**Rationale**:
- Model objects: Full ORM functionality for mutations
- Dict for history: Matches OpenAI API message format directly
- `{"role": "user", "content": "..."}` ready for agent consumption

**Alternatives Considered**:
- Always return models: Requires serialization at API layer
- Always return dicts: Loses ORM benefits for mutations

**Implementation**:
```python
def get_conversation_history(conversation_id: int, user_id: str, db: Session) -> list[dict]:
    """Returns messages in OpenAI format: [{"role": ..., "content": ...}]"""
    return [{"role": m.role, "content": m.content} for m in messages]
```

---

### RQ-007: Auto-Create Conversation Behavior

**Question**: Should `get_or_create_conversation` create new conversation when none exists?

**Decision**: Yes, auto-create new conversation if none exists for the user.

**Rationale**:
- Simplifies chat API implementation (no separate "start conversation" endpoint)
- User gets seamless experience - just start typing
- Matches expected chatbot UX patterns

**Alternatives Considered**:
- Require explicit creation: Extra API call, worse UX
- Return None if not exists: Caller must handle creation logic

**Implementation**:
```python
def get_or_create_conversation(user_id: str, db: Session) -> Conversation:
    conversation = db.exec(
        select(Conversation).where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    ).first()

    if not conversation:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    return conversation
```

---

## Technology Verification

### SQLModel with PostgreSQL

**Verified**: SQLModel works with Neon PostgreSQL via existing Phase II setup.
- Engine configuration in `backend/app/database.py`
- Session management via `get_session()` dependency
- Schema sync via `SQLModel.metadata.create_all(engine)`

### Alembic Migrations

**Verified**: Alembic is available for schema migrations if needed.
- Can use `alembic revision --autogenerate` for new tables
- Alternative: Direct `create_all()` for simple additions

### Phase II Compatibility

**Verified**: Existing models (User, Task) will not be affected.
- New models in separate files (conversation.py, message.py)
- Foreign keys reference existing `users.id`
- No modifications to existing tables

---

## Summary

All research questions resolved. No clarifications needed - user input was comprehensive.

**Key Decisions**:
1. Use `func.now()` for timezone-safe timestamps
2. Use `Text` type for unlimited message content
3. Use `Literal` + CHECK constraint for role validation
4. Use composite index for message ordering
5. Return model objects for mutations, dicts for history
6. Auto-create conversations for seamless UX
