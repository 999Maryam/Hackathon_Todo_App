"""
Test suite for the chat endpoint.

Task: T041 | Spec: specs/008-chat-endpoint-ui/spec.md
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import AsyncMock, patch

from app.main import app
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.agents.chat_runner import AgentResponse, ToolCallRecord


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_user(db_session: Session):
    """Create a sample user for testing."""
    user = User(
        id="test_user_123",
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def valid_jwt_token(sample_user: User):
    """Create a valid JWT token for the sample user."""
    from app.auth import BETTER_AUTH_SECRET
    import jwt

    token = jwt.encode(
        {"sub": sample_user.id, "exp": 9999999999},  # Far future expiry
        BETTER_AUTH_SECRET,
        algorithm="HS256"
    )
    return token


def test_chat_endpoint_success(client, sample_user, valid_jwt_token, db_session):
    """Test successful chat endpoint call."""
    # Mock the run_agent_with_tools function
    mock_response = AgentResponse(
        content="Sure, I can help you with that!",
        tool_calls=[],
        conversation_id=1
    )

    with patch('app.routers.chat.run_agent_with_tools', new_callable=AsyncMock) as mock_func:
        mock_func.return_value = mock_response

        response = client.post(
            f"/api/{sample_user.id}/chat",
            json={
                "message": "Hello, can you help me?",
                "conversation_id": None
            },
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Sure, I can help you with that!"
        assert data["conversation_id"] == 1
        assert data["tool_calls"] == []


def test_chat_endpoint_unauthorized(client):
    """Test chat endpoint without valid JWT token."""
    response = client.post(
        "/api/test_user/chat",
        json={
            "message": "Hello",
            "conversation_id": None
        },
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401


def test_chat_endpoint_forbidden(client, sample_user, valid_jwt_token):
    """Test chat endpoint with mismatched user_id and token."""
    response = client.post(
        "/api/other_user_id/chat",
        json={
            "message": "Hello",
            "conversation_id": None
        },
        headers={"Authorization": f"Bearer {valid_jwt_token}"}
    )

    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_chat_endpoint_validation_error(client, sample_user, valid_jwt_token):
    """Test chat endpoint with invalid request body."""
    response = client.post(
        f"/api/{sample_user.id}/chat",
        json={},  # Missing required fields
        headers={"Authorization": f"Bearer {valid_jwt_token}"}
    )

    assert response.status_code == 422  # Validation error


def test_chat_endpoint_with_tool_calls(client, sample_user, valid_jwt_token):
    """Test chat endpoint that returns tool calls."""
    # Mock response with tool calls
    mock_tool_call = ToolCallRecord(
        name="add_task",
        arguments={"title": "Test task", "description": "Test description"},
        result={"task_id": 1, "status": "created"}
    )

    mock_response = AgentResponse(
        content="I've added your task for you.",
        tool_calls=[mock_tool_call],
        conversation_id=1
    )

    with patch('app.routers.chat.run_agent_with_tools', new_callable=AsyncMock) as mock_func:
        mock_func.return_value = mock_response

        response = client.post(
            f"/api/{sample_user.id}/chat",
            json={
                "message": "Add a task called 'Test task'",
                "conversation_id": None
            },
            headers={"Authorization": f"Bearer {valid_jwt_token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "I've added your task for you."
        assert len(data["tool_calls"]) == 1
        assert data["tool_calls"][0]["name"] == "add_task"
        assert data["tool_calls"][0]["arguments"]["title"] == "Test task"


def test_conversation_isolation(client, valid_jwt_token):
    """Test that users cannot access other users' conversations."""
    # Test with a user_id that doesn't match the token
    other_user_id = "different_user_456"

    response = client.post(
        f"/api/{other_user_id}/chat",
        json={
            "message": "Hello",
            "conversation_id": None
        },
        headers={"Authorization": f"Bearer {valid_jwt_token}"}
    )

    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]