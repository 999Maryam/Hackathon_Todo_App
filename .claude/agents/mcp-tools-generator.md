# MCP Tools Generator Agent

**Agent ID**: `mcp-tools-generator`
**Phase**: III — Todo AI Chatbot
**Version**: 1.0.0
**Created**: 2026-01-12

> This agent is responsible **ONLY** for creating and exposing the 5 MCP tools
> that enable the AI chatbot to manage tasks through natural language commands.

---

## Purpose

Generate fully-compliant MCP tool implementations that:
1. Follow the Official MCP SDK specification exactly
2. Enforce user isolation on every operation
3. Use SQLModel queries with `user_id` filtering
4. Return consistent, predictable output formats
5. Handle errors gracefully with user-friendly messages

---

## Constitutional Reference

**Governing Document**: `.specify/memory/constitution.md` (v2.0.0)

**Applicable Sections**:
```
### VII. AI-Native Focus (Phase III+)

MCP Tools (exactly as specified):
- `add_task` — Create a new task
- `list_tasks` — List all user tasks
- `complete_task` — Mark task as complete
- `delete_task` — Remove a task
- `update_task` — Modify task properties

Behavior Requirements:
- Confirmation before destructive operations
- Graceful error handling with user-friendly messages
```

---

## MCP Tools Specification

### Tool 1: `add_task`

**Purpose**: Create a new task for the authenticated user

**JSON Schema**:
```json
{
  "name": "add_task",
  "description": "Create a new task for the user. Returns the created task with its ID.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "The title of the task (required)",
        "minLength": 1,
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "Optional detailed description of the task",
        "maxLength": 1000
      },
      "due_date": {
        "type": "string",
        "format": "date",
        "description": "Optional due date in YYYY-MM-DD format"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "Optional priority level, defaults to medium"
      }
    },
    "required": ["title"],
    "additionalProperties": false
  }
}
```

**Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md#add_task
# MCP Tool: add_task - Create new task with user isolation

from mcp.server import Server
from mcp.types import Tool, TextContent
from sqlmodel import Session, select
from models.task import Task
from datetime import date
from typing import Optional
import json

async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: str = "medium"
) -> dict:
    """
    Create a new task for the specified user.

    Args:
        user_id: Authenticated user's ID (from JWT)
        title: Task title (required)
        description: Optional task description
        due_date: Optional due date (YYYY-MM-DD)
        priority: Task priority (low/medium/high)

    Returns:
        dict: Created task details
    """
    # Parse due_date if provided
    parsed_due_date = None
    if due_date:
        try:
            parsed_due_date = date.fromisoformat(due_date)
        except ValueError:
            return {
                "success": False,
                "error": f"Invalid date format: {due_date}. Use YYYY-MM-DD."
            }

    # Create task with user_id (CRITICAL: user isolation)
    task = Task(
        user_id=user_id,  # MUST be from authenticated JWT
        title=title,
        description=description,
        due_date=parsed_due_date,
        priority=priority,
        is_completed=False
    )

    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": str(task.id),
            "status": "created",
            "title": task.title,
            "description": task.description,
            "due_date": str(task.due_date) if task.due_date else None,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "message": f"Task '{title}' created successfully."
        }
```

**Example Input**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "due_date": "2026-01-15",
  "priority": "high"
}
```

**Example Output**:
```json
{
  "success": true,
  "task_id": "123",
  "status": "created",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "due_date": "2026-01-15",
  "priority": "high",
  "is_completed": false,
  "message": "Task 'Buy groceries' created successfully."
}
```

---

### Tool 2: `list_tasks`

**Purpose**: List all tasks belonging to the authenticated user

**JSON Schema**:
```json
{
  "name": "list_tasks",
  "description": "List all tasks for the user with optional filtering and sorting.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "filter": {
        "type": "string",
        "enum": ["all", "completed", "pending"],
        "description": "Filter tasks by completion status, defaults to all"
      },
      "sort_by": {
        "type": "string",
        "enum": ["created_at", "due_date", "priority", "title"],
        "description": "Sort tasks by field, defaults to created_at"
      },
      "sort_order": {
        "type": "string",
        "enum": ["asc", "desc"],
        "description": "Sort order, defaults to desc"
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "description": "Maximum number of tasks to return, defaults to 50"
      }
    },
    "additionalProperties": false
  }
}
```

**Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md#list_tasks
# MCP Tool: list_tasks - List user's tasks with filtering

from sqlmodel import Session, select, desc, asc
from typing import Optional, List

async def list_tasks(
    user_id: str,
    filter: str = "all",
    sort_by: str = "created_at",
    sort_order: str = "desc",
    limit: int = 50
) -> dict:
    """
    List tasks for the specified user with optional filtering.

    Args:
        user_id: Authenticated user's ID (from JWT)
        filter: Filter by status (all/completed/pending)
        sort_by: Field to sort by
        sort_order: Sort direction (asc/desc)
        limit: Maximum results to return

    Returns:
        dict: List of tasks with count
    """
    with Session(engine) as session:
        # CRITICAL: Always filter by user_id first
        statement = select(Task).where(Task.user_id == user_id)

        # Apply completion filter
        if filter == "completed":
            statement = statement.where(Task.is_completed == True)
        elif filter == "pending":
            statement = statement.where(Task.is_completed == False)

        # Apply sorting
        sort_column = getattr(Task, sort_by, Task.created_at)
        if sort_order == "asc":
            statement = statement.order_by(asc(sort_column))
        else:
            statement = statement.order_by(desc(sort_column))

        # Apply limit
        statement = statement.limit(limit)

        tasks = session.exec(statement).all()

        # Format response
        task_list = [
            {
                "task_id": str(task.id),
                "title": task.title,
                "description": task.description,
                "due_date": str(task.due_date) if task.due_date else None,
                "priority": task.priority,
                "is_completed": task.is_completed,
                "created_at": task.created_at.isoformat()
            }
            for task in tasks
        ]

        return {
            "success": True,
            "count": len(task_list),
            "filter": filter,
            "tasks": task_list,
            "message": f"Found {len(task_list)} task(s)."
        }
```

**Example Input**:
```json
{
  "filter": "pending",
  "sort_by": "due_date",
  "sort_order": "asc"
}
```

**Example Output**:
```json
{
  "success": true,
  "count": 2,
  "filter": "pending",
  "tasks": [
    {
      "task_id": "123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "due_date": "2026-01-15",
      "priority": "high",
      "is_completed": false,
      "created_at": "2026-01-12T10:30:00"
    },
    {
      "task_id": "124",
      "title": "Call dentist",
      "description": null,
      "due_date": "2026-01-20",
      "priority": "medium",
      "is_completed": false,
      "created_at": "2026-01-12T11:00:00"
    }
  ],
  "message": "Found 2 task(s)."
}
```

---

### Tool 3: `complete_task`

**Purpose**: Mark a specific task as completed

**JSON Schema**:
```json
{
  "name": "complete_task",
  "description": "Mark a task as completed. Requires task_id.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to mark as complete"
      }
    },
    "required": ["task_id"],
    "additionalProperties": false
  }
}
```

**Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md#complete_task
# MCP Tool: complete_task - Mark task as completed with ownership check

async def complete_task(
    user_id: str,
    task_id: str
) -> dict:
    """
    Mark a task as completed.

    Args:
        user_id: Authenticated user's ID (from JWT)
        task_id: ID of the task to complete

    Returns:
        dict: Updated task status

    Raises:
        TaskNotFoundError: If task doesn't exist or belongs to another user
    """
    with Session(engine) as session:
        # CRITICAL: Query with BOTH task_id AND user_id for ownership validation
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Ownership check
        )
        task = session.exec(statement).first()

        # Task not found OR belongs to another user (same error for security)
        if not task:
            return {
                "success": False,
                "error": "task_not_found",
                "message": f"Task with ID '{task_id}' not found. Please check the task ID and try again."
            }

        # Check if already completed
        if task.is_completed:
            return {
                "success": True,
                "task_id": str(task.id),
                "status": "already_completed",
                "title": task.title,
                "message": f"Task '{task.title}' was already marked as complete."
            }

        # Mark as completed
        task.is_completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title,
            "is_completed": True,
            "message": f"Task '{task.title}' marked as complete. Well done!"
        }
```

**Example Input**:
```json
{
  "task_id": "123"
}
```

**Example Output (Success)**:
```json
{
  "success": true,
  "task_id": "123",
  "status": "completed",
  "title": "Buy groceries",
  "is_completed": true,
  "message": "Task 'Buy groceries' marked as complete. Well done!"
}
```

**Example Output (Not Found)**:
```json
{
  "success": false,
  "error": "task_not_found",
  "message": "Task with ID '999' not found. Please check the task ID and try again."
}
```

---

### Tool 4: `delete_task`

**Purpose**: Delete a task (with confirmation behavior)

**JSON Schema**:
```json
{
  "name": "delete_task",
  "description": "Delete a task permanently. This action cannot be undone. The AI should confirm with the user before calling this tool.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to delete"
      },
      "confirmed": {
        "type": "boolean",
        "description": "Must be true to proceed with deletion. AI should confirm with user first.",
        "default": false
      }
    },
    "required": ["task_id"],
    "additionalProperties": false
  }
}
```

**Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md#delete_task
# MCP Tool: delete_task - Remove task with ownership check and confirmation

async def delete_task(
    user_id: str,
    task_id: str,
    confirmed: bool = False
) -> dict:
    """
    Delete a task permanently.

    Args:
        user_id: Authenticated user's ID (from JWT)
        task_id: ID of the task to delete
        confirmed: Must be True to proceed (prevents accidental deletion)

    Returns:
        dict: Deletion status or confirmation request
    """
    with Session(engine) as session:
        # CRITICAL: Query with BOTH task_id AND user_id for ownership validation
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Ownership check
        )
        task = session.exec(statement).first()

        # Task not found OR belongs to another user
        if not task:
            return {
                "success": False,
                "error": "task_not_found",
                "message": f"Task with ID '{task_id}' not found. Please check the task ID and try again."
            }

        # Require confirmation for destructive action
        if not confirmed:
            return {
                "success": False,
                "status": "confirmation_required",
                "task_id": str(task.id),
                "title": task.title,
                "message": f"Are you sure you want to delete '{task.title}'? This action cannot be undone. Please confirm to proceed."
            }

        # Store title before deletion for response
        task_title = task.title

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "task_id": task_id,
            "status": "deleted",
            "title": task_title,
            "message": f"Task '{task_title}' has been permanently deleted."
        }
```

**Example Input (Without Confirmation)**:
```json
{
  "task_id": "123"
}
```

**Example Output (Confirmation Required)**:
```json
{
  "success": false,
  "status": "confirmation_required",
  "task_id": "123",
  "title": "Buy groceries",
  "message": "Are you sure you want to delete 'Buy groceries'? This action cannot be undone. Please confirm to proceed."
}
```

**Example Input (With Confirmation)**:
```json
{
  "task_id": "123",
  "confirmed": true
}
```

**Example Output (Deleted)**:
```json
{
  "success": true,
  "task_id": "123",
  "status": "deleted",
  "title": "Buy groceries",
  "message": "Task 'Buy groceries' has been permanently deleted."
}
```

---

### Tool 5: `update_task`

**Purpose**: Modify properties of an existing task

**JSON Schema**:
```json
{
  "name": "update_task",
  "description": "Update one or more properties of an existing task.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "The ID of the task to update"
      },
      "title": {
        "type": "string",
        "description": "New title for the task",
        "minLength": 1,
        "maxLength": 255
      },
      "description": {
        "type": "string",
        "description": "New description for the task",
        "maxLength": 1000
      },
      "due_date": {
        "type": "string",
        "format": "date",
        "description": "New due date in YYYY-MM-DD format (use null to clear)"
      },
      "priority": {
        "type": "string",
        "enum": ["low", "medium", "high"],
        "description": "New priority level"
      },
      "is_completed": {
        "type": "boolean",
        "description": "Set completion status"
      }
    },
    "required": ["task_id"],
    "additionalProperties": false
  }
}
```

**Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md#update_task
# MCP Tool: update_task - Modify task properties with ownership check

from typing import Optional

async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None,
    is_completed: Optional[bool] = None
) -> dict:
    """
    Update one or more properties of a task.

    Args:
        user_id: Authenticated user's ID (from JWT)
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)
        due_date: New due date YYYY-MM-DD (optional)
        priority: New priority (optional)
        is_completed: New completion status (optional)

    Returns:
        dict: Updated task details
    """
    with Session(engine) as session:
        # CRITICAL: Query with BOTH task_id AND user_id for ownership validation
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id  # Ownership check
        )
        task = session.exec(statement).first()

        # Task not found OR belongs to another user
        if not task:
            return {
                "success": False,
                "error": "task_not_found",
                "message": f"Task with ID '{task_id}' not found. Please check the task ID and try again."
            }

        # Track what was updated
        updates = []

        # Apply updates only for provided fields
        if title is not None:
            task.title = title
            updates.append("title")

        if description is not None:
            task.description = description
            updates.append("description")

        if due_date is not None:
            if due_date == "" or due_date.lower() == "null":
                task.due_date = None
                updates.append("due_date (cleared)")
            else:
                try:
                    task.due_date = date.fromisoformat(due_date)
                    updates.append("due_date")
                except ValueError:
                    return {
                        "success": False,
                        "error": "invalid_date",
                        "message": f"Invalid date format: {due_date}. Use YYYY-MM-DD."
                    }

        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                return {
                    "success": False,
                    "error": "invalid_priority",
                    "message": f"Invalid priority: {priority}. Use low, medium, or high."
                }
            task.priority = priority
            updates.append("priority")

        if is_completed is not None:
            task.is_completed = is_completed
            updates.append("is_completed")

        # Check if any updates were made
        if not updates:
            return {
                "success": True,
                "task_id": str(task.id),
                "status": "no_changes",
                "title": task.title,
                "message": "No changes were specified. Task remains unchanged."
            }

        # Save changes
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title,
            "description": task.description,
            "due_date": str(task.due_date) if task.due_date else None,
            "priority": task.priority,
            "is_completed": task.is_completed,
            "updated_fields": updates,
            "message": f"Task updated successfully. Changed: {', '.join(updates)}."
        }
```

**Example Input**:
```json
{
  "task_id": "123",
  "title": "Buy groceries and snacks",
  "priority": "medium",
  "due_date": "2026-01-20"
}
```

**Example Output**:
```json
{
  "success": true,
  "task_id": "123",
  "status": "updated",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread",
  "due_date": "2026-01-20",
  "priority": "medium",
  "is_completed": false,
  "updated_fields": ["title", "priority", "due_date"],
  "message": "Task updated successfully. Changed: title, priority, due_date."
}
```

---

## MCP Server Registration

**Full Server Implementation**:
```python
# Task: T3XX | Spec: specs/003-ai-chatbot/mcp-tools-spec.md
# MCP Server: Register all 5 task management tools

from mcp.server import Server
from mcp.types import Tool, TextContent
import json

# Initialize MCP server
server = Server("todo-task-manager")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """Register all available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user. Returns the created task with its ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title (required)", "minLength": 1, "maxLength": 255},
                    "description": {"type": "string", "description": "Optional description", "maxLength": 1000},
                    "due_date": {"type": "string", "format": "date", "description": "Due date YYYY-MM-DD"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for the user with optional filtering and sorting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "enum": ["all", "completed", "pending"]},
                    "sort_by": {"type": "string", "enum": ["created_at", "due_date", "priority", "title"]},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"]},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100}
                }
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed. Requires task_id.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of task to complete"}
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task permanently. AI should confirm with user before calling with confirmed=true.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of task to delete"},
                    "confirmed": {"type": "boolean", "description": "Must be true to proceed", "default": False}
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update one or more properties of an existing task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of task to update"},
                    "title": {"type": "string", "minLength": 1, "maxLength": 255},
                    "description": {"type": "string", "maxLength": 1000},
                    "due_date": {"type": "string", "format": "date"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                    "is_completed": {"type": "boolean"}
                },
                "required": ["task_id"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute the requested tool with user context."""

    # CRITICAL: user_id must be injected from authenticated JWT context
    # This is handled by the chat endpoint before calling MCP tools
    user_id = arguments.pop("_user_id", None)

    if not user_id:
        raise ValueError("Authentication required: user_id not provided")

    # Route to appropriate tool
    if name == "add_task":
        result = await add_task(user_id=user_id, **arguments)
    elif name == "list_tasks":
        result = await list_tasks(user_id=user_id, **arguments)
    elif name == "complete_task":
        result = await complete_task(user_id=user_id, **arguments)
    elif name == "delete_task":
        result = await delete_task(user_id=user_id, **arguments)
    elif name == "update_task":
        result = await update_task(user_id=user_id, **arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

---

## Security Requirements

### User Isolation (Constitution IV)

**CRITICAL**: Every tool MUST enforce user isolation:

```python
# ✅ CORRECT: Always include user_id in WHERE clause
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == user_id  # MANDATORY
)

# ❌ WRONG: Never query without user_id filter
statement = select(Task).where(Task.id == task_id)  # SECURITY VULNERABILITY
```

### Error Message Security

Never leak information about other users' tasks:

```python
# ✅ CORRECT: Generic "not found" message
if not task:
    return {"error": "task_not_found", "message": "Task not found"}

# ❌ WRONG: Reveals task exists but belongs to another user
if task.user_id != user_id:
    return {"error": "unauthorized", "message": "This task belongs to another user"}
```

### Authentication Flow

```
1. User sends message to /api/{user_id}/chat
2. Chat endpoint validates JWT token
3. Chat endpoint extracts user_id from token
4. Chat endpoint passes user_id to MCP tool via _user_id
5. MCP tool uses user_id in all database queries
```

---

## Error Handling Matrix

| Error Type | Code | Response Format |
|------------|------|-----------------|
| Task not found | `task_not_found` | `{"success": false, "error": "task_not_found", "message": "..."}` |
| Invalid date | `invalid_date` | `{"success": false, "error": "invalid_date", "message": "..."}` |
| Invalid priority | `invalid_priority` | `{"success": false, "error": "invalid_priority", "message": "..."}` |
| Confirmation needed | `confirmation_required` | `{"success": false, "status": "confirmation_required", "message": "..."}` |
| No changes | `no_changes` | `{"success": true, "status": "no_changes", "message": "..."}` |
| Already completed | `already_completed` | `{"success": true, "status": "already_completed", "message": "..."}` |

---

## Output Format Standards

### Success Response
```json
{
  "success": true,
  "task_id": "string",
  "status": "created|updated|completed|deleted",
  "title": "string",
  "message": "Human-friendly message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "error_code",
  "message": "Human-friendly error message"
}
```

### List Response
```json
{
  "success": true,
  "count": 0,
  "tasks": [],
  "message": "Human-friendly summary"
}
```

---

## File Structure

```
backend/
├── src/
│   └── mcp/
│       ├── __init__.py
│       ├── server.py         # MCP server initialization
│       ├── tools.py          # Tool implementations (this spec)
│       └── schemas.py        # Pydantic schemas for validation
└── tests/
    └── test_mcp_tools.py     # Tool unit tests
```

---

## Testing Checklist

- [ ] `add_task` creates task with correct user_id
- [ ] `add_task` validates required title field
- [ ] `add_task` handles optional fields correctly
- [ ] `list_tasks` only returns current user's tasks
- [ ] `list_tasks` filtering works (all/completed/pending)
- [ ] `list_tasks` sorting works (all fields, both directions)
- [ ] `complete_task` only completes own tasks
- [ ] `complete_task` returns appropriate message if already complete
- [ ] `delete_task` requires confirmation
- [ ] `delete_task` only deletes own tasks
- [ ] `update_task` only updates own tasks
- [ ] `update_task` handles partial updates
- [ ] All tools return consistent JSON format
- [ ] Error messages are user-friendly (no stack traces)
- [ ] User A cannot see/modify User B's tasks

---

## Related Documents

- **Global Constitution**: `.specify/memory/constitution.md`
- **AI Chatbot Manager**: `.claude/agents/agents-ai-chatbot-manager.md`
- **Phase II Task Model**: `backend/src/models/task.py`
- **Phase III Spec**: `specs/003-ai-chatbot/mcp-tools-spec.md`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-12 | Initial agent definition with all 5 MCP tools |
