# Data Model: Backend API for Todo Full-Stack Web Application

**Feature**: Backend API | **Date**: 2026-01-08 | **Plan Reference**: [plan.md](plan.md)

## Overview

This document defines the data entities, relationships, validation rules, and state transitions for the Todo Backend API. All data models use SQLModel (combining SQLAlchemy + Pydantic) for type-safe database access and automatic validation.

---

## Entity: Task

The **Task** entity represents a single todo item owned by a user. It is the primary data model for this application.

### Task (Database Table Model)

**Purpose**: Persistent storage of task data in PostgreSQL

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-----------|-------------|
| `id` | UUID | Primary Key, auto-generated | Unique task identifier (gen_random_uuid()) |
| `user_id` | VARCHAR(255) | Foreign Key, NOT NULL, Indexed | Reference to task owner (from JWT user_id claim) |
| `title` | VARCHAR(255) | NOT NULL, min_length=1, max_length=255 | Task title/name |
| `description` | TEXT | NULL, max_length=2000 | Optional detailed description |
| `completed` | BOOLEAN | NOT NULL, default=FALSE | Completion status toggle |
| `created_at` | TIMESTAMP | NOT NULL, auto-set to NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMP | NOT NULL, auto-update | Last modification timestamp (UTC) |

**SQLModel Definition**:

```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    """
    Task entity for database storage.
    Represents a single todo item with multi-user isolation via user_id.
    """
    __tablename__ = "tasks"

    # Primary Key
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique task identifier"
    )

    # User Reference (Foreign Key)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of this task (from JWT user_id claim)"
    )

    # Task Content
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional)"
    )

    # Status
    completed: bool = Field(
        default=False,
        description="Completion status: False (open) or True (completed)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was created (UTC timestamp)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When task was last modified (UTC timestamp)"
    )
```

**Database Indexes**:

```sql
-- Index on user_id for fast filtering (CRITICAL for multi-user queries)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Composite index for sorted queries
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

**Validation Rules**:

- `title`: Required, non-empty, max 255 characters
  - Error: 400 Bad Request if missing or empty
  - Error: 400 Bad Request if > 255 characters

- `description`: Optional, max 2000 characters
  - Warning: Silently truncated if > 2000 characters (or return 400 based on API design)
  - Recommended: Return 400 Bad Request for clarity

- `completed`: Boolean, defaults to False
  - Error: 400 Bad Request if not boolean

- `user_id`: Must match authenticated user from JWT
  - Error: 403 Forbidden if task user_id doesn't match authenticated user
  - Note: Set automatically by backend, not user-provided

---

## Request/Response Schemas

### TaskCreate (Create Request Schema)

**Purpose**: Validate POST request body for creating new tasks

**Fields** (subset of Task, excludes id, timestamps, user_id):

```python
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    """
    Schema for creating a new task via POST /api/{user_id}/tasks
    Does NOT include id, timestamps, or user_id (assigned by backend).
    """
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required, 1-255 characters)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Task description (optional, max 2000 characters)"
    )
```

**Validation Example**:

```python
# Valid
TaskCreate(title="Buy groceries", description="Milk, eggs, bread")

# Valid (minimal)
TaskCreate(title="Finish project")

# Invalid (empty title)
TaskCreate(title="", description="...")  # Error: ensure title is at least 1 character

# Invalid (title too long)
TaskCreate(title="x" * 256)  # Error: title must be at most 255 characters

# Invalid (description too long)
TaskCreate(title="Test", description="x" * 2001)  # Error: description must be at most 2000 characters
```

---

### TaskUpdate (Update Request Schema)

**Purpose**: Validate PUT request body for updating tasks

**Fields** (all optional, only provided fields are updated):

```python
class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task via PUT /api/{user_id}/tasks/{id}
    All fields are optional; only provided fields are updated.
    Note: 'completed' is NOT updatable via PUT (only via PATCH /complete).
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New task title (optional, 1-255 characters if provided)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="New task description (optional, max 2000 characters if provided)"
    )
```

**Validation Example**:

```python
# Valid (update title only)
TaskUpdate(title="New title")

# Valid (update description only)
TaskUpdate(description="New description")

# Valid (update both)
TaskUpdate(title="New title", description="New description")

# Valid (empty update - no-op)
TaskUpdate()

# Invalid (empty title when provided)
TaskUpdate(title="")  # Error: if title is provided, must be at least 1 character

# Invalid (title too long)
TaskUpdate(title="x" * 256)  # Error: title must be at most 255 characters
```

---

### TaskResponse (Response Schema)

**Purpose**: Serialize tasks for all API responses (GET, POST, PUT, PATCH, DELETE)

**Fields** (complete task with all attributes):

```python
from datetime import datetime
import uuid

class TaskResponse(BaseModel):
    """
    Schema for task responses in all endpoints.
    Includes all task fields including id, timestamps, user_id.
    """
    id: uuid.UUID = Field(description="Unique task identifier")
    user_id: str = Field(description="Task owner (from JWT user_id)")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description")
    completed: bool = Field(description="Completion status")
    created_at: datetime = Field(description="When task was created (UTC)")
    updated_at: datetime = Field(description="When task was last updated (UTC)")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel
```

**Response Example**:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:00:00Z",
  "updated_at": "2026-01-08T10:00:00Z"
}
```

---

### TaskListResponse (List Response Schema)

**Purpose**: Serialize lists of tasks for GET /api/{user_id}/tasks

```python
from typing import List

class TaskListResponse(BaseModel):
    """Response for GET /api/{user_id}/tasks (list all tasks)"""
    tasks: List[TaskResponse] = Field(description="List of tasks for user")

    class Config:
        from_attributes = True
```

**Response Example**:

```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user-123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "user-123",
      "title": "Finish project",
      "description": null,
      "completed": true,
      "created_at": "2026-01-08T09:00:00Z",
      "updated_at": "2026-01-08T11:30:00Z"
    }
  ]
}
```

---

### ErrorResponse (Error Schema)

**Purpose**: Standardized error response for all error scenarios

```python
class ErrorResponse(BaseModel):
    """Error response for all HTTP error status codes (400, 401, 403, 404, 500)"""
    error: str = Field(description="Human-readable error message")
    status: int = Field(description="HTTP status code")
    detail: Optional[str] = Field(
        default=None,
        description="Optional additional error details"
    )
```

**Response Examples**:

```json
// 401 Unauthorized - Missing Token
{
  "error": "Missing or invalid authentication token",
  "status": 401
}

// 401 Unauthorized - Invalid Signature
{
  "error": "Invalid token",
  "status": 401,
  "detail": "Token signature verification failed"
}

// 403 Forbidden - Permission Denied
{
  "error": "You do not have permission to access these tasks",
  "status": 403
}

// 404 Not Found - Task doesn't exist
{
  "error": "Task not found",
  "status": 404
}

// 400 Bad Request - Validation failed
{
  "error": "Validation error",
  "status": 400,
  "detail": "title: ensure this value has at least 1 character"
}

// 500 Internal Server Error
{
  "error": "Internal server error",
  "status": 500,
  "detail": "Unexpected error occurred. Please contact support."
}
```

---

## Database Schema (SQL)

### Users Table (Reference Only)

The `users` table is referenced for foreign key constraint but is NOT managed by this backend. User records are created by Better Auth on the frontend.

```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### Tasks Table (Managed by Backend)

```sql
CREATE TABLE tasks (
    -- Primary Key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign Key (references users table)
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- Content
    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Status
    completed BOOLEAN NOT NULL DEFAULT FALSE,

    -- Timestamps
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

---

## State Transitions

### Task Lifecycle

```
[Task Created]
    ↓
[Open] (completed = false)
    ├─→ [Edit title/description via PUT]
    │       ↓
    ├─→ [Open] (title/description updated)
    │
    ├─→ [Toggle completion via PATCH /complete]
    │       ↓
    ├─→ [Completed] (completed = true)
    │       ↓
    ├─→ [Toggle completion again via PATCH /complete]
    │       ↓
    ├─→ [Open] (completed = false)
    │
    └─→ [Delete via DELETE]
            ↓
        [Task Removed from Database]
```

**State Rules**:

- Tasks start in **Open** state (completed = false)
- Tasks can be toggled between **Open** and **Completed** unlimited times
- Tasks can be edited (title, description) in any state
- Completed tasks are still visible and editable; not archived
- Deleted tasks cannot be recovered

---

## Relationships

### Task ↔ User

- **Relationship**: Many Tasks → One User
- **Foreign Key**: `tasks.user_id → users.id`
- **Cascade**: ON DELETE CASCADE (if user is deleted, all their tasks are deleted)
- **Isolation**: All queries filtered by `WHERE user_id = authenticated_user_id`
- **No Direct Access**: Backend never returns tasks belonging to other users

---

## Data Constraints & Invariants

| Constraint | Rule | Enforcement | Error Handling |
|-----------|------|------------|-----------------|
| **Unique ID** | Each task has unique UUID | Database primary key | 500 error (should never occur) |
| **User Isolation** | user_id matches authenticated user | Query-level filtering | 403 Forbidden if violated |
| **Title Required** | title is non-empty | Pydantic validation | 400 Bad Request if empty |
| **Title Max Length** | title ≤ 255 characters | Pydantic validation | 400 Bad Request if exceeded |
| **Description Optional** | description can be null | Pydantic validation | 400 Bad Request if invalid type |
| **Description Max Length** | description ≤ 2000 characters | Pydantic validation | 400 Bad Request if exceeded |
| **Completed Boolean** | completed is true or false | Pydantic validation | 400 Bad Request if not boolean |
| **Timestamps Immutable** | created_at never changes | Database-level (no UPDATE) | Read-only in API |
| **Updated At Auto** | updated_at updates on each modification | Database trigger (if needed) or app logic | Auto-managed |

---

## Validation Summary

### On Create (POST)

- ✓ title: required, 1-255 chars
- ✓ description: optional, max 2000 chars
- ✗ completed: not provided (always defaults to false)
- ✗ id, user_id, created_at, updated_at: assigned by backend

### On Update (PUT)

- ✓ title: optional, if provided must be 1-255 chars
- ✓ description: optional, if provided must be max 2000 chars
- ✗ completed: not updatable (use PATCH /complete instead)
- ✗ id, user_id, created_at: immutable, cannot change
- ✗ updated_at: auto-updated by system

### On Toggle Complete (PATCH /complete)

- ✓ completed: auto-toggled (false → true or true → false)
- ✗ No request body; all other fields immutable

### On Delete (DELETE)

- ✗ No request body
- ✓ Task removed from database (no soft-delete)

---

## Migration Strategy

### Initial Setup (First Deployment)

```python
# In app/database.py
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=3600    # Recycle connections after 1 hour
)

# Create all tables from SQLModel definitions
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Call this on app startup
create_db_and_tables()
```

### Future Migrations (Schema Changes)

Use Alembic for versioned migrations:

```bash
# Generate migration for schema change
alembic revision --autogenerate -m "Add task priority field"

# Apply migration to database
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## Notes

- All timestamps are stored in UTC and returned in ISO 8601 format
- UUIDs are used for task IDs for global uniqueness and security (not sequential/guessable)
- Foreign key on user_id ensures referential integrity but trusts JWT user_id claim
- Indexes on user_id critical for multi-user queries with thousands of tasks
- No soft-delete; deleted tasks are permanently removed (can implement audit log later)
- No versioning/audit trail for task changes (can add later if needed)

---

**Status**: ✅ Complete - Ready for implementation

**Data Model Version**: 1.0.0 | **Created**: 2026-01-08
