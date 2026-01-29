"""Data models for the application."""

from sqlmodel import SQLModel
from app.models.task import Task
from app.models.user import User, UserCreate, UserPublic, UserLogin
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    ErrorResponse,
)

# Phase V: Advanced Features Models
from app.models.enums import Priority, RecurringFrequency
from app.models.tag import Tag
from app.models.task_tag import TaskTag
from app.models.recurring_config import RecurringConfig
from app.models.reminder import Reminder

__all__ = [
    # SQLModel base class (for Alembic migrations)
    "SQLModel",
    # Core Models
    "Task",
    "User",
    "UserCreate",
    "UserPublic",
    "UserLogin",
    "Conversation",
    "Message",
    # Schemas
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    "ErrorResponse",
    # Phase V: Enums
    "Priority",
    "RecurringFrequency",
    # Phase V: Models
    "Tag",
    "TaskTag",
    "RecurringConfig",
    "Reminder",
]
