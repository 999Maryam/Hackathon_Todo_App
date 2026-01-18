# Tasks: Database Models & Persistence Layer

**Input**: Design documents from `/specs/001-chatbot-db-models/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/conversation-service.md

**Tests**: Integration tests included as explicitly requested in spec.md deliverables section.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a **web application** with backend focus:
- Backend: `backend/app/` for source, `backend/tests/` for tests
- Models: `backend/app/models/`
- Services: `backend/app/services/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare directory structure and ensure models are properly exported

- [ ] T001 Create services directory at backend/app/services/
- [ ] T002 Create services __init__.py at backend/app/services/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create base models that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Create Conversation model in backend/app/models/conversation.py (FR-001, FR-004)
- [ ] T004 [P] Create Message model in backend/app/models/message.py (FR-002, FR-005, FR-012)
- [ ] T005 Update models __init__.py to export Conversation and Message in backend/app/models/__init__.py
- [ ] T006 Sync database schema by running create_db_and_tables() or Alembic migration
- [ ] T006.5 [P] Add database indexes: conversation.user_id, message(conversation_id, created_at), message.user_id

**Checkpoint**: Models and schema ready - user story implementation can now begin

**Database Schema Sync Note**

- Use existing Phase II Alembic setup (preferred):
  - `alembic revision --autogenerate -m "Add Conversation & Message models"`
  - `alembic upgrade head`

- For quick local/dev iteration (if Alembic not ready):
  ```python
  from app.db import engine
  from app.models import Base
  Base.metadata.create_all(bind=engine)
---

## Phase 3: User Story 1 - Create and Persist a Conversation (Priority: P1) 🎯 MVP

**Goal**: Enable creation of conversation records linked to authenticated users with proper isolation

**Independent Test**: Create a conversation via helper function and verify it exists in database with correct user_id and timestamps

### Tests for User Story 1

- [ ] T007 [P] [US1] Create test file skeleton at backend/tests/test_conversation.py with pytest fixtures
- [ ] T008 [P] [US1] Write test_create_conversation in backend/tests/test_conversation.py (SC-001)
- [ ] T009 [P] [US1] Write test_conversation_user_isolation in backend/tests/test_conversation.py (SC-002)

### Implementation for User Story 1

- [ ] T010 [US1] Implement create_conversation(user_id, db) in backend/app/services/conversation_service.py (FR-006)
- [ ] T011 [US1] Implement get_conversation(conversation_id, user_id, db) in backend/app/services/conversation_service.py (FR-013)
- [ ] T012 [US1] Add user_id ownership validation to get_conversation in backend/app/services/conversation_service.py (FR-013)
- [ ] T013 [US1] Run test_create_conversation and test_conversation_user_isolation to verify

**Checkpoint**: User Story 1 complete - conversations can be created and retrieved with user isolation

---

## Phase 4: User Story 2 - Add Messages to a Conversation (Priority: P1)

**Goal**: Enable adding user and assistant messages with role distinction and content validation

**Independent Test**: Add user and assistant messages to a conversation and verify both are stored with correct roles and timestamps

### Tests for User Story 2

- [ ] T014 [P] [US2] Write test_add_user_message in backend/tests/test_conversation.py
- [ ] T015 [P] [US2] Write test_add_assistant_message in backend/tests/test_conversation.py
- [ ] T016 [P] [US2] Write test_message_empty_content_rejected in backend/tests/test_conversation.py (SC-006)
- [ ] T017 [P] [US2] Write test_message_invalid_role_rejected in backend/tests/test_conversation.py (SC-006)

### Implementation for User Story 2

- [ ] T018 [US2] Implement _add_message internal helper in backend/app/services/conversation_service.py
- [ ] T019 [US2] Implement add_user_message(conversation_id, user_id, content, db) in backend/app/services/conversation_service.py (FR-007)
- [ ] T020 [US2] Implement add_assistant_message(conversation_id, user_id, content, db) in backend/app/services/conversation_service.py (FR-008)
- [ ] T021 [US2] Add content validation (empty content rejection) in backend/app/services/conversation_service.py (FR-011)
- [ ] T022 [US2] Add conversation ownership validation in _add_message in backend/app/services/conversation_service.py (FR-013)
- [ ] T023 [US2] Run User Story 2 tests to verify message addition works

**Checkpoint**: User Story 2 complete - messages can be added with role distinction and validation

---

## Phase 5: User Story 3 - Retrieve Ordered Message History (Priority: P1)

**Goal**: Enable retrieval of full conversation history in chronological order for AI context

**Independent Test**: Add multiple messages and verify retrieval returns them in created_at ascending order

### Tests for User Story 3

- [ ] T024 [P] [US3] Write test_get_conversation_history_ordered in backend/tests/test_conversation.py (SC-003)
- [ ] T025 [P] [US3] Write test_get_history_wrong_user_returns_empty in backend/tests/test_conversation.py (SC-002)
- [ ] T026 [P] [US3] Write test_get_history_10_messages in backend/tests/test_conversation.py (SC-004)

### Implementation for User Story 3

- [ ] T027 [US3] Implement get_conversation_history(conversation_id, user_id, db) in backend/app/services/conversation_service.py (FR-009)
- [ ] T028 [US3] Add ORDER BY created_at ASC to history query in backend/app/services/conversation_service.py
- [ ] T029 [US3] Add user_id filtering to history query in backend/app/services/conversation_service.py (FR-013)
- [ ] T030 [US3] Return list[dict] format for OpenAI compatibility in backend/app/services/conversation_service.py
- [ ] T031 [US3] Run User Story 3 tests to verify ordered retrieval

**Checkpoint**: User Story 3 complete - message history retrieval works with ordering and isolation
**Note**: Ordered history (created_at ASC) and clean dict format ensure the OpenAI agent receives accurate, chronological context for effective natural language understanding and processing.
---

## Phase 6: User Story 4 - Get or Create Conversation (Priority: P2)

**Goal**: Provide convenience helper that combines get and create operations for seamless chat UX

**Independent Test**: Call helper twice for same user and verify same conversation returned both times

### Tests for User Story 4

- [ ] T032 [P] [US4] Write test_get_or_create_conversation_creates_new in backend/tests/test_conversation.py
- [ ] T033 [P] [US4] Write test_get_or_create_conversation_returns_existing in backend/tests/test_conversation.py

### Implementation for User Story 4

- [ ] T034 [US4] Implement get_or_create_conversation(user_id, db) in backend/app/services/conversation_service.py (FR-010)
- [ ] T035 [US4] Add ORDER BY updated_at DESC to get most recent conversation in backend/app/services/conversation_service.py
- [ ] T036 [US4] Run User Story 4 tests to verify get_or_create behavior

**Checkpoint**: User Story 4 complete - conversations auto-created for seamless UX

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T037 [P] Update services __init__.py to export all helper functions in backend/app/services/__init__.py
- [ ] T038 [P] Run full test suite to verify all success criteria (SC-001 through SC-007)
- [ ] T039 [P] Verify database indexes exist using EXPLAIN on queries (SC-007)
- [ ] T040 [P] Create or update specs/database/schema.md with new models documentation
- [ ] T041 Run existing Phase II tests to verify no regressions (SC-005)
- [ ] T042 Run quickstart.md validation steps
- [ ] T043 [P] Run EXPLAIN ANALYZE on get_conversation_history query to verify index usage
---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - US1, US2, US3 are P1 priority - implement first
  - US4 is P2 priority - implement after P1 stories
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 (needs create_conversation and get_conversation)
- **User Story 3 (P1)**: Depends on US2 (needs messages to exist for history retrieval)
- **User Story 4 (P2)**: Can start after Foundational - Uses create_conversation from US1

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Helper functions in order: create → get → add → retrieve
- Story complete before moving to next priority

### Parallel Opportunities

**Foundational Phase (Phase 2):**
```
# These can run in parallel:
Task T003: "Create Conversation model"
Task T004: "Create Message model"
```

**User Story 1 Tests:**
```
# These can run in parallel:
Task T007: "Create test file skeleton"
Task T008: "Write test_create_conversation"
Task T009: "Write test_conversation_user_isolation"
```

**User Story 2 Tests:**
```
# These can run in parallel:
Task T014: "Write test_add_user_message"
Task T015: "Write test_add_assistant_message"
Task T016: "Write test_message_empty_content_rejected"
Task T017: "Write test_message_invalid_role_rejected"
```

**User Story 3 Tests:**
```
# These can run in parallel:
Task T024: "Write test_get_conversation_history_ordered"
Task T025: "Write test_get_history_wrong_user_returns_empty"
Task T026: "Write test_get_history_10_messages"
```

---

## Implementation Strategy

### MVP First (User Stories 1-3)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 - Conversation creation
4. Complete Phase 4: User Story 2 - Message addition
5. Complete Phase 5: User Story 3 - History retrieval
6. **STOP and VALIDATE**: Run all tests, verify SC-001 through SC-006
7. Ready for Phase III - Spec 2 (MCP Tools)

### Full Delivery

1. MVP (above)
2. Add User Story 4 - Get-or-create convenience helper
3. Complete Polish phase
4. All success criteria verified

---

## Summary

| Phase | Story | Tasks | Parallel Opportunities |
| ----- | ----- | ----- | ---------------------- |
| Setup | - | 2 | 0 |
| Foundational | - | 4 | 2 (models) |
| US1 | P1 | 7 | 3 (tests) |
| US2 | P1 | 10 | 4 (tests) |
| US3 | P1 | 8 | 3 (tests) |
| US4 | P2 | 5 | 2 (tests) |
| Polish | - | 6 | 4 |
| **Total** | - | **42** | **18** |

**MVP Scope**: Phases 1-5 (Setup + Foundational + US1 + US2 + US3) = 31 tasks
**Full Scope**: All phases = 42 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Spec references (FR-xxx, SC-xxx) included for traceability
