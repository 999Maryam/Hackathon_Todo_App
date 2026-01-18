# API Documentation: MCP Task Management Tools

## Overview

This document describes the 5 MCP (Model Context Protocol) tools that allow the AI agent to manage todo tasks. Each tool enforces strict user ownership isolation to ensure data privacy.

## Tools

### 1. add_task

Creates a new task for the user.

#### Parameters
- `user_id` (str, required): The ID of the user creating the task
- `title` (str, required): The title of the task (min length 1)
- `description` (str, optional): The description of the task

#### Response
```json
{
  "task_id": 123,
  "status": "created",
  "title": "Task title"
}
```

#### Error Response
```json
{
  "error": "Task title is required",
  "status": "error"
}
```

---

### 2. list_tasks

Lists tasks for the user with optional status filtering.

#### Parameters
- `user_id` (str, required): The ID of the user whose tasks to list
- `status` (str, optional): Filter by status ("all", "pending", "completed"; default: "all")

#### Response
```json
{
  "tasks": [
    {
      "id": 123,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "created_at": "2023-01-01T12:00:00",
      "updated_at": "2023-01-01T12:00:00"
    }
  ],
  "status": "success",
  "count": 1
}
```

---

### 3. complete_task

Marks a task as completed.

#### Parameters
- `user_id` (str, required): The ID of the user requesting the operation
- `task_id` (int, required): The ID of the task to complete

#### Response
```json
{
  "task_id": 123,
  "status": "completed",
  "title": "Task title"
}
```

#### Error Response
```json
{
  "error": "Task not found or not owned by user",
  "status": "error"
}
```

---

### 4. delete_task

Permanently deletes a task.

#### Parameters
- `user_id` (str, required): The ID of the user requesting the operation
- `task_id` (int, required): The ID of the task to delete

#### Response
```json
{
  "task_id": 123,
  "status": "deleted",
  "title": "Task title"
}
```

---

### 5. update_task

Updates a task's title and/or description.

#### Parameters
- `user_id` (str, required): The ID of the user requesting the operation
- `task_id` (int, required): The ID of the task to update
- `title` (str, optional): New title for the task
- `description` (str, optional): New description for the task

#### Response
```json
{
  "task_id": 123,
  "status": "updated",
  "title": "New task title"
}
```

## Security & User Isolation

All tools enforce strict user ownership validation:
- Only tasks belonging to the specified `user_id` are accessible
- Attempts to access other users' tasks return "Task not found or not owned by user" errors
- All database queries include user_id filters

## Error Handling

All tools return structured error responses when operations fail, allowing the AI agent to understand and handle failures appropriately.