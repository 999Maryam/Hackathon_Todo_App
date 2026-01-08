"""Integration tests for GET /api/{user_id}/tasks/{id} endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_get_task_with_valid_jwt(client: TestClient, valid_token: str, session):
    """Test getting a single task with valid JWT returns 200 OK."""
    user_id = "test-user-123"

    # Create a task first
    task_create = TaskCreate(title="Buy groceries", description="Milk, eggs")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.get(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(task.id)
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs"
    assert data["completed"] is False
    assert data["user_id"] == user_id


@pytest.mark.integration
def test_get_task_with_nonexistent_id(client: TestClient, valid_token: str):
    """Test getting a task with non-existent ID returns 404."""
    import uuid
    fake_id = uuid.uuid4()

    response = client.get(
        f"/api/test-user-123/tasks/{fake_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 404


@pytest.mark.integration
def test_get_task_without_jwt(client: TestClient, session):
    """Test getting a task without JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.get(f"/api/{user_id}/tasks/{task.id}")

    assert response.status_code == 403


@pytest.mark.integration
def test_get_task_with_invalid_jwt(client: TestClient, invalid_token: str, session):
    """Test getting a task with invalid JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.get(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_get_task_belonging_to_other_user(
    client: TestClient,
    valid_token: str,
    session,
):
    """Test that user cannot get task belonging to another user."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User B creates a task
    task_create = TaskCreate(title="User B's task")
    task = TaskService.create_task(session, user_b_id, task_create)

    # User A tries to get User B's task
    response = client.get(
        f"/api/{user_a_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    # Should get 404 (filtered view - task doesn't exist for this user)
    assert response.status_code == 404


@pytest.mark.integration
def test_get_task_returns_all_fields(client: TestClient, valid_token: str, session):
    """Test that GET returns all task fields including timestamps."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Full task", description="With all fields")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.get(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "user_id" in data
    assert "title" in data
    assert "description" in data
    assert "completed" in data
    assert "created_at" in data
    assert "updated_at" in data
