"""Unit tests for Task model validation."""

import pytest
from datetime import datetime
import uuid

from app.models.task import Task


@pytest.mark.unit
def test_task_creation_with_all_fields():
    """Test creating a task with all fields."""
    task_id = uuid.uuid4()
    now = datetime.utcnow()

    task = Task(
        id=task_id,
        user_id="user-123",
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=now,
        updated_at=now,
    )

    assert task.id == task_id
    assert task.user_id == "user-123"
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False
    assert task.created_at == now
    assert task.updated_at == now


@pytest.mark.unit
def test_task_title_required():
    """Test that task title is required."""
    with pytest.raises(TypeError):
        Task(
            user_id="user-123",
            # title missing
            description="Some description",
        )


@pytest.mark.unit
def test_task_user_id_required():
    """Test that task user_id is required."""
    with pytest.raises(TypeError):
        Task(
            title="Some title",
            # user_id missing
            description="Some description",
        )


@pytest.mark.unit
def test_task_defaults():
    """Test task default values."""
    task = Task(user_id="user-123", title="Test task")

    assert task.completed is False
    assert task.description is None
    assert task.id is not None  # auto-generated
    assert task.created_at is not None  # auto-generated
    assert task.updated_at is not None  # auto-generated


@pytest.mark.unit
def test_task_title_max_length():
    """Test task title with max length."""
    long_title = "x" * 255
    task = Task(user_id="user-123", title=long_title)
    assert len(task.title) == 255


@pytest.mark.unit
def test_task_description_optional():
    """Test task description is optional."""
    task = Task(user_id="user-123", title="Title")
    assert task.description is None


@pytest.mark.unit
def test_task_description_max_length():
    """Test task description with max length."""
    long_description = "x" * 2000
    task = Task(user_id="user-123", title="Title", description=long_description)
    assert len(task.description) == 2000
