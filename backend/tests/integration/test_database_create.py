"""Database integration tests for task creation."""

import pytest
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_task_persists_in_database(session: Session):
    """Test that created task persists in database with correct user_id."""
    user_id = "test-user-123"
    task_create = TaskCreate(
        title="Buy groceries",
        description="Milk, eggs, bread",
    )

    # Create task
    task = TaskService.create_task(session, user_id, task_create)

    # Verify task exists in database
    retrieved_task = session.get(Task, task.id)
    assert retrieved_task is not None
    assert retrieved_task.user_id == user_id
    assert retrieved_task.title == "Buy groceries"
    assert retrieved_task.description == "Milk, eggs, bread"
    assert retrieved_task.completed is False


@pytest.mark.integration
def test_task_assigned_correct_user_id(session: Session):
    """Test that task is assigned to correct user_id."""
    user_id = "user-xyz"
    task_create = TaskCreate(title="Test task")

    task = TaskService.create_task(session, user_id, task_create)

    assert task.user_id == user_id
    assert task.id is not None
    assert task.created_at is not None
    assert task.updated_at is not None


@pytest.mark.integration
def test_task_created_with_defaults(session: Session):
    """Test that task is created with correct defaults."""
    task_create = TaskCreate(title="Test")

    task = TaskService.create_task(session, "user-123", task_create)

    assert task.completed is False
    assert task.description is None
    assert task.created_at == task.updated_at
