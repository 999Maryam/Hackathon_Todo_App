"""Integration tests for POST /api/{user_id}/tasks endpoint."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_create_task_with_valid_jwt(client: TestClient, valid_token: str):
    """Test creating a task with valid JWT token returns 201 Created."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["completed"] is False
    assert data["user_id"] == "test-user-123"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.integration
def test_create_task_without_jwt_token(client: TestClient):
    """Test creating a task without JWT token returns 403."""
    response = client.post(
        "/api/test-user-123/tasks",
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_create_task_with_invalid_jwt(client: TestClient, invalid_token: str):
    """Test creating a task with invalid JWT returns 403."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {invalid_token}"},
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 403


@pytest.mark.integration
def test_create_task_with_expired_jwt(client: TestClient, expired_token: str):
    """Test creating a task with expired JWT returns 401."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {expired_token}"},
        json={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 401


@pytest.mark.integration
def test_create_task_with_missing_title(client: TestClient, valid_token: str):
    """Test creating a task without title returns 400 Bad Request."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_create_task_with_empty_title(client: TestClient, valid_token: str):
    """Test creating a task with empty title returns 400 Bad Request."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "",
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_create_task_with_title_too_long(client: TestClient, valid_token: str):
    """Test creating a task with title > 255 chars returns 400."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "x" * 256,
            "description": "Milk, eggs, bread",
        },
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_create_task_with_description_too_long(client: TestClient, valid_token: str):
    """Test creating a task with description > 2000 chars returns 400."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Buy groceries",
            "description": "x" * 2001,
        },
    )

    assert response.status_code == 400


@pytest.mark.integration
def test_create_task_with_minimal_data(client: TestClient, valid_token: str):
    """Test creating a task with only title (description optional)."""
    response = client.post(
        "/api/test-user-123/tasks",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Finish project",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Finish project"
    assert data["description"] is None
    assert data["completed"] is False
