# Quickstart Guide: MCP Tools Server & Task Operations

## Overview

This guide explains how to set up and use the MCP (Model Context Protocol) tools for managing todo tasks. The tools allow an AI agent to perform CRUD operations on tasks with strict user ownership isolation.

## Prerequisites

- Python 3.13+
- FastAPI
- SQLModel
- fmcp>=0.6.0 (MCP SDK)

## Installation

1. Install the MCP SDK:
```bash
pip install fmcp>=0.6.0
```

2. Ensure your requirements.txt includes:
```
fmcp>=0.6.0
```

## Tool Setup

The tools are organized in the `backend/app/tools/` directory:

```
backend/app/tools/
├── __init__.py
└── task_tools.py
```

## Available Tools

### 1. add_task
- Creates a new task for a user
- Requires: user_id, title
- Optional: description

### 2. list_tasks
- Lists tasks for a user with optional status filtering
- Requires: user_id
- Optional: status ("all", "pending", "completed")

### 3. complete_task
- Marks a task as completed
- Requires: user_id, task_id

### 4. delete_task
- Permanently deletes a task
- Requires: user_id, task_id

### 5. update_task
- Updates task title and/or description
- Requires: user_id, task_id
- Optional: title, description

## Running the MCP Server

The MCP server is implemented in `backend/app/mcp_server.py`:

```python
from app.mcp_server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Testing the Tools

Run the integration tests:

```bash
cd backend
pytest tests/test_mcp_tools.py -v
```

## User Isolation

All tools enforce strict user ownership validation:
- Only tasks belonging to the specified user_id are accessible
- Cross-user access attempts return "Task not found or not owned by user" errors

## Error Handling

All tools return structured error responses when operations fail, allowing the AI agent to handle failures appropriately.

## Integration with AI Agent

The tools can be registered with an AI agent system to enable natural language task management.