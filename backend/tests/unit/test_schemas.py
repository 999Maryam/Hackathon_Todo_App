"""Unit tests for Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from app.models.schemas import TaskCreate, TaskUpdate, TaskResponse


@pytest.mark.unit
def test_task_create_valid():
    """Test TaskCreate with valid data."""
    schema = TaskCreate(title="Test task", description="Description")
    assert schema.title == "Test task"
    assert schema.description == "Description"


@pytest.mark.unit
def test_task_create_minimal():
    """Test TaskCreate with only required field."""
    schema = TaskCreate(title="Test task")
    assert schema.title == "Test task"
    assert schema.description is None


@pytest.mark.unit
def test_task_create_missing_title():
    """Test TaskCreate validation fails without title."""
    with pytest.raises(ValidationError):
        TaskCreate(description="Description")


@pytest.mark.unit
def test_task_create_empty_title():
    """Test TaskCreate validation fails with empty title."""
    with pytest.raises(ValidationError):
        TaskCreate(title="")


@pytest.mark.unit
def test_task_create_title_too_long():
    """Test TaskCreate validation fails with title > 255 chars."""
    with pytest.raises(ValidationError):
        TaskCreate(title="x" * 256)


@pytest.mark.unit
def test_task_create_description_too_long():
    """Test TaskCreate validation fails with description > 2000 chars."""
    with pytest.raises(ValidationError):
        TaskCreate(title="Title", description="x" * 2001)


@pytest.mark.unit
def test_task_update_all_optional():
    """Test TaskUpdate with all fields optional."""
    schema = TaskUpdate()
    assert schema.title is None
    assert schema.description is None


@pytest.mark.unit
def test_task_update_title_only():
    """Test TaskUpdate with title only."""
    schema = TaskUpdate(title="New title")
    assert schema.title == "New title"
    assert schema.description is None


@pytest.mark.unit
def test_task_update_description_only():
    """Test TaskUpdate with description only."""
    schema = TaskUpdate(description="New description")
    assert schema.title is None
    assert schema.description == "New description"


@pytest.mark.unit
def test_task_update_empty_title():
    """Test TaskUpdate validation fails with empty title when provided."""
    with pytest.raises(ValidationError):
        TaskUpdate(title="")


@pytest.mark.unit
def test_task_update_title_too_long():
    """Test TaskUpdate validation fails with title > 255 chars."""
    with pytest.raises(ValidationError):
        TaskUpdate(title="x" * 256)


@pytest.mark.unit
def test_task_response_from_dict():
    """Test TaskResponse can be created from dict."""
    import uuid
    from datetime import datetime

    task_id = uuid.uuid4()
    now = datetime.utcnow()

    data = {
        "id": task_id,
        "user_id": "user-123",
        "title": "Test task",
        "description": "Description",
        "completed": False,
        "created_at": now,
        "updated_at": now,
    }

    schema = TaskResponse(**data)
    assert schema.id == task_id
    assert schema.user_id == "user-123"
    assert schema.title == "Test task"
