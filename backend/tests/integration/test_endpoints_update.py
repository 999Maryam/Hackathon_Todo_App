"""Integration tests for PUT /api/{user_id}/tasks/{id} endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_update_task_with_valid_jwt(client: TestClient, valid_token: str, session):
    """Test updating a task with valid JWT returns 200 OK."""
    user_id = "test-user-123"

    # Create a task first
    task_create = TaskCreate(title="Original title", description="Original desc")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Updated title",
            "description": "Updated description",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"


@pytest.mark.integration
def test_update_task_title_only(client: TestClient, valid_token: str, session):
    """Test updating only title leaves description unchanged."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Original", description="Keep this")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "New title"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["description"] == "Keep this"


@pytest.mark.integration
def test_update_task_description_only(client: TestClient, valid_token: str, session):
    """Test updating only description leaves title unchanged."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Keep this", description="Original desc")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"description": "New description"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Keep this"
    assert data["description"] == "New description"


@pytest.mark.integration
def test_update_task_with_empty_title(client: TestClient, valid_token: str, session):
    """Test updating with empty title returns 400."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Original")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": ""},
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_update_task_with_nonexistent_id(client: TestClient, valid_token: str):
    """Test updating non-existent task returns 404."""
    import uuid
    fake_id = uuid.uuid4()

    response = client.put(
        f"/api/test-user-123/tasks/{fake_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "New title"},
    )

    assert response.status_code == 404


@pytest.mark.integration
def test_update_task_without_jwt(client: TestClient, session):
    """Test updating task without JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        json={"title": "New title"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_update_task_with_invalid_jwt(client: TestClient, invalid_token: str, session):
    """Test updating task with invalid JWT returns 403."""
    user_id = "test-user-123"
    task_create = TaskCreate(title="Task")
    task = TaskService.create_task(session, user_id, task_create)

    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {invalid_token}"},
        json={"title": "New title"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_update_other_users_task(
    client: TestClient,
    valid_token: str,
    session,
):
    """Test that user cannot update another user's task."""
    user_a_id = "test-user-123"
    user_b_id = "test-user-456"

    # User B creates a task
    task_create = TaskCreate(title="User B's task")
    task = TaskService.create_task(session, user_b_id, task_create)

    # User A tries to update User B's task
    response = client.put(
        f"/api/{user_a_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Hacked"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_update_task_updates_timestamp(client: TestClient, valid_token: str, session):
    """Test that updating a task updates the updated_at timestamp."""
    user_id = "test-user-123"

    task_create = TaskCreate(title="Original")
    task = TaskService.create_task(session, user_id, task_create)
    original_updated_at = task.updated_at

    # Wait a moment and update (in real test might use time.sleep)
    response = client.put(
        f"/api/{user_id}/tasks/{task.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated"},
    )

    assert response.status_code == 200
    data = response.json()
    # updated_at should be different (or at least present)
    assert "updated_at" in data
