---
id: 0001
title: Constitution for Phase II Todo Web App
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Maryam
command: /sp.constitution
labels: ["spec-driven-development", "authentication", "security", "api-design", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - null
---

## Prompt

Project: Phase II - Todo Full-Stack Web Application (Hackathon)
Core principles:
- Spec-driven development using Claude Code + Spec-Kit Plus
- Strict separation of concerns between frontend, backend, and authentication
- Security by design with stateless JWT-based authentication
- Full multi-user support with complete data isolation per user
- Reliability through persistent storage and proper error handling
- Modern, responsive, and maintainable codebase

Key standards:
- Technology stack must be followed exactly:
  - Frontend: Next.js 16+ with App Router
  - Backend: Python FastAPI
  - ORM: SQLModel
  - Database: Neon Serverless PostgreSQL
  - Authentication: Better Auth (with JWT plugin enabled)
- API design: Strictly RESTful with proper HTTP methods and status codes
- API endpoints: Exactly the following 6 endpoints (no more, no less):
  - GET    /api/{user_id}/tasks
  - POST   /api/{user_id}/tasks
  - GET    /api/{user_id}/tasks/{id}
  - PUT    /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
  - PATCH  /api/{user_id}/tasks/{id}/complete
- Authentication flow:
  - Better Auth issues JWT tokens on signup/signin
  - Frontend attaches JWT in Authorization: Bearer <token> header for every API call
  - FastAPI middleware verifies JWT using shared BETTER_AUTH_SECRET
  - All routes extract authenticated user_id and enforce ownership (filter/modify only user's own tasks)
- Code quality:
  - Python: PEP 8, type hints everywhere, Pydantic/SQLModel for validation
  - Next.js: TypeScript, ESLint + Prettier
  - Comprehensive inline comments and API documentation (FastAPI Swagger)
- Testing:
  - Backend: Unit + integration tests with pytest
  - Frontend: Basic component/tests for critical flows
  - End-to-end: Manual verification of full user flows

Constraints:
- No session storage in database for authentication – must be fully stateless (JWT only)
- Shared secret via environment variable BETTER_AUTH_SECRET in both frontend and backend
- All API endpoints require valid JWT → return 401 Unauthorized if missing/invalid
- Task ownership strictly enforced at database/query level (no user can access another's tasks)
- Database schema must associate every task with a user_id foreign key
- Token expiry must be configured (recommended: 7 days default)
- Responsive UI that works on desktop and mobile
- All 5 basic todo features (create, list, view, update, delete, toggle complete) must be fully functional in the web app

Success criteria:
- Complete end-to-end flow works flawlessly:
  - User can signup → signin → receive JWT
  - Authenticated user can perform all CRUD + complete operations on their own tasks only
  - Second user cannot see or modify first user's tasks
- Data persists correctly in Neon PostgreSQL and survives app restarts
- Unauthorized API requests receive proper 401 response
- Expired/invalid tokens are rejected
- Frontend is responsive and provides clear feedback (loading, errors, success)
- Swagger UI documents all endpoints correctly
- No security vulnerabilities in authentication or data access
- Project passes full integration testing with multiple simultaneous users
- Clean, readable, and well-structured codebase ready for future extensions

## Response snapshot

Created comprehensive constitution for Phase II Todo Full-Stack Web Application with 6 core principles covering spec-driven development, separation of concerns, stateless JWT security, multi-user data isolation, persistent storage, and modern codebase standards. Documented immutable technology stack, exact 6-endpoint API contract, code quality standards, testing requirements, security constraints, and success criteria. Established governance procedures with semantic versioning and compliance review requirements. Constitution serves as the authoritative source for all architectural and implementation decisions throughout the project.

## Outcome

- ✅ Impact: Constitution establishes clear, non-negotiable governance for Phase II. All future features, tasks, and architectural decisions will be evaluated against these 6 principles and explicit constraints. Enables independent verification of completion and alignment with requirements.
- 🧪 Tests: No automated tests for constitution; compliance verification via PR review and design document alignment checks
- 📁 Files: .specify/memory/constitution.md (primary); CLAUDE.md (technology stack table and agent mapping updated)
- 🔁 Next prompts: `/sp.specify` for Phase II feature specification; `/sp.plan` for high-level architecture design; `/sp.tasks` for sprint planning
- 🧠 Reflection: Constitution successfully captures all project requirements into immutable principles. Clear separation between governance (this file) and runtime guidance (CLAUDE.md). Ready to proceed with spec phase.

## Evaluation notes (flywheel)

- Failure modes observed: None; constitution covers all stated requirements and constraints
- Graders run and results (PASS/FAIL): PASS - All placeholders filled, no bracket tokens remaining, dates ISO formatted, principles are declarative and testable
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Proceed with /sp.specify to create feature specification based on these constitutional principles
