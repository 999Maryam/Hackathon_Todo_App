"""Tests for multi-user data isolation and ownership enforcement."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_user_cannot_access_other_users_tasks(
    client: TestClient,
    valid_token: str,
    another_user_token: str,
    session,
):
    """Test that user_A cannot see user_B's tasks."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User B creates a task
    task_create = TaskCreate(title="User B's task")
    TaskService.create_task(session, user_b_id, task_create)

    # User A tries to list User B's tasks
    response = client.get(
        f"/api/{user_b_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},  # User A's token
    )

    # Should get 403 Forbidden
    assert response.status_code == 403


@pytest.mark.integration
def test_url_mismatch_with_jwt_mismatch(
    client: TestClient,
    valid_token: str,
    another_user_token: str,
    session,
):
    """Test that JWT user_id must match URL user_id."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # Try to access User B's tasks with User A's token
    response = client.get(
        f"/api/{user_b_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_task_isolation_between_users(client: TestClient, session):
    """Test that tasks are isolated between different users."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User A creates a task
    task_a = TaskCreate(title="Task for User A")
    TaskService.create_task(session, user_a_id, task_a)

    # User B creates a task
    task_b = TaskCreate(title="Task for User B")
    TaskService.create_task(session, user_b_id, task_b)

    # Verify User A's token only lists User A's tasks
    token_a = "valid-token-user-a"  # Would be valid token for user A
    token_b = "valid-token-user-b"  # Would be valid token for user B

    # Create valid tokens for both users
    from app.api.dependencies import create_test_token
    token_a = create_test_token(user_a_id)
    token_b = create_test_token(user_b_id)

    response_a = client.get(
        f"/api/{user_a_id}/tasks",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert response_a.status_code == 200
    assert len(response_a.json()["tasks"]) == 1
    assert response_a.json()["tasks"][0]["title"] == "Task for User A"

    response_b = client.get(
        f"/api/{user_b_id}/tasks",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert response_b.status_code == 200
    assert len(response_b.json()["tasks"]) == 1
    assert response_b.json()["tasks"][0]["title"] == "Task for User B"
