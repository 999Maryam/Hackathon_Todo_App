# Service Contract: Conversation & Message Persistence

**Feature**: 001-chatbot-db-models
**Date**: 2026-01-14
**Type**: Internal Service Layer (not HTTP API)

---

## Overview

This contract defines the helper functions for conversation and message persistence.
These are **internal service functions**, not HTTP endpoints. They will be consumed
by the Chat API endpoint in Phase III - Spec 4.

---

## Service Interface

### Location

```
backend/app/services/conversation_service.py
```

---

## Function Contracts

### create_conversation

Creates a new conversation for a user.

**Signature**:
```python
def create_conversation(user_id: str, db: Session) -> Conversation
```

**Parameters**:
| Name    | Type    | Required | Description                    |
| ------- | ------- | -------- | ------------------------------ |
| user_id | str     | Yes      | Authenticated user's ID        |
| db      | Session | Yes      | SQLModel database session      |

**Returns**: `Conversation` - The newly created conversation object

**Behavior**:
1. Create new Conversation with user_id
2. Commit to database
3. Refresh and return conversation

**Errors**:
| Condition            | Behavior                              |
| -------------------- | ------------------------------------- |
| Invalid user_id      | Database FK constraint error          |
| Database error       | Raises SQLAlchemy exception           |

---

### get_conversation

Retrieves a specific conversation by ID with ownership validation.

**Signature**:
```python
def get_conversation(conversation_id: int, user_id: str, db: Session) -> Conversation | None
```

**Parameters**:
| Name            | Type    | Required | Description                    |
| --------------- | ------- | -------- | ------------------------------ |
| conversation_id | int     | Yes      | Conversation ID to retrieve    |
| user_id         | str     | Yes      | Authenticated user's ID        |
| db              | Session | Yes      | SQLModel database session      |

**Returns**: `Conversation | None` - Conversation if found and owned by user, else None

**Behavior**:
1. Query conversation by ID
2. Validate user_id matches conversation.user_id
3. Return conversation or None

**Security**: Always filters by user_id to prevent cross-user access.

---

### get_or_create_conversation

Gets the most recent conversation for a user, or creates a new one.

**Signature**:
```python
def get_or_create_conversation(user_id: str, db: Session) -> Conversation
```

**Parameters**:
| Name    | Type    | Required | Description                    |
| ------- | ------- | -------- | ------------------------------ |
| user_id | str     | Yes      | Authenticated user's ID        |
| db      | Session | Yes      | SQLModel database session      |

**Returns**: `Conversation` - Existing or newly created conversation

**Behavior**:
1. Query for most recent conversation by user_id (ORDER BY updated_at DESC)
2. If found, return existing conversation
3. If not found, create new conversation and return it

**Use Case**: Chat API calls this to get active conversation without requiring explicit conversation management.

---

### add_user_message

Adds a user message to a conversation.

**Signature**:
```python
def add_user_message(
    conversation_id: int,
    user_id: str,
    content: str,
    db: Session
) -> Message
```

**Parameters**:
| Name            | Type    | Required | Description                    |
| --------------- | ------- | -------- | ------------------------------ |
| conversation_id | int     | Yes      | Target conversation ID         |
| user_id         | str     | Yes      | Authenticated user's ID        |
| content         | str     | Yes      | Message content (non-empty)    |
| db              | Session | Yes      | SQLModel database session      |

**Returns**: `Message` - The created message object

**Behavior**:
1. Validate conversation exists and belongs to user
2. Validate content is non-empty
3. Create message with role="user"
4. Update conversation.updated_at
5. Commit and return message

**Errors**:
| Condition            | Behavior                              |
| -------------------- | ------------------------------------- |
| Empty content        | Raises ValueError                     |
| Conversation not found| Raises ValueError                    |
| Wrong user           | Raises ValueError ("Access denied")   |

---

### add_assistant_message

Adds an assistant message to a conversation.

**Signature**:
```python
def add_assistant_message(
    conversation_id: int,
    user_id: str,
    content: str,
    db: Session
) -> Message
```

**Parameters**:
| Name            | Type    | Required | Description                    |
| --------------- | ------- | -------- | ------------------------------ |
| conversation_id | int     | Yes      | Target conversation ID         |
| user_id         | str     | Yes      | Authenticated user's ID        |
| content         | str     | Yes      | Assistant response (non-empty) |
| db              | Session | Yes      | SQLModel database session      |

**Returns**: `Message` - The created message object

**Behavior**:
1. Validate conversation exists and belongs to user
2. Validate content is non-empty
3. Create message with role="assistant"
4. Update conversation.updated_at
5. Commit and return message

**Errors**: Same as add_user_message

---

### get_conversation_history

Retrieves all messages for a conversation in chronological order.

**Signature**:
```python
def get_conversation_history(
    conversation_id: int,
    user_id: str,
    db: Session
) -> list[dict]
```

**Parameters**:
| Name            | Type    | Required | Description                    |
| --------------- | ------- | -------- | ------------------------------ |
| conversation_id | int     | Yes      | Target conversation ID         |
| user_id         | str     | Yes      | Authenticated user's ID        |
| db              | Session | Yes      | SQLModel database session      |

**Returns**: `list[dict]` - Messages in OpenAI format

**Response Format**:
```python
[
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there! How can I help?"},
    {"role": "user", "content": "List my tasks"},
    {"role": "assistant", "content": "Here are your tasks: ..."}
]
```

**Behavior**:
1. Query messages WHERE conversation_id AND user_id match
2. Order by created_at ASC (oldest first)
3. Transform to list of {"role": ..., "content": ...} dicts

**Security**: Always filters by user_id to prevent cross-user access.

**Edge Cases**:
| Condition                | Returns                              |
| ------------------------ | ------------------------------------ |
| Non-existent conversation| Empty list `[]`                      |
| Wrong user_id            | Empty list `[]`                      |
| No messages yet          | Empty list `[]`                      |

---

## Usage Example

```python
from app.services.conversation_service import (
    get_or_create_conversation,
    add_user_message,
    add_assistant_message,
    get_conversation_history
)
from app.database import get_session

# In Chat API endpoint
def handle_chat(user_id: str, user_message: str, db: Session):
    # Get or create conversation
    conversation = get_or_create_conversation(user_id, db)

    # Add user message
    add_user_message(conversation.id, user_id, user_message, db)

    # Get history for AI context
    history = get_conversation_history(conversation.id, user_id, db)

    # Process with AI agent (Phase III - Spec 3)
    assistant_response = ai_agent.run(history, user_message)

    # Save assistant response
    add_assistant_message(conversation.id, user_id, assistant_response, db)

    return {"response": assistant_response}
```

---

## Testing Contract

### Unit Tests

| Test Case                          | Expected Result                       |
| ---------------------------------- | ------------------------------------- |
| Create conversation                | Returns Conversation with user_id     |
| Get conversation (valid)           | Returns Conversation                  |
| Get conversation (wrong user)      | Returns None                          |
| Add user message                   | Returns Message with role="user"      |
| Add assistant message              | Returns Message with role="assistant" |
| Add message (empty content)        | Raises ValueError                     |
| Get history (valid)                | Returns ordered list[dict]            |
| Get history (wrong user)           | Returns []                            |
| Get history (10 messages)          | Returns all 10 in order               |

### Integration Tests

| Test Case                          | Expected Result                       |
| ---------------------------------- | ------------------------------------- |
| Create → Add 10 → Get history      | 10 messages in creation order         |
| User A creates, User B reads       | User B gets empty list                |
| Multiple conversations per user    | Each has independent messages         |
