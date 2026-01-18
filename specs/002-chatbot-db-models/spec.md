# Feature Specification: Database Models & Persistence Layer for Todo AI Chatbot

**Feature Branch**: `001-chatbot-db-models`
**Created**: 2026-01-14
**Status**: Draft
**Phase**: III - Spec 1 of 4
**Input**: User description: "Database Models & Persistence Layer for Todo AI Chatbot (Phase III – Spec 1)"

---

## Overview

This specification defines the database models and persistence layer required to support a stateless AI chatbot for the Todo application. The chatbot requires persistent conversation storage so that:
- Chat sessions survive server restarts
- The server remains stateless (all state in database)
- Multi-user isolation is strictly enforced
- The existing Task model from Phase II is preserved

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Persist a Conversation (Priority: P1)

A user opens the chat interface for the first time in a session. The system creates a new conversation record linked to their user account. All subsequent messages in this chat session are persisted to the database.

**Why this priority**: This is the foundational capability. Without conversation persistence, no chat functionality can work reliably.

**Independent Test**: Can be fully tested by creating a conversation via helper function and verifying it exists in the database with correct user_id.

**Acceptance Scenarios**:

1. **Given** an authenticated user with no active conversation, **When** the system creates a new conversation, **Then** a conversation record is created with the user's ID and current timestamp.
2. **Given** an authenticated user, **When** a conversation is created, **Then** the conversation is retrievable only by that user (not by other users).

---

### User Story 2 - Add Messages to a Conversation (Priority: P1)

A user sends a message through the chat interface. The system persists the user's message, processes it, and persists the assistant's response. Both messages are linked to the same conversation with proper role distinction.

**Why this priority**: Message persistence is equally critical as conversation creation - without it, the chatbot has no memory.

**Independent Test**: Can be tested by adding user and assistant messages to a conversation and verifying both are stored with correct roles and timestamps.

**Acceptance Scenarios**:

1. **Given** an existing conversation, **When** a user message is added, **Then** the message is stored with role="user", correct content, and current timestamp.
2. **Given** an existing conversation, **When** an assistant message is added, **Then** the message is stored with role="assistant", correct content, and current timestamp.
3. **Given** a user message with empty content, **When** attempting to save, **Then** the system rejects the message with a validation error.

---

### User Story 3 - Retrieve Ordered Message History (Priority: P1)

When processing a new user message, the system retrieves the full conversation history in chronological order to provide context to the AI agent.

**Why this priority**: Without ordered history retrieval, the AI agent cannot understand conversation context.

**Independent Test**: Can be tested by adding multiple messages in a specific order and verifying retrieval returns them in created_at ascending order.

**Acceptance Scenarios**:

1. **Given** a conversation with multiple messages, **When** history is retrieved, **Then** messages are returned in chronological order (oldest first).
2. **Given** a conversation with messages from User A, **When** User B requests the history, **Then** an empty result is returned (no cross-user access).
3. **Given** a conversation with 10 messages, **When** history is retrieved, **Then** all 10 messages are returned with correct roles and content.

---

### User Story 4 - Get or Create Conversation (Priority: P2)

When a user starts chatting, the system either retrieves their existing active conversation or creates a new one if none exists. This simplifies the calling code.

**Why this priority**: This is a convenience helper that combines create and get operations - important but less fundamental than individual operations.

**Independent Test**: Can be tested by calling the helper twice for the same user and verifying the same conversation is returned both times.

**Acceptance Scenarios**:

1. **Given** a user with no existing conversation, **When** get_or_create is called, **Then** a new conversation is created and returned.
2. **Given** a user with an existing conversation, **When** get_or_create is called, **Then** the existing conversation is returned (not duplicated).

---

### Edge Cases

- What happens when a message with an invalid role (not "user" or "assistant") is submitted?
  - System rejects with validation error
- What happens when retrieving history for a non-existent conversation?
  - System returns empty list (not an error)
- What happens when adding a message to a conversation owned by a different user?
  - System rejects the operation (enforces ownership)
- What happens when content exceeds reasonable limits?
  - System truncates or rejects based on database constraints
- What happens during concurrent message additions?
  - Messages are ordered by created_at timestamp; database handles concurrency

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define a Conversation model with fields: id (auto-increment integer, primary key), user_id (string, foreign key to users), created_at (datetime), updated_at (datetime)
- **FR-002**: System MUST define a Message model with fields: id (auto-increment integer, primary key), conversation_id (integer, foreign key to conversation), user_id (string, foreign key to users), role (string: "user" or "assistant"), content (text, not empty), created_at (datetime)
- **FR-003**: System MUST NOT modify or break the existing Task model from Phase II
- **FR-004**: System MUST create an index on conversation.user_id for fast user-scoped queries
- **FR-005**: System MUST create a composite index on message.conversation_id + message.created_at for fast ordered retrieval
- **FR-006**: System MUST provide a helper function to create a new conversation for a given user_id
- **FR-007**: System MUST provide a helper function to add a user message to a conversation (validates user_id ownership)
- **FR-008**: System MUST provide a helper function to add an assistant message to a conversation (validates user_id ownership)
- **FR-009**: System MUST provide a helper function to retrieve full ordered message history for a conversation (validates user_id ownership, orders by created_at ascending)
- **FR-010**: System MUST provide a helper function to get an existing conversation or create a new one if none exists for a user
- **FR-011**: System MUST reject messages with empty content
- **FR-012**: System MUST reject messages with roles other than "user" or "assistant"
- **FR-013**: All database operations MUST filter by user_id to prevent cross-user data access
- **FR-014**: Timestamps (created_at, updated_at) MUST use server-side defaults (datetime.utcnow)
- **FR-015**: System MUST reuse the existing database connection and session management from Phase II

### Key Entities

- **User**: Existing entity from Phase II. Represents an authenticated user. Has id (string, PK), email, name, password_hash, created_at.

- **Task**: Existing entity from Phase II. Represents a todo item. Has id (UUID, PK), user_id (FK to users), title, description, completed, created_at, updated_at. MUST NOT be modified.

- **Conversation**: New entity. Represents a chat session. One user can have many conversations. Fields: id (int, PK), user_id (string, FK to users), created_at (datetime), updated_at (datetime).

- **Message**: New entity. Represents a single message in a conversation. Fields: id (int, PK), conversation_id (int, FK to conversation), user_id (string, FK to users, for ownership validation), role ("user" or "assistant"), content (text), created_at (datetime).

### Entity Relationships

```
User (1) ──────< (many) Conversation
User (1) ──────< (many) Task (existing from Phase II)
Conversation (1) ──────< (many) Message
User (1) ──────< (many) Message (ownership validation)
```

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All three models (Task, Conversation, Message) are queryable and relationships work correctly - verified by creating linked records and traversing relationships.

- **SC-002**: User isolation is enforced - verified by attempting cross-user access and confirming zero results returned.

- **SC-003**: Message ordering is reliable - verified by adding messages with known timestamps and confirming retrieval order matches creation order.

- **SC-004**: Helper functions operate correctly - verified by integration tests that create conversation, add 5+ messages, and retrieve ordered history.

- **SC-005**: Schema is compatible with existing Phase II setup - verified by running existing tests after adding new models (no regressions).

- **SC-006**: Validation rules are enforced - verified by attempting to create messages with empty content or invalid roles and confirming rejection.

- **SC-007**: Database indexes are created - verified by checking database schema or using EXPLAIN on queries.

---

## Constraints

- **Mandatory technologies**: SQLModel (ORM + Pydantic), Neon Serverless PostgreSQL
- **Database**: Use existing DATABASE_URL from Phase II - do NOT create a new database
- **Existing code**: Do NOT drop, rename, or modify existing Task table/fields
- **Session management**: Reuse Phase II database session/engine setup
- **No pagination**: Keep simple - retrieve all messages for a conversation
- **No caching**: Always read/write directly from/to database
- **No advanced features**: No message attachments, edits, deletions, or threading
- **No conversation metadata**: No title, summary, or other extended fields (keep minimal)

---

## Assumptions

- Phase II database connection is working and accessible
- User authentication (JWT verification, current_user dependency) is functional from Phase II
- The `users` table exists and has records for testing
- Alembic migrations or SQLModel metadata sync will handle schema updates
- Message content can be text of reasonable length (database default TEXT type limits apply)

---

## Out of Scope

- MCP tools integration (Phase III - Spec 2)
- OpenAI agent setup or runner (Phase III - Spec 3)
- Chat API endpoint /api/chat (Phase III - Spec 4)
- Frontend/ChatKit integration
- Authentication logic (reusing Phase II)
- Message attachments, edits, deletions, or threading
- Advanced conversation metadata (title, summary, etc.)
- Pagination or archiving of messages

---

## Deliverables

1. **SQLModel Classes**: New/updated model classes in `backend/app/models/`
   - `conversation.py` - Conversation model
   - `message.py` - Message model
   - Update `__init__.py` to export new models

2. **Helper Functions**: CRUD operations in `backend/app/` (crud/ or services/ directory)
   - `create_conversation(user_id, db) -> Conversation`
   - `get_conversation(conversation_id, user_id, db) -> Conversation | None`
   - `get_or_create_conversation(user_id, db) -> Conversation`
   - `add_user_message(conversation_id, user_id, content, db) -> Message`
   - `add_assistant_message(conversation_id, user_id, content, db) -> Message`
   - `get_conversation_history(conversation_id, user_id, db) -> list[dict]`

3. **Tests**: Integration tests in `backend/tests/`
   - Test conversation creation with user isolation
   - Test message addition with role validation
   - Test ordered history retrieval
   - Test cross-user access prevention

4. **Schema Documentation**: Update or create `specs/database/schema.md` with new models
