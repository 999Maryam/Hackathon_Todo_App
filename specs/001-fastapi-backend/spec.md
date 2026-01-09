# Feature Specification: Backend API for Todo Full-Stack Web Application

**Feature Branch**: `001-fastapi-backend`
**Created**: 2026-01-08
**Status**: Draft
**Input**: Implement secure RESTful FastAPI backend with persistent storage in Neon PostgreSQL, JWT authentication middleware, and enforced multi-user data isolation

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Authenticated User Creates a Task (Priority: P1)

As an authenticated user with a valid JWT token, I want to create a new task by sending POST request to the API so that I can add items to my task list.

**Why this priority**: Creating tasks is the core value proposition of a todo app. Without task creation, the app has no functionality. This is MVP-critical.

**Independent Test**: Can be fully tested by logging in with a valid JWT, sending a POST request to `/api/{user_id}/tasks` with task data, and verifying the task is stored in the database with the correct user_id and appears in subsequent GET requests.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT token, **When** they POST a new task with title and description to `/api/{user_id}/tasks`, **Then** the API returns 201 Created with the task object including id, user_id, title, description, completed status (false), and timestamps.

2. **Given** a user sends a request without a JWT token, **When** they attempt to POST to `/api/{user_id}/tasks`, **Then** the API returns 401 Unauthorized with error message "Missing or invalid authentication token".

3. **Given** a user sends an expired JWT token, **When** they attempt to POST to `/api/{user_id}/tasks`, **Then** the API returns 401 Unauthorized with error message "Token expired or invalid".

---

### User Story 2 - Authenticated User Retrieves Their Tasks (Priority: P1)

As an authenticated user, I want to retrieve all my tasks via GET request so that I can see my complete task list.

**Why this priority**: Viewing tasks is essential functionality. Users must see what they've created. This enables the core workflow loop.

**Independent Test**: Can be fully tested by creating several tasks as one user, then retrieving them via GET `/api/{user_id}/tasks` and verifying only that user's tasks are returned, with correct data structure and timestamps.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and has created 3 tasks, **When** they GET `/api/{user_id}/tasks`, **Then** the API returns 200 OK with a list of exactly 3 task objects with all required fields.

2. **Given** a user is authenticated but has no tasks, **When** they GET `/api/{user_id}/tasks`, **Then** the API returns 200 OK with an empty list `[]`.

3. **Given** user A attempts to GET `/api/user_B_id/tasks` (accessing another user's tasks), **When** the request includes user A's valid JWT, **Then** the API returns 403 Forbidden with error message "You do not have permission to access these tasks".

---

### User Story 3 - Authenticated User Retrieves a Single Task (Priority: P1)

As an authenticated user, I want to retrieve a specific task by ID so that I can view its full details.

**Why this priority**: Viewing individual task details is necessary for many workflows (edit, view, reference). Core MVP functionality.

**Independent Test**: Can be fully tested by creating a task, retrieving it by ID via GET `/api/{user_id}/tasks/{id}`, and verifying all task data is returned correctly.

**Acceptance Scenarios**:

1. **Given** a user has created a task with ID 42, **When** they GET `/api/{user_id}/tasks/42`, **Then** the API returns 200 OK with the complete task object.

2. **Given** a user attempts to GET a non-existent task ID, **When** they request `/api/{user_id}/tasks/999`, **Then** the API returns 404 Not Found with error message "Task not found".

3. **Given** user A tries to retrieve a task owned by user B, **When** user A GETs `/api/{user_A_id}/tasks/{task_B_id}`, **Then** the API returns 404 Not Found (task appears non-existent from user A's perspective due to ownership filtering).

---

### User Story 4 - Authenticated User Updates a Task (Priority: P1)

As an authenticated user, I want to update an existing task's title and description via PUT request so that I can modify task details.

**Why this priority**: Task editing is essential for productivity. Users need to refine task details after creation. Core MVP functionality.

**Independent Test**: Can be fully tested by creating a task, updating its title and description via PUT `/api/{user_id}/tasks/{id}`, and verifying the changes persist in subsequent GET requests.

**Acceptance Scenarios**:

1. **Given** a user owns a task, **When** they PUT updated title and description to `/api/{user_id}/tasks/{id}`, **Then** the API returns 200 OK with the updated task object reflecting the changes.

2. **Given** a user attempts to update a non-existent task, **When** they PUT to `/api/{user_id}/tasks/999`, **Then** the API returns 404 Not Found.

3. **Given** user A attempts to update a task owned by user B, **When** user A PUTs to `/api/{user_B_id}/tasks/{task_B_id}`, **Then** the API returns 403 Forbidden with error message "You do not have permission to modify this task".

---

### User Story 5 - Authenticated User Toggles Task Completion (Priority: P1)

As an authenticated user, I want to toggle a task's completion status via PATCH request so that I can mark tasks as done or incomplete.

**Why this priority**: Task completion tracking is the primary value of a todo app. This workflow (create → update → complete) is critical for MVP.

**Independent Test**: Can be fully tested by creating a task (completed=false), PATCH it to mark complete (completed=true), and verify the status persists in the database and subsequent GET requests.

**Acceptance Scenarios**:

1. **Given** a user has a task with completed=false, **When** they PATCH `/api/{user_id}/tasks/{id}/complete`, **Then** the API returns 200 OK with the task object showing completed=true and updated_at timestamp.

2. **Given** a user has a task with completed=true, **When** they PATCH `/api/{user_id}/tasks/{id}/complete`, **Then** the API returns 200 OK with the task object showing completed=false (toggle behavior).

3. **Given** user A attempts to complete a task owned by user B, **When** user A PATCHes `/api/{user_B_id}/tasks/{task_B_id}/complete`, **Then** the API returns 403 Forbidden.

---

### User Story 6 - Authenticated User Deletes a Task (Priority: P1)

As an authenticated user, I want to delete a task via DELETE request so that I can remove unwanted tasks from my list.

**Why this priority**: Deletion is fundamental for task management. Users need to clean up completed or erroneous tasks. Core MVP functionality.

**Independent Test**: Can be fully tested by creating a task, deleting it via DELETE `/api/{user_id}/tasks/{id}`, verifying it no longer appears in GET requests, and attempting to retrieve it returns 404.

**Acceptance Scenarios**:

1. **Given** a user owns a task, **When** they DELETE `/api/{user_id}/tasks/{id}`, **Then** the API returns 204 No Content, and subsequent GET `/api/{user_id}/tasks` does not include the deleted task.

2. **Given** a user attempts to delete a non-existent task, **When** they DELETE `/api/{user_id}/tasks/999`, **Then** the API returns 404 Not Found.

3. **Given** user A attempts to delete a task owned by user B, **When** user A DELETEs `/api/{user_B_id}/tasks/{task_B_id}`, **Then** the API returns 403 Forbidden, and the task remains in the database.

---

### Edge Cases

- What happens when a user sends a request with a tampered JWT token (invalid signature)?
- What happens when two users simultaneously update the same task (handled by ownership filtering)?
- What happens when a user sends requests with SQL injection attempts in task titles (must be sanitized by Pydantic/SQLModel)?
- What happens when the database connection fails midway through a request?
- What happens when a user submits extremely large task descriptions (should validate max length)?
- What happens when a user sends requests with malformed JSON (should return 400 Bad Request)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose exactly 6 RESTful API endpoints with correct HTTP methods (GET, POST, PUT, DELETE, PATCH) as specified in the constitution.

- **FR-002**: System MUST verify JWT token on every authenticated request. Invalid or missing tokens MUST return 401 Unauthorized. Expired tokens MUST return 401 Unauthorized.

- **FR-003**: System MUST extract authenticated user_id from JWT token and use it to filter all task queries and modifications. No user can access another user's tasks via database-level filtering.

- **FR-004**: System MUST store tasks in Neon PostgreSQL with schema: id (UUID, primary key), user_id (UUID, foreign key to users table), title (string, required, max 255 chars), description (string, optional, max 2000 chars), completed (boolean, default false), created_at (timestamp, auto-set), updated_at (timestamp, auto-update).

- **FR-005**: System MUST return proper HTTP status codes: 200 OK (GET success), 201 Created (POST success), 204 No Content (DELETE success), 400 Bad Request (malformed input), 401 Unauthorized (missing/invalid token), 403 Forbidden (ownership violation), 404 Not Found (task doesn't exist or belongs to another user), 500 Internal Server Error (unexpected errors).

- **FR-006**: System MUST validate all request payloads using Pydantic models. Invalid data MUST return 400 Bad Request with descriptive error messages.

- **FR-007**: System MUST include comprehensive FastAPI Swagger UI documentation for all 6 endpoints, automatically generated from code.

- **FR-008**: System MUST implement JWT verification middleware that extracts and validates the token from the `Authorization: Bearer <token>` header.

- **FR-009**: System MUST use SQLModel for ORM with full type hints on all models and database operations.

- **FR-010**: System MUST follow PEP 8 code style with comprehensive inline comments explaining non-obvious logic.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item. Attributes: id (UUID), user_id (UUID, foreign key), title (string), description (string), completed (boolean), created_at (ISO timestamp), updated_at (ISO timestamp). Each task belongs to exactly one user.

- **User Reference**: JWT tokens contain user_id claim. No user table creation required; system trusts user_id from Better Auth tokens.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 API endpoints are implemented and tested. Each endpoint handles the happy path and all error scenarios (401, 403, 404, 400) correctly.

- **SC-002**: JWT authentication middleware correctly verifies tokens on every protected request. Requests with missing, invalid, or expired tokens return 401 Unauthorized.

- **SC-003**: Multi-user data isolation is enforced at query level. User A cannot see, retrieve, update, or delete User B's tasks. Attempts return 403 or 404 as appropriate.

- **SC-004**: Tasks are persisted in Neon PostgreSQL with all required fields. Data survives application restart and concurrent access.

- **SC-005**: API returns correct HTTP status codes for all scenarios (200, 201, 204, 400, 401, 403, 404, 500) with clear JSON error messages.

- **SC-006**: FastAPI Swagger UI documents all 6 endpoints with request/response schemas, parameter descriptions, and example values.

- **SC-007**: Backend achieves 90%+ test coverage with unit tests (models, validation) and integration tests (endpoints, auth, database operations).

- **SC-008**: API response time is <500ms for all requests under normal load (measured locally).

- **SC-009**: Code follows PEP 8 standards, includes type hints on all functions/classes, and has inline comments explaining complex logic.

## Assumptions

- **JWT Token Structure**: Better Auth issues JWT tokens with a `user_id` claim. This claim is the source of truth for user identification.

- **Shared Secret**: The `BETTER_AUTH_SECRET` environment variable is shared between frontend and backend for JWT verification. Backend can verify tokens without querying a database.

- **User Management**: No user creation/deletion endpoints are required. Users are managed by Better Auth (frontend handles signup/signin). Backend only trusts JWT tokens.

- **Database Readiness**: Neon PostgreSQL connection is available via `DATABASE_URL` environment variable. Migrations are applied before app startup.

- **Token Expiry**: Better Auth is configured to issue tokens with a 7-day expiration (or as configured). Backend trusts token expiry without additional validation.

## Out of Scope

- User authentication endpoints (signup, signin, logout) - handled by Better Auth on frontend
- Session management or database-stored sessions - fully stateless via JWT
- Advanced features: pagination, filtering, sorting, search, real-time updates, file uploads
- Frontend code, UI components, or web pages
- Custom authentication library development

## Dependencies & Assumptions

- Depends on Better Auth being configured with JWT plugin and issuing valid tokens
- Assumes Neon PostgreSQL is available and reachable via `DATABASE_URL`
- Assumes `BETTER_AUTH_SECRET` is configured in environment
- No external dependencies on frontend code or UI libraries

## Next Steps

1. **Plan Phase**: Design detailed architecture (project structure, database migrations, middleware layers)
2. **Tasks Phase**: Break into specific implementation tasks (models, routes, tests)
3. **Implementation**: Execute via `fastapi-backend-dev` agent
4. **Testing**: Run comprehensive unit and integration tests
5. **Integration**: Verify with frontend (full end-to-end flow)
