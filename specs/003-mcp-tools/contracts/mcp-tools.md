# MCP Tools Contract: Task Operations

**Feature**: 002-mcp-tools
**Date**: 2026-01-14
**Protocol**: Model Context Protocol (MCP)
**Transport**: stdio (default)

---

## Overview

This document defines the contract for 5 MCP tools exposed by the Todo AI Chatbot backend. These tools enable the OpenAI agent to manage tasks on behalf of authenticated users.

---

## Tool Registry

| Tool Name | Description | Spec Reference |
|-----------|-------------|----------------|
| `add_task` | Create a new task | FR-004, FR-005, FR-006 |
| `list_tasks` | List user's tasks | FR-007, FR-008, FR-009 |
| `complete_task` | Mark task as completed | FR-010, FR-011, FR-012 |
| `delete_task` | Permanently remove task | FR-013, FR-014, FR-015 |
| `update_task` | Modify task title/description | FR-016, FR-017, FR-018 |

---

## Tool Definitions

### 1. add_task

**Description**: Create a new task for the specified user.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The authenticated user's ID"
    },
    "title": {
      "type": "string",
      "description": "Task title (required, max 255 characters)"
    },
    "description": {
      "type": "string",
      "description": "Task description (optional, max 2000 characters)"
    }
  },
  "required": ["user_id", "title"]
}
```

**Output Schema (Success)**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "UUID of the created task"
    },
    "status": {
      "type": "string",
      "enum": ["created"]
    },
    "title": {
      "type": "string",
      "description": "The task title"
    }
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Schema (Error)**:
```json
{
  "type": "object",
  "properties": {
    "error": {
      "type": "string",
      "description": "Error message"
    }
  },
  "required": ["error"]
}
```

**Example - Success**:
```json
// Input
{"user_id": "user-123", "title": "Buy groceries", "description": "Milk, eggs, bread"}

// Output
{"task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "created", "title": "Buy groceries"}
```

**Example - Error**:
```json
// Input
{"user_id": "user-123", "title": ""}

// Output
{"error": "Title is required"}
```

---

### 2. list_tasks

**Description**: List all tasks for the specified user, optionally filtered by completion status.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The authenticated user's ID"
    },
    "status": {
      "type": "string",
      "enum": ["all", "pending", "completed"],
      "default": "all",
      "description": "Filter by task status"
    }
  },
  "required": ["user_id"]
}
```

**Output Schema (Success)**:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "id": {"type": "string"},
      "title": {"type": "string"},
      "description": {"type": ["string", "null"]},
      "completed": {"type": "boolean"},
      "created_at": {"type": "string", "format": "date-time"},
      "updated_at": {"type": "string", "format": "date-time"}
    },
    "required": ["id", "title", "completed", "created_at", "updated_at"]
  }
}
```

**Example - Success**:
```json
// Input
{"user_id": "user-123", "status": "pending"}

// Output
[
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-14T10:00:00Z",
    "updated_at": "2026-01-14T10:00:00Z"
  },
  {
    "id": "b2c3d4e5-f6a7-8901-bcde-f23456789012",
    "title": "Call mom",
    "description": null,
    "completed": false,
    "created_at": "2026-01-14T11:00:00Z",
    "updated_at": "2026-01-14T11:00:00Z"
  }
]
```

**Example - Empty**:
```json
// Input
{"user_id": "user-456", "status": "all"}

// Output
[]
```

---

### 3. complete_task

**Description**: Mark a task as completed. Requires ownership validation.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "description": "UUID of the task to complete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema (Success)**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {"type": "string"},
    "status": {"type": "string", "enum": ["completed"]},
    "title": {"type": "string"}
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Schema (Error)**:
```json
{
  "type": "object",
  "properties": {
    "error": {"type": "string"}
  },
  "required": ["error"]
}
```

**Example - Success**:
```json
// Input
{"user_id": "user-123", "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}

// Output
{"task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "completed", "title": "Buy groceries"}
```

**Example - Error (Not Found/Not Owned)**:
```json
// Input
{"user_id": "user-456", "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}

// Output
{"error": "Task not found or not owned"}
```

---

### 4. delete_task

**Description**: Permanently remove a task from the database. Requires ownership validation.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "description": "UUID of the task to delete"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema (Success)**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {"type": "string"},
    "status": {"type": "string", "enum": ["deleted"]},
    "title": {"type": "string"}
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Schema (Error)**:
```json
{
  "type": "object",
  "properties": {
    "error": {"type": "string"}
  },
  "required": ["error"]
}
```

**Example - Success**:
```json
// Input
{"user_id": "user-123", "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"}

// Output
{"task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "deleted", "title": "Buy groceries"}
```

**Example - Error (Not Found/Not Owned)**:
```json
// Input
{"user_id": "user-123", "task_id": "nonexistent-id"}

// Output
{"error": "Task not found or not owned"}
```

---

### 5. update_task

**Description**: Update a task's title and/or description. Requires ownership validation.

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "user_id": {
      "type": "string",
      "description": "The authenticated user's ID"
    },
    "task_id": {
      "type": "string",
      "description": "UUID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "New task title (optional)"
    },
    "description": {
      "type": "string",
      "description": "New task description (optional)"
    }
  },
  "required": ["user_id", "task_id"]
}
```

**Output Schema (Success)**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {"type": "string"},
    "status": {"type": "string", "enum": ["updated"]},
    "title": {"type": "string"}
  },
  "required": ["task_id", "status", "title"]
}
```

**Output Schema (Error)**:
```json
{
  "type": "object",
  "properties": {
    "error": {"type": "string"}
  },
  "required": ["error"]
}
```

**Example - Success**:
```json
// Input
{"user_id": "user-123", "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "title": "Buy organic groceries"}

// Output
{"task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "status": "updated", "title": "Buy organic groceries"}
```

**Example - Error (Not Found/Not Owned)**:
```json
// Input
{"user_id": "user-456", "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "title": "Hacked!"}

// Output
{"error": "Task not found or not owned"}
```

---

## Error Codes

| Error Message | Cause | Tool(s) |
|--------------|-------|---------|
| `"Title is required"` | Empty or missing title | add_task |
| `"Task not found or not owned"` | Invalid task_id or ownership violation | complete_task, delete_task, update_task |
| `"User ID is required"` | Empty or missing user_id | All tools |

---

## Security Guarantees

1. **User Isolation**: All tools filter by `user_id` - users cannot access others' tasks
2. **No Data Leakage**: Error messages do not reveal whether task exists for other users
3. **Ownership Validation**: Mutation operations verify ownership before proceeding
4. **Stateless**: No session data - each call is independent

---

## MCP Server Configuration

**Server Name**: `todo-task-tools`
**Transport**: stdio (default)
**Entry Point**: `python -m app.tools.mcp_server`

---

## Integration Notes

### For Spec 3 (OpenAI Agent)

The agent will connect to this MCP server to execute task operations. The agent:
1. Extracts `user_id` from JWT token
2. Passes `user_id` to each tool call
3. Interprets tool responses (success or error)
4. Formats responses for user in natural language

### For Testing

Tools can be tested directly by importing functions from `app.tools.task_tools`:
```python
from app.tools.task_tools import add_task, list_tasks, complete_task, delete_task, update_task
```
