# Data Model: Chat Endpoint & Beautiful Responsive Chat UI

**Feature**: 008-chat-endpoint-ui
**Date**: 2026-01-15

---

## Overview

This feature reuses existing database entities from previous phases (Conversation, Message from Spec 1) and introduces runtime entities for API requests and responses. The data model focuses on chat-specific runtime structures while leveraging existing persistent entities.

---

## Reused Database Entities (from Spec 1)

### Conversation
```
conversations
├── id: int (PK, auto-increment)
├── user_id: str (FK → users.id)
├── created_at: datetime
└── updated_at: datetime

Index: ix_conversation_user (user_id)
```

### Message
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

---

## Runtime Entities (New)

### ChatRequest
Request payload for the chat endpoint.

```python
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: int | None = None  # Optional - creates new if None
    message: str                        # User's message to AI

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 42,
                "message": "Add a task to buy groceries"
            }
        }
```

**Purpose**: Defines the expected input format for the chat API endpoint.

### ChatResponse
Response payload from the chat endpoint.

```python
class ToolCallRecord(BaseModel):
    """Record of a tool invocation during agent execution."""
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


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int              # ID of the conversation used
    response: str                     # AI's response to the user
    tool_calls: list[ToolCallRecord]  # Tools invoked (may be empty)

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 42,
                "response": "Got it! I've added 'Buy groceries' to your tasks.",
                "tool_calls": [
                    {
                        "name": "add_task",
                        "arguments": {"title": "Buy groceries"},
                        "result": {"task_id": 1, "status": "created", "title": "Buy groceries"}
                    }
                ]
            }
        }
```

**Purpose**: Defines the response format from the chat API endpoint with tool execution results.

---

## API Contract Schema

### Request Schema
```
POST /api/{user_id}/chat

Headers:
- Authorization: Bearer <JWT_TOKEN>

Body:
{
  "conversation_id": int | null,  // Optional conversation ID
  "message": string               // User's message to the AI
}

Validation:
- message is required and non-empty
- conversation_id must be valid if provided
- user_id must match JWT token's user_id
```

### Response Schema
```
Status: 200 OK

{
  "conversation_id": int,         // ID of the conversation used/created
  "response": string,             // AI's response text
  "tool_calls": [                // Array of tools executed (may be empty)
    {
      "name": string,             // Tool name (add_task, list_tasks, etc.)
      "arguments": object,        // Arguments passed to the tool
      "result": object            // Result returned by the tool
    }
  ]
}
```

### Error Responses
```
401 Unauthorized:
{
  "detail": "Not authenticated"
}

403 Forbidden:
{
  "detail": "Access denied"
}

422 Validation Error:
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Data Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────────┐
│              ChatRequest                    │
│  conversation_id: 42 (optional)             │
│  message: "Add buy groceries to my list"    │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Authentication & Validation         │
│  - Verify JWT token                        │
│  - Ensure user_id matches token            │
│  - Validate request format                 │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Conversation Management             │
│  - Load existing conversation (if ID given) │
│  - Create new conversation (if ID is None) │
│  - Append user message to conversation     │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│          Gemini AI Processing               │
│  - Format conversation history for Gemini  │
│  - Send user message to Gemini agent       │
│  - Receive response and potential tool calls│
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│           Tool Execution                    │
│  - Execute tools called by Gemini          │
│  - Collect results                         │
│  - Prepare final response                  │
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Response Assembly                   │
│  - Save assistant message to conversation  │
│  - Format ChatResponse with results        │
└─────────────────────────────────────────────┘
     │
     ▼
API Response
```

---

## Validation Rules

### ChatRequest
- `message` MUST be non-empty string
- `conversation_id` MUST be positive integer if provided
- `user_id` in JWT token MUST match the authenticated user

### ChatResponse
- `conversation_id` MUST be positive integer
- `response` MUST be non-empty string
- `tool_calls` MAY be empty array
- Each `ToolCallRecord` MUST have valid name, arguments, and result

### Conversation Isolation
- Users CAN ONLY access their OWN conversations
- All database queries MUST include user_id filter
- Invalid conversation_id returns 403 Forbidden

---

## No Schema Changes Required

This feature requires no database migrations because:
1. Conversation and Message tables already exist (Spec 1)
2. All new entities are runtime-only (not persisted directly)
3. Tool call records are embedded in response payload rather than stored separately

The existing conversation/message structure provides all needed persistence capabilities.