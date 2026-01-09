# Phase II - Todo Full-Stack Web Application Constitution

<!-- Sync Impact Report: Version 1.0.0 (initial) | Created: 2026-01-08 -->

## Core Principles

### I. Spec-Driven Development (SDD)
Every feature MUST be driven by a written specification before any code is written. The workflow is mandatory: Spec → Plan → Tasks → Implement. No exceptions. Specifications MUST include clear acceptance criteria, user stories, and success conditions. This ensures alignment with requirements and enables independent verification of completion.

### II. Strict Separation of Concerns
The application MUST maintain clear boundaries between frontend, backend, and authentication layers. Each layer uses its designated technology stack without mixing concerns. Frontend (Next.js) handles UI and state; Backend (FastAPI) handles business logic and data access; Authentication (Better Auth + JWT) handles user identity and tokens. No direct database access from frontend. No UI logic in backend.

### III. Security by Design - Stateless JWT Authentication
Authentication MUST be fully stateless using JWT tokens issued by Better Auth. Sessions MUST NOT be stored in the database. Every API request MUST include a valid JWT token in the `Authorization: Bearer <token>` header. FastAPI middleware MUST verify all tokens using the shared `BETTER_AUTH_SECRET` environment variable. All routes MUST extract the authenticated user_id and enforce strict ownership validation (users can only access their own tasks). Token expiry MUST be configured (recommended: 7 days default).

### IV. Multi-User Data Isolation
Every task in the database MUST be associated with a `user_id` foreign key. Query-level filtering MUST enforce that no user can access, modify, or delete another user's tasks. This isolation MUST be implemented at the database query level, never relying on frontend-only validation. Unauthorized API requests MUST receive 401 Unauthorized responses with clear error messages.

### V. Reliable Persistent Storage
All data MUST be persisted in Neon Serverless PostgreSQL using SQLModel ORM. Data MUST survive application restarts and concurrent user access. Database schema MUST enforce foreign key constraints and proper indexing. Migrations MUST be version-controlled and reproducible. No in-memory-only data storage in production.

### VI. Modern, Responsive, and Maintainable Codebase
Frontend UI MUST be responsive and work seamlessly on desktop, tablet, and mobile devices. All code MUST follow language-specific standards: Python (PEP 8, type hints everywhere, Pydantic validation), Next.js (TypeScript, ESLint + Prettier). Code MUST be self-documenting with comprehensive inline comments. FastAPI Swagger documentation MUST be complete and accurate. No legacy patterns or technical debt shortcuts allowed.

## Technology Stack (Non-Negotiable)

- **Frontend**: Next.js 16+ with App Router (TypeScript, ESLint, Prettier)
- **Backend**: Python FastAPI (PEP 8, type hints, Pydantic validation)
- **ORM**: SQLModel (strongly typed database models)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (with JWT plugin enabled)
- **Environment Configuration**: `.env` file with shared `BETTER_AUTH_SECRET`

## API Design & Endpoints

The backend MUST expose exactly 6 RESTful endpoints (no more, no less):

```
GET    /api/{user_id}/tasks           # List all tasks for authenticated user
POST   /api/{user_id}/tasks           # Create a new task for authenticated user
GET    /api/{user_id}/tasks/{id}      # Get a single task (verify ownership)
PUT    /api/{user_id}/tasks/{id}      # Update a task (verify ownership)
DELETE /api/{user_id}/tasks/{id}      # Delete a task (verify ownership)
PATCH  /api/{user_id}/tasks/{id}/complete  # Toggle task completion status
```

All endpoints MUST:
- Require valid JWT token in `Authorization: Bearer <token>` header
- Return `401 Unauthorized` for missing or invalid tokens
- Return `403 Forbidden` if user attempts to access another user's task
- Return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- Support standard HTTP methods strictly (GET for retrieval, POST for creation, PUT for full updates, PATCH for partial updates, DELETE for removal)
- Include comprehensive Swagger documentation

## Code Quality Standards

### Python Backend
- All functions and classes MUST include type hints
- Pydantic models MUST validate all inputs
- PEP 8 compliance is mandatory
- Comprehensive inline comments explaining non-obvious logic
- FastAPI Swagger UI MUST be complete and accurate
- Error handling MUST return structured JSON responses with clear error messages

### Next.js Frontend
- TypeScript MUST be used throughout (no plain JavaScript)
- ESLint + Prettier MUST enforce code style
- Components MUST be modular and reusable
- Responsive design MUST work on all viewport sizes (mobile, tablet, desktop)
- Clear user feedback for loading states, errors, and success messages
- HTTP-only cookies or secure localStorage for token storage

## Testing Requirements

### Backend Testing
- Unit tests MUST cover all business logic using pytest
- Integration tests MUST verify API contracts and end-to-end flows
- All tests MUST pass before code is merged
- Test coverage MUST be measurable and tracked

### Frontend Testing
- Component tests for critical user flows (auth, task creation, task listing)
- Basic snapshot tests for UI consistency
- End-to-end manual verification of signup → signin → CRUD operations

### End-to-End Testing
- Manual verification that multiple simultaneous users cannot see or modify each other's tasks
- Verification that expired or invalid tokens are properly rejected
- Verification that data persists across application restarts
- Verification that Swagger UI documents all endpoints correctly

## Security Constraints (Non-Negotiable)

- No session storage in database - JWT only
- `BETTER_AUTH_SECRET` MUST be stored in `.env` and never committed
- All API endpoints MUST require valid JWT
- Task ownership MUST be enforced at query level
- Unauthorized requests MUST receive 401 responses
- No sensitive data (passwords, tokens) in logs or error responses
- HTTPS MUST be used in production (though development can use HTTP)
- SQL injection protection via SQLModel ORM
- XSS protection via Next.js built-in escaping
- CSRF protection via SameSite cookies

## Success Criteria (Must-Have)

✓ Complete end-to-end flow: User can signup → signin → receive JWT
✓ Authenticated user can perform all CRUD + complete operations on their own tasks only
✓ Second user cannot see or modify first user's tasks
✓ Data persists correctly in Neon PostgreSQL and survives app restarts
✓ Unauthorized API requests receive proper 401 response
✓ Expired/invalid tokens are rejected with 401 response
✓ Frontend is responsive and provides clear feedback (loading, errors, success)
✓ Swagger UI documents all 6 endpoints correctly
✓ No security vulnerabilities in authentication or data access
✓ Project passes full integration testing with multiple simultaneous users
✓ All 5 basic todo features fully functional: create, list, view, update, delete, toggle complete
✓ Clean, readable, well-structured codebase ready for future extensions

## Governance

**Constitution Authority**: This constitution supersedes all other practices and guidelines. All PRs and design decisions MUST verify compliance with these principles before proceeding.

**Amendment Procedure**: Significant changes to principles or technology stack MUST be approved by the project architect before implementation. Minor clarifications may be updated without formal approval but MUST be documented in the amendment log.

**Version Semantics**:
- MAJOR: Backward-incompatible principle removals or technology stack changes
- MINOR: New principles added or significant guidance expansion
- PATCH: Clarifications, wording improvements, non-semantic refinements

**Compliance Review**: All pull requests MUST reference which constitutional principles they uphold. Code reviews MUST verify adherence to these core principles before merge approval.

**Runtime Guidance**: See `CLAUDE.md` for day-to-day development guidance and agent invocation rules. See `.specify/memory/constitution.md` (this file) for immutable project principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
