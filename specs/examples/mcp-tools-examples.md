# Usage Examples: MCP Task Management Tools

This document provides practical examples of how to use the 5 MCP task management tools for the AI agent.

## Tool Registration Example

```python
from fmcp import server as mcp_server
from fmcp.server.tool import tool
from app.mcp_server import TodoMCPService

# The tools are automatically registered when the server starts
# Each tool is available as a method in the TodoMCPService class
```

## Example 1: Add Task

The AI agent can create a new task for a user:

```json
{
  "name": "add_task_tool",
  "arguments": {
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }
}
```

**Response:**
```json
{
  "task_id": 456,
  "status": "created",
  "title": "Buy groceries"
}
```

## Example 2: List Tasks

The AI agent can retrieve a user's tasks:

```json
{
  "name": "list_tasks_tool",
  "arguments": {
    "user_id": "user123",
    "status": "all"
  }
}
```

**Response:**
```json
{
  "tasks": [
    {
      "id": 456,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2023-01-01T10:00:00",
      "updated_at": "2023-01-01T10:00:00"
    }
  ],
  "status": "success",
  "count": 1
}
```

## Example 3: Complete Task

The AI agent can mark a task as completed:

```json
{
  "name": "complete_task_tool",
  "arguments": {
    "user_id": "user123",
    "task_id": 456
  }
}
```

**Response:**
```json
{
  "task_id": 456,
  "status": "completed",
  "title": "Buy groceries"
}
```

## Example 4: Delete Task

The AI agent can permanently remove a task:

```json
{
  "name": "delete_task_tool",
  "arguments": {
    "user_id": "user123",
    "task_id": 456
  }
}
```

**Response:**
```json
{
  "task_id": 456,
  "status": "deleted",
  "title": "Buy groceries"
}
```

## Example 5: Update Task

The AI agent can modify a task's title or description:

```json
{
  "name": "update_task_tool",
  "arguments": {
    "user_id": "user123",
    "task_id": 456,
    "title": "Buy groceries and household supplies",
    "description": "Milk, eggs, bread, toilet paper"
  }
}
```

**Response:**
```json
{
  "task_id": 456,
  "status": "updated",
  "title": "Buy groceries and household supplies"
}
```

## Error Handling Examples

### Missing Title Error
```json
{
  "name": "add_task_tool",
  "arguments": {
    "user_id": "user123",
    "title": ""
  }
}
```

**Response:**
```json
{
  "error": "Task title is required",
  "status": "error"
}
```

### Access Denied Error
```json
{
  "name": "complete_task_tool",
  "arguments": {
    "user_id": "user456",
    "task_id": 456
  }
}
```

**Response:**
```json
{
  "error": "Task not found or not owned by user",
  "status": "error"
}
```

## AI Agent Integration

The tools can be integrated into an AI agent system like this:

```python
# Example of how an AI agent might use these tools
def handle_user_request(user_id, request_text):
    # Parse user request and determine appropriate tool
    if "add task" in request_text.lower():
        # Extract title and description from user request
        title = extract_title(request_text)
        description = extract_description(request_text)

        # Call the add_task tool
        result = call_tool("add_task_tool", {
            "user_id": user_id,
            "title": title,
            "description": description
        })

        return f"Added task: {result['title']}"

    elif "show my tasks" in request_text.lower():
        # Call the list_tasks tool
        result = call_tool("list_tasks_tool", {
            "user_id": user_id,
            "status": "all"
        })

        tasks = result["tasks"]
        return f"You have {len(tasks)} tasks: {[task['title'] for task in tasks]}"

    # Additional logic for other operations...
```