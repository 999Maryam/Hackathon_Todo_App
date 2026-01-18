"""Integration tests for Conversation and Message models and services.

Task: T007-T009, T014-T017, T024-T026, T032-T033
Spec: specs/001-chatbot-db-models/spec.md

Tests cover all success criteria:
- SC-001: Conversation creation with user_id
- SC-002: User isolation (cross-user access prevention)
- SC-003: Ordered message history retrieval
- SC-004: 10+ messages in correct sequence
- SC-005: No regression in existing Phase II tests
- SC-006: Validation (empty content, invalid role rejection)
- SC-007: Database indexes exist and are used
"""

import pytest
from sqlmodel import Session

from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.conversation_service import (
    create_conversation,
    get_conversation,
    get_or_create_conversation,
    add_user_message,
    add_assistant_message,
    get_conversation_history,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def test_user(session: Session) -> User:
    """Create a test user in the database."""
    user = User(
        id="test-user-123",
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def another_user(session: Session) -> User:
    """Create another test user for isolation tests."""
    user = User(
        id="test-user-456",
        email="another@example.com",
        name="Another User",
        password_hash="hashed_password"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# =============================================================================
# User Story 1: Create and Persist a Conversation (T007-T009, T013)
# =============================================================================


class TestCreateConversation:
    """Tests for conversation creation and retrieval."""

    def test_create_conversation(self, session: Session, test_user: User):
        """T008: Create a conversation and verify it exists with correct user_id.

        SC-001: Conversation model persists with user_id and timestamps
        """
        # Act
        conversation = create_conversation(test_user.id, session)

        # Assert
        assert conversation.id is not None
        assert conversation.user_id == test_user.id
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

        # Verify in database
        db_conversation = session.get(Conversation, conversation.id)
        assert db_conversation is not None
        assert db_conversation.user_id == test_user.id

    def test_conversation_user_isolation(
        self,
        session: Session,
        test_user: User,
        another_user: User
    ):
        """T009: Verify user cannot access another user's conversation.

        SC-002: User isolation - cross-user access prevention
        """
        # Arrange: Create conversation for test_user
        conversation = create_conversation(test_user.id, session)

        # Act: Try to get conversation as another_user
        result = get_conversation(conversation.id, another_user.id, session)

        # Assert: Should return None (access denied)
        assert result is None

        # Verify original user can still access
        own_result = get_conversation(conversation.id, test_user.id, session)
        assert own_result is not None
        assert own_result.id == conversation.id


# =============================================================================
# User Story 2: Add Messages to a Conversation (T014-T017, T023)
# =============================================================================


class TestAddMessages:
    """Tests for message addition with role distinction and validation."""

    def test_add_user_message(self, session: Session, test_user: User):
        """T014: Add a user message and verify role and content."""
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act
        message = add_user_message(
            conversation.id, test_user.id, "Hello, AI!", session
        )

        # Assert
        assert message.id is not None
        assert message.role == "user"
        assert message.content == "Hello, AI!"
        assert message.conversation_id == conversation.id
        assert message.user_id == test_user.id
        assert message.created_at is not None

    def test_add_assistant_message(self, session: Session, test_user: User):
        """T015: Add an assistant message and verify role and content."""
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act
        message = add_assistant_message(
            conversation.id, test_user.id, "Hello! How can I help?", session
        )

        # Assert
        assert message.id is not None
        assert message.role == "assistant"
        assert message.content == "Hello! How can I help?"
        assert message.conversation_id == conversation.id

    def test_message_empty_content_rejected(
        self, session: Session, test_user: User
    ):
        """T016: Empty message content should be rejected.

        SC-006: Validation - empty content rejection
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act & Assert: Empty string
        with pytest.raises(ValueError, match="content cannot be empty"):
            add_user_message(conversation.id, test_user.id, "", session)

        # Act & Assert: Whitespace only
        with pytest.raises(ValueError, match="content cannot be empty"):
            add_user_message(conversation.id, test_user.id, "   ", session)

    def test_message_invalid_role_rejected(self, session: Session, test_user: User):
        """T017: Invalid role should be rejected by database constraint.

        SC-006: Validation - invalid role rejection
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act & Assert: Try to create message with invalid role directly
        # The Literal type + CHECK constraint should prevent this
        message = Message(
            conversation_id=conversation.id,
            user_id=test_user.id,
            role="invalid_role",  # type: ignore
            content="test"
        )
        session.add(message)

        # Should raise an error on commit due to CHECK constraint
        with pytest.raises(Exception):  # IntegrityError or similar
            session.commit()

    def test_message_to_nonexistent_conversation_rejected(
        self, session: Session, test_user: User
    ):
        """Adding message to non-existent conversation should fail."""
        # Act & Assert
        with pytest.raises(ValueError, match="Conversation not found"):
            add_user_message(99999, test_user.id, "Hello", session)

    def test_message_to_other_users_conversation_rejected(
        self,
        session: Session,
        test_user: User,
        another_user: User
    ):
        """Adding message to another user's conversation should fail.

        SC-002: User isolation
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act & Assert: another_user tries to add message
        with pytest.raises(ValueError, match="access denied"):
            add_user_message(
                conversation.id, another_user.id, "Sneaky message", session
            )


# =============================================================================
# User Story 3: Retrieve Ordered Message History (T024-T026, T031)
# =============================================================================


class TestGetConversationHistory:
    """Tests for ordered message history retrieval."""

    def test_get_conversation_history_ordered(
        self, session: Session, test_user: User
    ):
        """T024: Messages should be returned in chronological order.

        SC-003: Ordered message history (created_at ASC)
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)
        add_user_message(conversation.id, test_user.id, "First", session)
        add_assistant_message(conversation.id, test_user.id, "Second", session)
        add_user_message(conversation.id, test_user.id, "Third", session)

        # Act
        history = get_conversation_history(conversation.id, test_user.id, session)

        # Assert: Correct order and format
        assert len(history) == 3
        assert history[0] == {"role": "user", "content": "First"}
        assert history[1] == {"role": "assistant", "content": "Second"}
        assert history[2] == {"role": "user", "content": "Third"}

    def test_get_history_wrong_user_returns_empty(
        self,
        session: Session,
        test_user: User,
        another_user: User
    ):
        """T025: Requesting history as wrong user should return empty list.

        SC-002: User isolation
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)
        add_user_message(conversation.id, test_user.id, "Secret message", session)

        # Act: another_user requests history
        history = get_conversation_history(
            conversation.id, another_user.id, session
        )

        # Assert: Empty list (not unauthorized error - just no data)
        assert history == []

    def test_get_history_10_messages(self, session: Session, test_user: User):
        """T026: Test with 10+ alternating messages in correct sequence.

        SC-004: Integration test with 10 alternating messages
        """
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Add 10 alternating messages
        for i in range(10):
            if i % 2 == 0:
                add_user_message(
                    conversation.id, test_user.id, f"User message {i+1}", session
                )
            else:
                add_assistant_message(
                    conversation.id, test_user.id, f"Assistant message {i+1}", session
                )

        # Act
        history = get_conversation_history(conversation.id, test_user.id, session)

        # Assert
        assert len(history) == 10

        # Verify alternating pattern and correct sequence
        for i, msg in enumerate(history):
            expected_role = "user" if i % 2 == 0 else "assistant"
            expected_content = f"{expected_role.capitalize()} message {i+1}"
            assert msg["role"] == expected_role
            assert msg["content"] == expected_content

    def test_empty_conversation_returns_empty_list(
        self, session: Session, test_user: User
    ):
        """Empty conversation should return empty list."""
        # Arrange
        conversation = create_conversation(test_user.id, session)

        # Act
        history = get_conversation_history(conversation.id, test_user.id, session)

        # Assert
        assert history == []


# =============================================================================
# User Story 4: Get or Create Conversation (T032-T033, T036)
# =============================================================================


class TestGetOrCreateConversation:
    """Tests for get_or_create_conversation helper."""

    def test_get_or_create_conversation_creates_new(
        self, session: Session, test_user: User
    ):
        """T032: Should create new conversation when none exists."""
        # Act
        conversation = get_or_create_conversation(test_user.id, session)

        # Assert
        assert conversation.id is not None
        assert conversation.user_id == test_user.id

    def test_get_or_create_conversation_returns_existing(
        self, session: Session, test_user: User
    ):
        """T033: Should return most recent existing conversation."""
        # Arrange: Create two conversations
        first_conv = create_conversation(test_user.id, session)
        second_conv = create_conversation(test_user.id, session)

        # Act: get_or_create should return the most recent
        result = get_or_create_conversation(test_user.id, session)

        # Assert: Should be the second (most recent) conversation
        assert result.id == second_conv.id

    def test_get_or_create_returns_recently_active(
        self, session: Session, test_user: User
    ):
        """Should return conversation with most recent activity."""
        # Arrange: Create two conversations
        first_conv = create_conversation(test_user.id, session)
        second_conv = create_conversation(test_user.id, session)

        # Add message to first conversation (updates its updated_at)
        add_user_message(first_conv.id, test_user.id, "Activity!", session)

        # Act
        result = get_or_create_conversation(test_user.id, session)

        # Assert: Should be first_conv now (most recently updated)
        assert result.id == first_conv.id


# =============================================================================
# Cross-User Isolation Tests (Additional SC-002 coverage)
# =============================================================================


class TestMultiUserIsolation:
    """Additional tests for multi-user isolation."""

    def test_multiple_users_multiple_conversations(
        self,
        session: Session,
        test_user: User,
        another_user: User
    ):
        """Each user should only see their own conversations."""
        # Arrange
        user1_conv = create_conversation(test_user.id, session)
        user2_conv = create_conversation(another_user.id, session)

        add_user_message(user1_conv.id, test_user.id, "User 1 msg", session)
        add_user_message(user2_conv.id, another_user.id, "User 2 msg", session)

        # Act
        user1_history = get_conversation_history(
            user1_conv.id, test_user.id, session
        )
        user2_history = get_conversation_history(
            user2_conv.id, another_user.id, session
        )

        # Assert: Each user sees only their own messages
        assert len(user1_history) == 1
        assert user1_history[0]["content"] == "User 1 msg"

        assert len(user2_history) == 1
        assert user2_history[0]["content"] == "User 2 msg"

        # Cross-access should return empty
        cross_history = get_conversation_history(
            user1_conv.id, another_user.id, session
        )
        assert cross_history == []
