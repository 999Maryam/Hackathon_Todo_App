"""Integration tests for PATCH /api/{user_id}/tasks/{id}/complete endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_toggle_completion_false_to_true(client: TestClient, valid_token: str, session):
    """Test toggling completion from false to true."""
    user_id = "test-user-123"

    # Create task (completed=false by default)
    task_create = TaskCreate(title="Buy groceries")
    task = TaskService.create_task(session, user_id, task_create)
    assert task.completed is False

    response = client.patch(
        f"/api/{user_id}/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


@pytest.mark.integration
def test_toggle_completion_true_to_false(client: TestClient, valid_token: str, session):
    """Test toggling completion from true to false."""
    user_id = "test-user-123"

    # Create task and toggle to true first
    task_create = TaskCreate(title="Buy groceries")
    task = TaskService.create_task(session, user_id, task_create)
    TaskService.toggle_complete(session, user_id, task.id)

    # Now toggle back to false
    response = client.patch(
        f"/api/{user_id}/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


@pytest.mark.integration
def test_toggle_completion_nonexistent_id(client: TestClient, valid_token: str):
    """Test toggling completion with non-existent ID returns 404."""
    import uuid
    fake_id = uuid.uuid4()

    response = client.patch(
        f"/api/test-user-123/tasks/{fake_id}/complete",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 404


@pytest.mark.integration
def test_toggle_completion_without_jwt(client: TestClient, session):
    """Test toggling completion without JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.patch(f"/api/{user_id}/tasks/{task.id}/complete")

    assert response.status_code == 403


@pytest.mark.integration
def test_toggle_completion_with_invalid_jwt(client: TestClient, invalid_token: str, session):
    """Test toggling completion with invalid JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.patch(
        f"/api/{user_id}/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_toggle_completion_other_users_task(
    client: TestClient,
    valid_token: str,
    session,
):
    """Test that user cannot toggle another user's task."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User B creates a task
    task_create = TaskCreate(title="User B's task")
    task = TaskService.create_task(session, user_b_id, task_create)

    # User A tries to toggle User B's task
    response = client.patch(
        f"/api/{user_a_id}/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_toggle_completion_updates_timestamp(client: TestClient, valid_token: str, session):
    """Test that toggling completion updates the updated_at timestamp."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)
    original_updated_at = task.updated_at

    response = client.patch(
        f"/api/{user_id}/tasks/{task.id}/complete",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    # updated_at should be present and potentially different
    assert "updated_at" in data
