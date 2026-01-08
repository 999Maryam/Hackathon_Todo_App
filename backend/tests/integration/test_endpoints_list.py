"""Integration tests for GET /api/{user_id}/tasks endpoint."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
def test_list_tasks_with_valid_jwt(client: TestClient, valid_token: str, session):
    """Test listing tasks with valid JWT returns 200 OK."""
    user_id = "test-user-123"

    # Create a task first
    task_create = TaskCreate(title="Buy groceries")
    TaskService.create_task(session, user_id, task_create)

    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "tasks" in data
    assert isinstance(data["tasks"], list)
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "Buy groceries"


@pytest.mark.integration
def test_list_tasks_empty_list(client: TestClient, valid_token: str):
    """Test listing tasks with no tasks returns 200 OK with empty list."""
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []


@pytest.mark.integration
def test_list_multiple_tasks(client: TestClient, valid_token: str, session):
    """Test listing 3 tasks returns all 3 tasks."""
    user_id = "test-user-123"

    # Create 3 tasks
    for i in range(3):
        task_create = TaskCreate(title=f"Task {i+1}")
        TaskService.create_task(session, user_id, task_create)

    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 3
    titles = [task["title"] for task in data["tasks"]]
    assert "Task 1" in titles
    assert "Task 2" in titles
    assert "Task 3" in titles


@pytest.mark.integration
def test_list_tasks_without_jwt(client: TestClient):
    """Test listing tasks without JWT returns 403."""
    response = client.get("/api/test-user-123/tasks")

    assert response.status_code == 403


@pytest.mark.integration
def test_list_tasks_with_invalid_jwt(client: TestClient, invalid_token: str):
    """Test listing tasks with invalid JWT returns 403."""
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {invalid_token}"},
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_list_tasks_with_expired_jwt(client: TestClient, expired_token: str):
    """Test listing tasks with expired JWT returns 401."""
    response = client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 401
