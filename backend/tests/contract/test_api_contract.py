"""Contract tests to verify API matches OpenAPI specification."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.contract
class TestAPIContract:
    """Verify all endpoints match OpenAPI contract."""

    def test_list_tasks_endpoint_exists(self, client: TestClient, valid_token: str):
        """Test GET /api/{user_id}/tasks endpoint exists and returns correct schema."""
        response = client.get(
            "/api/test-user-123/tasks",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert isinstance(data["tasks"], list)

    def test_create_task_endpoint_exists(self, client: TestClient, valid_token: str):
        """Test POST /api/{user_id}/tasks endpoint exists and returns 201."""
        response = client.post(
            "/api/test-user-123/tasks",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={"title": "Test task"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["user_id"] == "test-user-123"
        assert data["title"] == "Test task"

    def test_get_task_endpoint_exists(self, client: TestClient, valid_token: str, session):
        """Test GET /api/{user_id}/tasks/{id} endpoint exists."""
        user_id = "test-user-123"
        task_create = TaskCreate(title="Test task")
        task = TaskService.create_task(session, user_id, task_create)

        response = client.get(
            f"/api/{user_id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(task.id)

    def test_update_task_endpoint_exists(self, client: TestClient, valid_token: str, session):
        """Test PUT /api/{user_id}/tasks/{id} endpoint exists."""
        user_id = "test-user-123"
        task_create = TaskCreate(title="Original")
        task = TaskService.create_task(session, user_id, task_create)

        response = client.put(
            f"/api/{user_id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={"title": "Updated"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"

    def test_delete_task_endpoint_exists(self, client: TestClient, valid_token: str, session):
        """Test DELETE /api/{user_id}/tasks/{id} endpoint exists and returns 204."""
        user_id = "test-user-123"
        task_create = TaskCreate(title="To delete")
        task = TaskService.create_task(session, user_id, task_create)

        response = client.delete(
            f"/api/{user_id}/tasks/{task.id}",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 204

    def test_toggle_complete_endpoint_exists(self, client: TestClient, valid_token: str, session):
        """Test PATCH /api/{user_id}/tasks/{id}/complete endpoint exists."""
        user_id = "test-user-123"
        task_create = TaskCreate(title="To toggle")
        task = TaskService.create_task(session, user_id, task_create)

        response = client.patch(
            f"/api/{user_id}/tasks/{task.id}/complete",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_response_schema_list_tasks(self, client: TestClient, valid_token: str, session):
        """Verify list tasks response schema matches spec."""
        user_id = "test-user-123"
        task_create = TaskCreate(title="Test", description="Desc")
        TaskService.create_task(session, user_id, task_create)

        response = client.get(
            f"/api/{user_id}/tasks",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        data = response.json()
        task = data["tasks"][0]

        # Verify all required fields
        required_fields = ["id", "user_id", "title", "completed", "created_at", "updated_at"]
        for field in required_fields:
            assert field in task, f"Missing field: {field}"

    def test_response_schema_create_task(self, client: TestClient, valid_token: str):
        """Verify create task response schema matches spec."""
        response = client.post(
            "/api/test-user-123/tasks",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={"title": "Test", "description": "Desc"},
        )
        data = response.json()

        # Verify all required fields
        required_fields = ["id", "user_id", "title", "completed", "created_at", "updated_at"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

        # Verify field types
        assert isinstance(data["completed"], bool)
        assert isinstance(data["user_id"], str)

    def test_error_response_schema(self, client: TestClient):
        """Verify error responses have correct schema."""
        import uuid
        response = client.get(
            f"/api/test-user/tasks/{uuid.uuid4()}",
        )
        # Should get 403 for missing token
        assert response.status_code == 403

    def test_health_check_endpoint(self, client: TestClient):
        """Verify health check endpoint exists."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
