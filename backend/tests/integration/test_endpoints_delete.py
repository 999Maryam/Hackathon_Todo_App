"""Integration tests for DELETE /api/{user_id}/tasks/{id} endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_delete_task_with_valid_jwt(client: TestClient, valid_token: str, session):
    """Test deleting a task with valid JWT returns 204 No Content."""
    user_id = "test-user-123"

    # Create a task first
    task_create = TaskCreate(title="Task to delete")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.delete(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 204


@pytest.mark.integration
def test_delete_task_removes_from_database(client: TestClient, valid_token: str, session):
    """Test that delete removes task from database (subsequent GET returns 404)."""
    user_id = "test-user-123"

    # Create and delete a task
    task_create = TaskCreate(title="Task to delete")
    task = TaskService.create_task(session, user_id, task_create)
    task_id = task.id

    # Delete it
    response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 204

    # Try to get it - should be 404
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response.status_code == 404


@pytest.mark.integration
def test_delete_task_with_nonexistent_id(client: TestClient, valid_token: str):
    """Test deleting non-existent task returns 404."""
    import uuid
    fake_id = uuid.uuid4()

    response = client.delete(
        f"/api/test-user-123/tasks/{fake_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 404


@pytest.mark.integration
def test_delete_task_without_jwt(client: TestClient, session):
    """Test deleting task without JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.delete(f"/api/{user_id}/tasks/{task.id}")

    assert response.status_code == 403


@pytest.mark.integration
def test_delete_task_with_invalid_jwt(client: TestClient, invalid_token: str, session):
    """Test deleting task with invalid JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.delete(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_delete_other_users_task(
    client: TestClient,
    valid_token: str,
    session,
):
    """Test that user cannot delete another user's task."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User B creates a task
    task_create = TaskCreate(title="User B's task")
    task = TaskService.create_task(session, user_b_id, task_create)

    # User A tries to delete User B's task
    response = client.delete(
        f"/api/{user_a_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_delete_task_twice(client: TestClient, valid_token: str, session):
    """Test deleting the same task twice - first 204, second 404."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    # First delete - should succeed
    response1 = client.delete(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response1.status_code == 204

    # Second delete - should fail with 404
    response2 = client.delete(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )
    assert response2.status_code == 404
