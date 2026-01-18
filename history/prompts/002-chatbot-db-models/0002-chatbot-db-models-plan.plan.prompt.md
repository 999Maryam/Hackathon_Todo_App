---
id: "0002"
title: "Chatbot DB Models Implementation Plan"
stage: plan
date: 2026-01-14
surface: agent
model: claude-opus-4-5-20251101
feature: 001-chatbot-db-models
branch: 001-chatbot-db-models
user: developer
command: /sp.plan
labels: ["database", "models", "phase-iii", "sqlmodel", "persistence", "conversation", "message"]
links:
  spec: specs/001-chatbot-db-models/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-chatbot-db-models/plan.md
  - specs/001-chatbot-db-models/research.md
  - specs/001-chatbot-db-models/data-model.md
  - specs/001-chatbot-db-models/quickstart.md
  - specs/001-chatbot-db-models/contracts/conversation-service.md
tests:
  - N/A (plan phase - tests defined for implementation)
---

## Prompt

Database Models & Persistence for Todo AI Chatbot (Phase III – Spec 1)

Create:
- Updated database schema diagram showing relationships:
  User 1→* Conversation 1→* Message
  User 1→* Task (existing)
- SQLModel class definitions: Conversation, Message (extend Task if needed)
- CRUD helper functions (conversation & message level)
- Pytest test file skeleton for models + helpers
- Index & constraint documentation note

Decisions:
- Timestamps → server_default=func.now() (consistent & timezone-safe)
- Message.content → Text (not limited length → better for long AI responses)
- Role field → Literal["user", "assistant"] (strict validation)
- Ordering → always sort messages by created_at ASC (critical for natural language context)
- Indexes → composite on message (conversation_id, created_at) + user_id on both tables
- Helper return type → full objects/lists (easier for agent to consume)
- New conversation auto-creation → yes, when no conversation_id provided

Testing strategy (focused on natural-language readiness):
- Model tests:
  - Conversation: user_id required, timestamps auto-set
  - Message: role validation, content not null/empty
- Integration tests:
  - Create conversation → add 10 alternating user/assistant messages → retrieve ordered list (assert len==10, correct sequence)
  - Wrong user_id → returns empty or raises error
  - Empty conversation → returns []
  - Multiple conversations per user → isolation verified
- Manual check: run queries in DB client → verify order & ownership

Technical details & order:
1. Define models → Conversation + Message (with relationships & indexes)
2. Add helper functions:
   - create_or_get_conversation(user_id) → returns conversation_id
   - add_message(conversation_id, user_id, role, content)
   - get_ordered_messages(conversation_id, user_id) → list[dict] for agent
3. Add ownership checks in every helper (WHERE user_id = ?)
4. Write & run pytest suite (fixtures for user/conversation)
5. Sync schema (SQLModel metadata or Alembic autogenerate)
6. Update /specs/database/schema.md with new models & relationships

Why this matters for natural language:
- Ordered message history → agent sees full context in correct sequence
- Fast retrieval (indexes) → low latency for every chat request
- Strict user isolation → no hallucination from other users' data
- Clean helpers → agent receives perfect input format every time

## Response snapshot

Created comprehensive implementation plan for Phase III - Spec 1: Database Models & Persistence Layer.

**Artifacts Generated:**
- `plan.md` - Full implementation plan with phases, decisions, risks
- `research.md` - 7 research questions resolved (timestamps, content type, role validation, ordering, indexes, return types, auto-create)
- `data-model.md` - Entity definitions with ERD, SQLModel class code, indexes
- `contracts/conversation-service.md` - Service interface with 6 helper functions
- `quickstart.md` - Step-by-step implementation guide

**Key Technical Decisions:**
1. `server_default=func.now()` for timezone-safe timestamps
2. `Text` type for unlimited message content
3. `Literal["user", "assistant"]` + CHECK constraint for role validation
4. Composite index on (conversation_id, created_at) for fast ordering
5. Return dicts for history (OpenAI format), objects for mutations

**Constitution Check:** All 6 relevant principles passed (SDD, Progressive Evolution, Security First, Stateless Design, AI-Native Focus, Maintainability).

**Agent Context Updated:** CLAUDE.md now includes Python 3.13+, SQLModel, SQLAlchemy for this feature.

## Outcome

- ✅ Impact: Complete implementation plan ready for task generation
- 🧪 Tests: Test cases defined in contracts and quickstart (to be implemented)
- 📁 Files: 5 artifacts created in specs/001-chatbot-db-models/
- 🔁 Next prompts: /sp.tasks to generate task breakdown, then /sp.implement
- 🧠 Reflection: User input was detailed - all decisions pre-made, plan documents them

## Evaluation notes (flywheel)

- Failure modes observed: None - user provided comprehensive technical decisions
- Graders run and results (PASS/FAIL): Constitution check PASS (all 6 principles)
- Prompt variant (if applicable): Standard /sp.plan flow with detailed user input
- Next experiment (smallest change to try): N/A - plan complete
