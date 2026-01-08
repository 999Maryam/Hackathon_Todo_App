"""Pytest configuration and fixtures for testing."""

import os
from datetime import datetime, timedelta
from typing import Generator

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from app.api.dependencies import create_test_token
from app.config import settings
from app.database import get_session
from app.main import app


# Use SQLite in-memory database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def engine():
    """Create test database engine."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine) -> Generator[Session, None, None]:
    """Create test database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection,
        class_=Session,
    )
    session = session_local()

    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(session) -> TestClient:
    """Create test client with overridden dependencies."""
    return TestClient(app)


@pytest.fixture
def valid_token() -> str:
    """Create a valid JWT token for testing."""
    return create_test_token("test-user-123")


@pytest.fixture
def another_user_token() -> str:
    """Create a valid JWT token for another user."""
    return create_test_token("test-user-456")


@pytest.fixture
def expired_token() -> str:
    """Create an expired JWT token."""
    payload = {
        "user_id": "test-user-123",
        "exp": datetime.utcnow() - timedelta(hours=1),
    }
    token = jwt.encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256",
    )
    return token


@pytest.fixture
def invalid_token() -> str:
    """Create an invalid JWT token (wrong secret)."""
    payload = {
        "user_id": "test-user-123",
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    token = jwt.encode(
        payload,
        "wrong-secret",
        algorithm="HS256",
    )
    return token
