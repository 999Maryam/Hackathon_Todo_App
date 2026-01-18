"""MCP Server for Todo Task Management Tools.

This module implements a FastMCP server that registers the 5 task management tools
for the OpenAI agent to use. The server handles database session management
through its lifespan context.
"""

from fmcp import server as mcp_server
from fmcp.server.tool import tool
from sqlmodel import Session
from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from app.database import engine
from app.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for database session management."""
    # Startup: nothing specific needed
    yield
    # Shutdown: nothing specific needed
    # Engine disposal happens automatically


# Create FastAPI app for MCP server
app = FastAPI(lifespan=lifespan)


@mcp_server(app)
class TodoMCPService:
    """MCP Service class that registers all task management tools."""

    @tool
    def add_task_tool(
        self,
        user_id: str,
        title: str,
        description: str = ""
    ):
        """Add a new task for the user.

        Args:
            user_id: The ID of the user creating the task
            title: The title of the task (required)
            description: The description of the task (optional)

        Returns:
            Dictionary with task_id, status, and title on success
        """
        with Session(engine) as db:
            # Pass db session to the actual implementation
            result = add_task(user_id, title, description if description else None, db)
            return result

    @tool
    def list_tasks_tool(
        self,
        user_id: str,
        status: str = "all"
    ):
        """List tasks for the user with optional status filtering.

        Args:
            user_id: The ID of the user whose tasks to list
            status: Filter by status ("all", "pending", "completed"; default: "all")

        Returns:
            Dictionary with tasks array and status
        """
        with Session(engine) as db:
            # Pass db session to the actual implementation
            result = list_tasks(user_id, status, db)
            return result

    @tool
    def complete_task_tool(
        self,
        user_id: str,
        task_id: int
    ):
        """Mark a task as completed.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to complete

        Returns:
            Dictionary with task_id, status, and title on success
        """
        with Session(engine) as db:
            # Pass db session to the actual implementation
            result = complete_task(user_id, task_id, db)
            return result

    @tool
    def delete_task_tool(
        self,
        user_id: str,
        task_id: int
    ):
        """Delete a task permanently.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to delete

        Returns:
            Dictionary with task_id, status, and title on success
        """
        with Session(engine) as db:
            # Pass db session to the actual implementation
            result = delete_task(user_id, task_id, db)
            return result

    @tool
    def update_task_tool(
        self,
        user_id: str,
        task_id: int,
        title: str = "",
        description: str = ""
    ):
        """Update a task's title and/or description.

        Args:
            user_id: The ID of the user requesting the operation
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Dictionary with task_id, status, and title on success
        """
        with Session(engine) as db:
            # Pass db session to the actual implementation
            # Only pass non-empty values
            title_val = title if title else None
            desc_val = description if description else None
            result = update_task(user_id, task_id, title_val, desc_val, db)
            return result


# Entry point for running the server directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)