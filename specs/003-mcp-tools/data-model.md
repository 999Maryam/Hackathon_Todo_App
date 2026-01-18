# Data Model: MCP Tools Server & Task Operations

**Feature**: 002-mcp-tools
**Date**: 2026-01-14

---

## Overview

This feature does NOT create new database entities. It reuses the existing Phase II `Task` model for all operations. This document describes the existing model and how MCP tools interact with it.

---

## Existing Entity: Task (Phase II)

**Source**: `backend/app/models/task.py`

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, auto-generated | Unique task identifier |
| user_id | str | FK → users.id, indexed | Owner of this task |
| title | str | required, max 255 chars | Task title |
| description | str | optional, max 2000 chars | Task description |
| completed | bool | default False | Completion status |
| created_at | datetime | auto, UTC | Creation timestamp |
| updated_at | datetime | auto, UTC | Last modification timestamp |

### Relationships

- **User (1:N)**: Each task belongs to one user
- **Conversation**: No direct relationship (tasks managed via MCP tools, not conversation)

### Indexes

- `user_id` - For filtering tasks by owner

---

## Tool Context Model (New - In-Memory Only)

This is NOT a database model but a runtime context for MCP tools.

```python
@dataclass
class ToolContext:
    """Context passed to MCP tools via lifespan."""
    db_session_factory: Callable[[], Generator[Session, None, None]]
```

**Purpose**: Provides database session access to tools without maintaining state.

---

## Tool Input/Output Schemas

### add_task

**Input**:
```json
{
  "user_id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)"
}
```

**Output (Success)**:
```json
{
  "task_id": "string (UUID)",
  "status": "created",
  "title": "string"
}
```

**Output (Error)**:
```json
{
  "error": "Title is required"
}
```

---

### list_tasks

**Input**:
```json
{
  "user_id": "string (required)",
  "status": "string (optional: 'all'|'pending'|'completed', default 'all')"
}
```

**Output (Success)**:
```json
[
  {
    "id": "string (UUID)",
    "title": "string",
    "description": "string|null",
    "completed": false,
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
]
```

**Output (Empty)**:
```json
[]
```

---

### complete_task

**Input**:
```json
{
  "user_id": "string (required)",
  "task_id": "string (UUID, required)"
}
```

**Output (Success)**:
```json
{
  "task_id": "string (UUID)",
  "status": "completed",
  "title": "string"
}
```

**Output (Error)**:
```json
{
  "error": "Task not found or not owned"
}
```

---

### delete_task

**Input**:
```json
{
  "user_id": "string (required)",
  "task_id": "string (UUID, required)"
}
```

**Output (Success)**:
```json
{
  "task_id": "string (UUID)",
  "status": "deleted",
  "title": "string"
}
```

**Output (Error)**:
```json
{
  "error": "Task not found or not owned"
}
```

---

### update_task

**Input**:
```json
{
  "user_id": "string (required)",
  "task_id": "string (UUID, required)",
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Output (Success)**:
```json
{
  "task_id": "string (UUID)",
  "status": "updated",
  "title": "string"
}
```

**Output (Error)**:
```json
{
  "error": "Task not found or not owned"
}
```

---

## State Transitions

### Task Completion State

```
[created] --complete_task--> [completed]
     ^                            |
     |                            v
     +-----(unchanged)------------+
```

Note: `complete_task` sets `completed=True`. It does NOT toggle (per FR-011: "mark the task as completed").

### Task Lifecycle

```
[non-existent] --add_task--> [exists, incomplete]
                                    |
                     +----complete_task----+
                     v                     |
               [exists, complete]          |
                     |                     |
        +----delete_task----+   +----delete_task----+
        v                                  v
   [deleted]                          [deleted]
```

---

## Data Validation Rules

### add_task Validation

1. `user_id` - Required, non-empty string
2. `title` - Required, non-empty string, max 255 characters
3. `description` - Optional, max 2000 characters if provided

### list_tasks Validation

1. `user_id` - Required, non-empty string
2. `status` - Optional, must be one of: "all", "pending", "completed"
   - Invalid values default to "all"

### complete_task / delete_task / update_task Validation

1. `user_id` - Required, non-empty string
2. `task_id` - Required, valid UUID string

### Cross-Cutting Validation

- **User Isolation**: All operations filter by `user_id = provided_user_id`
- **Ownership Error**: Return `{"error": "Task not found or not owned"}` for:
  - Non-existent task_id
  - task_id exists but belongs to different user

---

## No New Database Changes

This feature:
- Does NOT add new tables
- Does NOT modify existing tables
- Does NOT require migrations

All operations use the existing Phase II Task model as-is.
