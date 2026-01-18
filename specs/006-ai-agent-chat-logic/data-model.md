# Data Model: AI Agent & Chat Logic

**Feature**: 007-ai-agent-chat-logic
**Date**: 2026-01-14

---

## Overview

This feature introduces **no new database tables**. It uses existing entities from Spec 1 (Conversation, Message) and Spec 2 (Task). The data model focuses on runtime entities for agent execution.

---

## Existing Database Entities (Referenced)

### Conversation (from Spec 1)
```
conversations
├── id: int (PK, auto-increment)
├── user_id: str (FK → users.id)
├── created_at: datetime
└── updated_at: datetime

Index: ix_conversation_user (user_id)
```

### Message (from Spec 1)
```
messages
├── id: int (PK, auto-increment)
├── conversation_id: int (FK → conversations.id)
├── user_id: str (FK → users.id)
├── role: str ("user" | "assistant")
├── content: text
└── created_at: datetime

Index: ix_message_conversation_created (conversation_id, created_at)
Index: ix_message_user (user_id)
Constraint: valid_message_role (role IN ('user', 'assistant'))
```

### Task (from Phase II)
```
tasks
├── id: int (PK)
├── user_id: str (FK → users.id)
├── title: str
├── description: str (nullable)
├── completed: bool
├── created_at: datetime
└── updated_at: datetime

Index: ix_task_user (user_id)
```

---

## Runtime Entities (New)

### AgentContext

Runtime context passed to tool functions via `RunContextWrapper`.

```python
class AgentContext:
    """Context data injected into tool calls."""
    user_id: str       # Authenticated user's ID
    db: Session        # Database session for queries
```

**Purpose**: Provides user isolation and database access to tools without exposing these in agent-visible parameters.

### ToolCallRecord

Record of a single tool invocation during agent execution.

```python
class ToolCallRecord(BaseModel):
    """Pydantic model for tool call logging."""
    name: str           # Tool name (e.g., "add_task")
    arguments: dict     # Arguments passed to tool
    result: dict        # Tool return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "add_task",
                "arguments": {"title": "Buy groceries"},
                "result": {"task_id": 1, "status": "created", "title": "Buy groceries"}
            }
        }
```

**Purpose**: Captures tool execution details for response payload and debugging.

### AgentResponse

Response from the chat runner function.

```python
class AgentResponse(BaseModel):
    """Response from run_agent_with_tools()."""
    content: str                      # Assistant's text response
    tool_calls: list[ToolCallRecord]  # Tools invoked (may be empty)
    conversation_id: int              # Conversation ID used

    class Config:
        json_schema_extra = {
            "example": {
                "content": "Got it! I've added 'Buy groceries' to your tasks.",
                "tool_calls": [
                    {
                        "name": "add_task",
                        "arguments": {"title": "Buy groceries"},
                        "result": {"task_id": 1, "status": "created", "title": "Buy groceries"}
                    }
                ],
                "conversation_id": 42
            }
        }
```

**Purpose**: Structured response for API consumers (Spec 4 endpoint).

---

## Data Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────────┐
│            AgentContext                     │
│  user_id: "user_123"                        │
│  db: <Session>                              │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Conversation (from DB)              │
│  id: 42                                     │
│  user_id: "user_123"                        │
│  messages: [...]                            │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         OpenAI Agent Execution              │
│  - System prompt loaded                     │
│  - History provided                         │
│  - Tools available                          │
└─────────────────────────────────────────────┘
     │
     ▼ (Tool calls)
┌─────────────────────────────────────────────┐
│         ToolCallRecord[]                    │
│  [{name, arguments, result}, ...]           │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         AgentResponse                       │
│  content: "Got it! Added..."                │
│  tool_calls: [...]                          │
│  conversation_id: 42                        │
└─────────────────────────────────────────────┘
     │
     ▼
Messages saved to DB
```

---

## Validation Rules

### AgentContext
- `user_id` MUST be non-empty string
- `db` MUST be valid SQLModel Session

### ToolCallRecord
- `name` MUST be one of: add_task, list_tasks, complete_task, delete_task, update_task
- `arguments` MUST be valid JSON dict
- `result` MUST be valid JSON dict

### AgentResponse
- `content` MUST be non-empty string
- `tool_calls` MAY be empty list
- `conversation_id` MUST be positive integer

---

## No Schema Changes Required

This feature requires no database migrations because:
1. Conversation and Message tables already exist (Spec 1)
2. Task table already exists (Phase II)
3. All new entities are runtime-only (not persisted directly)

Tool call records are embedded in assistant message content or returned via API - they are not stored as separate database records.
