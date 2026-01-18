# Implementation Plan: Database Models & Persistence Layer

**Branch**: `001-chatbot-db-models` | **Date**: 2026-01-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-chatbot-db-models/spec.md`
**Phase**: III - Spec 1 of 4

---

## Summary

Implement the database models and persistence layer for the Todo AI Chatbot. This includes:
- Two new SQLModel entities: `Conversation` and `Message`
- CRUD helper functions for conversation and message management
- Strict multi-user isolation via user_id filtering
- Ordered message retrieval for AI context window

Technical approach: Extend existing Phase II database setup with new models, use server-side timestamp defaults, composite indexes for performance, and service layer pattern for helper functions.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, SQLAlchemy, Pydantic v2
**Storage**: Neon Serverless PostgreSQL (existing Phase II connection)
**Testing**: pytest
**Target Platform**: Linux server (Docker container in Phase IV)
**Project Type**: Web application (backend focus for this spec)
**Performance Goals**: Fast ordered message retrieval (<50ms for 100 messages)
**Constraints**: Reuse existing DATABASE_URL, no modifications to Task model
**Scale/Scope**: Multi-user, ~1000 messages per conversation max

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Verification

| Principle | Status | Evidence |
| --------- | ------ | -------- |
| I. Spec-Driven Development | ✅ PASS | Full spec created via `/sp.specify` |
| II. Progressive Evolution | ✅ PASS | Builds on Phase II DB + auth |
| IV. Security First | ✅ PASS | user_id FK on all tables, query filtering |
| V. Stateless & Resilient | ✅ PASS | All state in PostgreSQL, no in-memory |
| VII. AI-Native Focus | ✅ PASS | Conversation persistence for AI context |
| VIII. Maintainability | ✅ PASS | Task ID + spec references in code comments |

### Post-Design Verification

| Principle | Status | Evidence |
| --------- | ------ | -------- |
| I. Spec-Driven Development | ✅ PASS | Plan derived from spec requirements |
| II. Progressive Evolution | ✅ PASS | Uses existing database.py, models pattern |
| IV. Security First | ✅ PASS | All queries filter by user_id |
| V. Stateless & Resilient | ✅ PASS | Server-side timestamps, FK constraints |
| VII. AI-Native Focus | ✅ PASS | OpenAI-format message retrieval |
| VIII. Maintainability | ✅ PASS | Service layer abstraction, full test coverage |

**Gate Status**: ✅ ALL PASSED - Proceed to implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/001-chatbot-db-models/
├── spec.md                       # Feature specification
├── plan.md                       # This file
├── research.md                   # Phase 0: Research decisions
├── data-model.md                 # Phase 1: Entity definitions
├── quickstart.md                 # Phase 1: Implementation guide
├── contracts/
│   └── conversation-service.md   # Phase 1: Service interface contract
├── checklists/
│   └── requirements.md           # Quality checklist
└── tasks.md                      # Phase 2: Task breakdown (via /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py          # Export new models
│   │   ├── user.py              # Existing (DO NOT MODIFY)
│   │   ├── task.py              # Existing (DO NOT MODIFY)
│   │   ├── conversation.py      # NEW: Conversation model
│   │   └── message.py           # NEW: Message model
│   ├── services/
│   │   └── conversation_service.py  # NEW: CRUD helpers
│   └── database.py              # Existing (reuse)
└── tests/
    └── test_conversation.py     # NEW: Integration tests
```

**Structure Decision**: Web application structure selected. Backend-only changes for this spec - extends existing `backend/app/` layout with new models and services directories.

---

## Implementation Phases

### Phase 1: Models (Priority: P1)

1. Create `backend/app/models/conversation.py`
   - Conversation SQLModel with id, user_id, created_at, updated_at
   - Index on user_id
   - Relationship to Message

2. Create `backend/app/models/message.py`
   - Message SQLModel with id, conversation_id, user_id, role, content, created_at
   - Composite index on (conversation_id, created_at)
   - Index on user_id
   - CHECK constraint on role

3. Update `backend/app/models/__init__.py`
   - Export Conversation and Message

### Phase 2: Service Layer (Priority: P1)

4. Create `backend/app/services/` directory (if needed)

5. Create `backend/app/services/conversation_service.py`
   - create_conversation(user_id, db)
   - get_conversation(conversation_id, user_id, db)
   - get_or_create_conversation(user_id, db)
   - add_user_message(conversation_id, user_id, content, db)
   - add_assistant_message(conversation_id, user_id, content, db)
   - get_conversation_history(conversation_id, user_id, db)

### Phase 3: Database Sync (Priority: P1)

6. Sync schema
   - Run `create_db_and_tables()` or create Alembic migration
   - Verify tables and indexes created

### Phase 4: Testing (Priority: P1)

7. Create `backend/tests/test_conversation.py`
   - Test conversation creation
   - Test message addition (user and assistant roles)
   - Test ordered history retrieval
   - Test user isolation (cross-user access prevention)
   - Test validation (empty content, invalid role)

### Phase 5: Documentation (Priority: P2)

8. Update `specs/database/schema.md`
   - Add Conversation and Message entity documentation
   - Document indexes and constraints

---

## Technical Decisions

| Decision | Choice | Rationale |
| -------- | ------ | --------- |
| Timestamps | `server_default=func.now()` | Database-level consistency, timezone-safe |
| Message content | `Text` type | Unlimited length for long AI responses |
| Role validation | `Literal` + CHECK | Type safety + database integrity |
| Ordering | `created_at ASC` | Chronological for AI context |
| Indexes | Composite on (conv_id, created_at) | Fast ordered retrieval |
| Helper returns | Objects for mutations, dicts for history | ORM benefits + OpenAI format |
| Auto-create | Yes for get_or_create | Seamless chat UX |

---

## Risk Analysis

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Schema sync breaks existing tables | High | Use `create_all()` which is additive, test with existing data |
| Performance with many messages | Medium | Composite index, future pagination if needed |
| Circular imports between models | Low | Use TYPE_CHECKING pattern, string references |

---

## Complexity Tracking

> No constitution violations requiring justification.

All design choices align with constitution principles. No complexity exceptions needed.

---

## Artifacts Generated

| Artifact | Path | Status |
| -------- | ---- | ------ |
| Research | `specs/001-chatbot-db-models/research.md` | ✅ Complete |
| Data Model | `specs/001-chatbot-db-models/data-model.md` | ✅ Complete |
| Service Contract | `specs/001-chatbot-db-models/contracts/conversation-service.md` | ✅ Complete |
| Quickstart | `specs/001-chatbot-db-models/quickstart.md` | ✅ Complete |

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Execute implementation via `/sp.implement`
3. Run tests to verify all success criteria
4. Continue to Phase III - Spec 2 (MCP Tools)
