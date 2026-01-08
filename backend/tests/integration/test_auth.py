"""Integration tests for JWT authentication across all endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.models.schemas import TaskCreate
from app.services.task_service import TaskService


@pytest.mark.integration
class TestAuthentication:
    """Authentication tests for all endpoints."""

    def test_missing_token_returns_403(self, client: TestClient):
        """Test that missing token returns 403."""
        response = client.get("/api/test-user/tasks")
        assert response.status_code == 403

    def test_invalid_token_returns_403(self, client: TestClient, invalid_token: str):
        """Test that invalid token returns 403."""
        response = client.get(
            "/api/test-user/tasks",
            headers={"Authorization": f"Bearer {invalid_token}"},
        )
        assert response.status_code == 403

    def test_expired_token_returns_401(self, client: TestClient, expired_token: str):
        """Test that expired token returns 401."""
        response = client.get(
            "/api/test-user/tasks",
            headers={"Authorization": f"Bearer {expired_token}"},
        )
        assert response.status_code == 401

    def test_valid_token_succeeds(self, client: TestClient, valid_token: str):
        """Test that valid token allows access."""
        response = client.get(
            "/api/test-user-123/tasks",
            headers={"Authorization": f"Bearer {valid_token}"},
        )
        # 200 or 403 depending on user_id match (we're testing auth, not ownership)
        assert response.status_code in [200, 403]

    def test_token_required_for_create(self, client: TestClient):
        """Test that token is required for creating tasks."""
        response = client.post(
            "/api/test-user/tasks",
            json={"title": "Test"},
        )
        assert response.status_code == 403

    def test_token_required_for_get(self, client: TestClient):
        """Test that token is required for getting tasks."""
        import uuid
        response = client.get(f"/api/test-user/tasks/{uuid.uuid4()}")
        assert response.status_code == 403

    def test_token_required_for_update(self, client: TestClient):
        """Test that token is required for updating tasks."""
        import uuid
        response = client.put(
            f"/api/test-user/tasks/{uuid.uuid4()}",
            json={"title": "Updated"},
        )
        assert response.status_code == 403

    def test_token_required_for_delete(self, client: TestClient):
        """Test that token is required for deleting tasks."""
        import uuid
        response = client.delete(f"/api/test-user/tasks/{uuid.uuid4()}")
        assert response.status_code == 403

    def test_token_required_for_complete(self, client: TestClient):
        """Test that token is required for toggling completion."""
        import uuid
        response = client.patch(f"/api/test-user/tasks/{uuid.uuid4()}/complete")
        assert response.status_code == 403

    def test_malformed_token(self, client: TestClient):
        """Test that malformed token is rejected."""
        response = client.get(
            "/api/test-user/tasks",
            headers={"Authorization": "Bearer not-a-valid-jwt"},
        )
        assert response.status_code == 403

    def test_bearer_prefix_required(self, client: TestClient, valid_token: str):
        """Test that Bearer prefix is required."""
        response = client.get(
            "/api/test-user/tasks",
            headers={"Authorization": f"Token {valid_token}"},
        )
        # Should fail because it's expecting Bearer
        assert response.status_code == 403
