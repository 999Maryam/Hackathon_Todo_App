"""MCP Tools Package for Todo AI Chatbot.

This package contains MCP (Model Context Protocol) tools that allow the AI agent
to perform todo task operations such as adding, listing, completing, deleting,
and updating tasks.

Each tool enforces strict user ownership isolation to ensure data privacy.
"""

from .task_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task"
]