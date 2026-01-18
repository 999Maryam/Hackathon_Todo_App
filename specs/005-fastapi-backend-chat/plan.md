# Implementation Plan: Backend API for Todo Full-Stack Web Application

**Branch**: `001-fastapi-backend` | **Date**: 2026-01-08 | **Spec**: [specs/001-fastapi-backend/spec.md](spec.md)

**Input**: Feature specification from `/specs/001-fastapi-backend/spec.md`

## Summary

Implement a secure, stateless RESTful FastAPI backend API with 6 endpoints for multi-user task management. The backend will enforce user data isolation through JWT authentication and query-level filtering, persist all data to Neon Serverless PostgreSQL using SQLModel ORM, and provide comprehensive Swagger documentation. Implementation follows a phased approach: Foundation (database models, environment setup) → Authentication (JWT middleware, dependency injection) → Core API (CRUD endpoints with ownership enforcement) → Error Handling (global exception handlers) → Testing (full pytest suite with success criteria coverage).

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**:
- FastAPI (async web framework)
- SQLModel (ORM combining SQLAlchemy + Pydantic)
- PyJWT (JWT token verification)
- Pydantic (data validation)
- SQLAlchemy (database abstraction)
- psycopg2 (PostgreSQL driver, sync)
- pytest (testing framework)
- python-dotenv (environment variable management)

**Storage**: Neon Serverless PostgreSQL (cloud-hosted, automatic scaling, serverless billing)

**Testing**: pytest (unit + integration tests), manual verification via Swagger UI

**Target Platform**: Linux server (development) / cloud deployment (production via Vercel/AWS/GCP)

**Project Type**: Web backend (single FastAPI application, no frontend code)

**Performance Goals**:
- API response time: <500ms p95 for all requests (development benchmark)
- Concurrent users: Support basic local testing (10+ simultaneous)
- Database queries: <100ms for simple task operations

**Constraints**:
- Stateless JWT-only authentication (no session database)
- Shared BETTER_AUTH_SECRET environment variable for token verification
- All responses must be JSON format
- PEP 8 compliance mandatory
- No external authentication service calls in backend

**Scale/Scope**:
- 1-5 concurrent users (hackathon scope)
- 6 RESTful endpoints
- Single Task entity with user_id isolation
- ~500-1000 lines of code for backend + tests

## Constitution Check

**Mandatory Principles Verification:**

| Principle | Requirement | Status |
|-----------|-----------|--------|
| Spec-Driven Development | Workflow: Spec → Plan → Tasks → Implement | ✅ PASS - Following SDD workflow exactly |
| Strict Separation of Concerns | Backend handles only API/data logic, no frontend | ✅ PASS - FastAPI pure backend, no Next.js code |
| Security by Design - Stateless JWT | No session database, JWT-only auth with shared secret | ✅ PASS - PyJWT middleware, BETTER_AUTH_SECRET from env |
| Multi-User Data Isolation | Query-level filtering on user_id, database foreign key | ✅ PASS - SQLModel enforces FK, all queries filtered by user_id |
| Reliable Persistent Storage | PostgreSQL with SQLModel ORM, migrations versioned | ✅ PASS - Neon PostgreSQL, SQLModel models with migrations |
| Modern Responsive Codebase | Type hints, PEP 8, comprehensive comments, Swagger docs | ✅ PASS - Python type hints, inline comments, auto-generated docs |

**Technology Stack Alignment:**

| Requirement | Plan | Alignment |
|-------------|------|-----------|
| FastAPI backend | FastAPI 0.100+ (Python) | ✅ EXACT MATCH |
| SQLModel ORM | SQLModel 0.12+ | ✅ EXACT MATCH |
| Neon PostgreSQL | psycopg2 sync driver + SQLAlchemy | ✅ EXACT MATCH |
| JWT authentication | PyJWT + FastAPI Depends | ✅ EXACT MATCH (Better Auth compatible) |
| 6 exact endpoints | RESTful with correct HTTP methods | ✅ EXACT MATCH |

**Gate Result**: ✅ PASS - All constitutional principles verified. No conflicts. Ready to proceed with design.

## Key Technical Decisions

### 1. Database Connection Strategy: Synchronous SQLAlchemy Core

**Decision**: Use synchronous `sqlalchemy.create_engine()` with psycopg2 driver

**Rationale**:
- Hackathon scope doesn't require async/scaling benefits
- Synchronous code is simpler to understand, debug, and test
- SQLModel with sync is well-documented and production-proven
- Reduces dependency complexity (no asyncpg, no async context managers)

**Alternatives Considered**:
- **Async with asyncpg**: Better for 100+ concurrent users, but adds complexity; not needed for hackathon
- **Connection pooling (SQLAlchemy pool)**: Will be included in sync approach for good practice

**Tradeoff**: Loss of theoretical scalability vs. gain in development speed and simplicity. ✅ Acceptable for hackathon.

### 2. JWT Verification Library: PyJWT

**Decision**: Use `PyJWT` library for token verification

**Rationale**:
- Minimal dependencies (PyJWT is core JWT spec implementation)
- Battle-tested, production-ready, widely adopted
- Simple API: `jwt.decode(token, secret, algorithms=["HS256"])`
- No bloat; Better Auth compatible

**Alternatives Considered**:
- **python-jose**: Feature-rich (supports JWE, JWS variants), but heavier; overkill for our use case
- **authlib**: Full OAuth2/OIDC framework, not needed; too much overhead

**Tradeoff**: Less feature-rich vs. simpler and faster. ✅ Best fit for hackathon scope.

### 3. Authenticated User Dependency Injection: Reusable `Depends` Pattern

**Decision**: Create a reusable `current_user()` dependency for FastAPI route protection

**Rationale**:
- FastAPI Depends pattern is idiomatic and DRY (don't repeat yourself)
- Single dependency handles all auth logic: extract token → verify signature → extract user_id → return user
- All routes with `current_user` parameter automatically enforce auth
- Reduces code duplication across 6 endpoints

**Implementation Pattern**:
```python
async def current_user(request: Request) -> str:
    # Extract token from Authorization: Bearer <token> header
    # Verify JWT signature using BETTER_AUTH_SECRET
    # Return user_id or raise HTTPException(401)

@app.get("/api/{user_id}/tasks")
def get_tasks(user_id: str, user: str = Depends(current_user)):
    # user is now authenticated user_id from token
    # Verify user_id == request user_id (ownership check)
```

**Alternatives Considered**:
- **Per-route token extraction**: Copy-paste verification code in each route (redundant, error-prone)
- **Middleware-only approach**: Attach user to request context (less type-safe, harder to test)

**Tradeoff**: Slight learning curve vs. elegant, maintainable code. ✅ Worth it for 6 endpoints.

### 4. Error Handling: Global Exception Handlers + Per-Route Raises

**Decision**: Combine global `@app.exception_handler()` for common errors (401, 403, 404) + explicit raises in routes

**Rationale**:
- Global handlers ensure consistent error response format (JSON with error message)
- Centralized 401/403/404 logic avoids repetition
- Per-route raises are explicit and testable
- FastAPI automatically catches `HTTPException` and applies handler

**Implementation Pattern**:
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status": exc.status_code}
    )

# In routes:
if not user_owns_task(task_id):
    raise HTTPException(status_code=403, detail="Permission denied")
```

**Alternatives Considered**:
- **Only per-route raises**: No consistency guarantee; error format varies by route
- **Only global middleware**: Hard to provide context-specific error messages

**Tradeoff**: Dual approach vs. simpler single approach. ✅ Better error handling quality.

### 5. Environment Variable Management: Pydantic `BaseSettings`

**Decision**: Use `pydantic.BaseSettings` for configuration management

**Rationale**:
- Validates environment variables at app startup (fail fast if BETTER_AUTH_SECRET missing)
- Type-safe: `DATABASE_URL: str`, `JWT_EXPIRY_DAYS: int` are validated types, not strings
- Single `config.py` file: all env vars in one place, imported throughout app
- Better than `python-dotenv` + `os.getenv()` (no type safety, no early validation)

**Implementation Pattern**:
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    JWT_EXPIRY_DAYS: int = 7
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()  # Validates .env at import time
```

**Alternatives Considered**:
- **python-dotenv + os.getenv()**: Simple but no validation; silent failures if vars missing
- **Direct environment module**: No type validation

**Tradeoff**: Slight setup overhead vs. robust configuration. ✅ Better for production readiness.

## Project Structure

### Documentation (Feature Specification)

```text
specs/001-fastapi-backend/
├── spec.md                    # User stories & requirements (existing)
├── plan.md                    # This file - architecture decisions
├── research.md                # Phase 0 - Research findings (generated)
├── data-model.md              # Phase 1 - Entity definitions & schema
├── contracts/                 # Phase 1 - API endpoint contracts (OpenAPI)
│   └── api-openapi.yaml       # OpenAPI 3.0 specification
├── quickstart.md              # Phase 1 - Setup & run instructions
├── checklists/
│   └── requirements.md        # Quality validation checklist (existing)
└── tasks.md                   # Phase 2 - Implementation tasks (/sp.tasks)
```

### Source Code (Backend Application)

**Selected Structure**: Option 1 - Single Backend Project (FastAPI is monolithic by design)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization, route mounting
│   ├── config.py              # Pydantic BaseSettings for env vars
│   ├── database.py            # SQLAlchemy engine, session factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py            # SQLModel Task entity with validation
│   │   └── schemas.py         # Pydantic schemas for request/response validation
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py    # Reusable Depends: current_user()
│   │   └── routes.py          # All 6 endpoints: GET, POST, PUT, DELETE, PATCH
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py            # JWT verification middleware (optional if using Depends)
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py    # Business logic: get_task, create_task, etc.
│   └── utils/
│       ├── __init__.py
│       └── errors.py          # Custom exception classes
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest fixtures (test DB, auth tokens, etc.)
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py     # Task model validation tests
│   │   └── test_schemas.py    # Pydantic schema validation tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_auth.py       # JWT verification, 401 tests
│   │   ├── test_endpoints.py  # All 6 endpoints happy path + error cases
│   │   ├── test_ownership.py  # User A cannot access User B's tasks
│   │   └── test_database.py   # Data persistence, concurrent access
│   └── contract/
│       ├── __init__.py
│       └── test_api_contract.py  # OpenAPI compliance tests
│
├── migrations/
│   └── alembic/               # Database migration scripts (optional, can start with SQLModel auto-create)
│
├── .env.example               # Template for required environment variables
├── .env                       # NEVER COMMIT - local environment variables
├── .gitignore                 # Ignore .env, __pycache__, venv, etc.
├── requirements.txt           # Python dependencies (pip freeze)
├── pyproject.toml             # Modern Python project config (alternative to setup.py)
├── Makefile                   # Dev convenience: make install, make test, make run
├── README.md                  # Quick start guide (symlink to quickstart.md)
└── docker-compose.yml         # Optional: Local Neon PostgreSQL for development (or use cloud)
```

**Structure Decision Rationale**:
- **Single `backend/` directory**: All backend code in one place; can later split into multiple services if needed
- **Clear separation**: `models/` → database layer; `api/routes.py` → HTTP layer; `services/` → business logic layer
- **Organized tests**: Unit (models), Integration (routes + DB), Contract (OpenAPI)
- **Configuration centralized**: `config.py` handles all env vars and settings
- **PEP 8 friendly**: Clear module organization, easy to navigate

## High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  - Handles user signup/signin via Better Auth               │
│  - Receives JWT token from Better Auth                      │
│  - Stores token in localStorage / HTTP-only cookie          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    Authorization: Bearer <JWT>
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    FastAPI Backend                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─ HTTP Request with JWT Token ────────────────────────┐  │
│  │                                                       │  │
│  ├─→ [JWT Verification Middleware / Depends]            │  │
│  │   - Extract token from Authorization header          │  │
│  │   - Verify signature using BETTER_AUTH_SECRET        │  │
│  │   - Decode and extract user_id claim                 │  │
│  │   - Raise 401 if invalid/expired                     │  │
│  │                                                       │  │
│  ├─→ [Route Handler]                                    │  │
│  │   - Receive authenticated user_id via Depends        │  │
│  │   - Validate ownership: user_id == request user_id   │  │
│  │   - Query SQLModel models (filtered by user_id)      │  │
│  │   - Execute business logic (create, read, etc.)      │  │
│  │   - Raise 403 if ownership violated                  │  │
│  │   - Raise 404 if task not found                      │  │
│  │                                                       │  │
│  ├─→ [SQLModel ORM]                                     │  │
│  │   - Type-safe models with Pydantic validation        │  │
│  │   - Automatic database schema generation             │  │
│  │   - Query builder with ownership filtering           │  │
│  │                                                       │  │
│  ├─→ [Response]                                         │  │
│  │   - JSON response with HTTP status code              │  │
│  │   - Global exception handlers format errors          │  │
│  │   - Swagger/OpenAPI auto-documents all endpoints     │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    SQL Query (filtered by user_id)
                           │
┌──────────────────────────▼──────────────────────────────────┐
│           Neon Serverless PostgreSQL                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  tasks table:                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ id (UUID) │ user_id (FK) │ title │ description │ ... │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ task-001  │ user-A       │ ...   │ ...         │ ... │  │
│  │ task-002  │ user-A       │ ...   │ ...         │ ... │  │
│  │ task-003  │ user-B       │ ...   │ ...         │ ... │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  All queries automatically filtered:                        │
│  SELECT * FROM tasks WHERE user_id = 'user-A'              │
│  (User A only sees task-001, task-002)                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Database Schema Design

### Task Entity (SQLModel Model)

```python
from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    """Base fields shared between request/response and database models"""
    title: str = Field(min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    completed: bool = Field(default=False, description="Completion status")

class Task(TaskBase, table=True):
    """Database model for tasks table"""
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # No users table; trusts JWT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    """Request schema for creating tasks (no id, timestamps, or user_id - assigned by backend)"""
    pass

class TaskUpdate(SQLModel):
    """Request schema for updating tasks (all fields optional)"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    # Note: completed is NOT updatable via PUT; only via PATCH /complete

class TaskResponse(TaskBase):
    """Response schema for all endpoints (includes id, timestamps, user_id)"""
    id: uuid.UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
```

### Database Migration (Alembic-optional, can use SQLModel auto-create)

```sql
-- Create users table (reference for foreign key, but no auth operations in backend)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create tasks table with multi-user data isolation
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index on user_id for fast filtering (critical for multi-user queries)
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Index on user_id + created_at for sorting queries
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

## API Endpoint Contracts

### RESTful Design Principles

All 6 endpoints follow strict RESTful conventions:

| Method | Path | Semantics | Status Codes |
|--------|------|-----------|--------------|
| GET | `/api/{user_id}/tasks` | Retrieve all user's tasks | 200, 401, 403 |
| POST | `/api/{user_id}/tasks` | Create new task | 201, 400, 401, 403 |
| GET | `/api/{user_id}/tasks/{id}` | Retrieve single task | 200, 401, 403, 404 |
| PUT | `/api/{user_id}/tasks/{id}` | Update task (title, description) | 200, 400, 401, 403, 404 |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | 204, 401, 403, 404 |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion status | 200, 401, 403, 404 |

### Example Endpoint: GET /api/{user_id}/tasks

**Request**:
```
GET /api/user-123/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoidXNlci0xMjMifQ...
```

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "user-123",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-08T10:00:00Z",
      "updated_at": "2026-01-08T10:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "user-123",
      "title": "Finish project",
      "description": null,
      "completed": true,
      "created_at": "2026-01-08T09:00:00Z",
      "updated_at": "2026-01-08T11:30:00Z"
    }
  ]
}
```

**Response (401 Unauthorized - missing token)**:
```json
{
  "error": "Missing or invalid authentication token",
  "status": 401
}
```

**Response (403 Forbidden - user_id mismatch)**:
```json
{
  "error": "You do not have permission to access these tasks",
  "status": 403
}
```

*See `contracts/api-openapi.yaml` for complete OpenAPI 3.0 specification*

## JWT Authentication Flow

### Token Verification Process

```
1. Frontend receives JWT from Better Auth
   - Token contains: { "user_id": "user-123", "exp": 1704844800, ... }
   - Shared secret: BETTER_AUTH_SECRET from environment

2. Frontend includes token in every API request
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

3. Backend FastAPI Depends (current_user):
   a. Extract Authorization header
   b. Parse "Bearer <token>" format
   c. Call jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
   d. On success: Extract user_id claim → return user_id
   e. On failure: Raise HTTPException(status_code=401, detail="Token invalid/expired")

4. Route handler receives authenticated user_id
   @app.get("/api/{user_id}/tasks")
   def get_tasks(user_id: str, user: str = Depends(current_user)):
       # Ownership check: if user != user_id → raise 403
       # Query: SELECT * FROM tasks WHERE user_id = user
       # Return filtered results

5. Response sent to frontend (200, 400, 401, 403, or 404)
```

### Middleware/Dependency Implementation Pattern

```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from app.config import settings

security = HTTPBearer()

def current_user(credentials: HTTPBearer = Depends(security)) -> str:
    """
    Extract and verify JWT token from Authorization header.
    Returns authenticated user_id or raises 401.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

# Usage in routes:
@app.get("/api/{user_id}/tasks")
def get_tasks(user_id: str, auth_user: str = Depends(current_user)):
    if auth_user != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    # proceed with query filtered by user_id
```

## Implementation Phases

### Phase 0: Foundation & Research

**Purpose**: Resolve all design unknowns, document technical decisions

**Deliverables**:
- `research.md`: Technology comparisons, best practices, decision rationale
- Updated plan.md with all decisions documented (completed above)

**Timeline**: Same as plan execution

### Phase 1: Design & Contracts

**Purpose**: Document data model, API contracts, and setup instructions

**Deliverables**:
1. `data-model.md`: Complete SQLModel entity definitions with validation rules
2. `contracts/api-openapi.yaml`: OpenAPI 3.0 specification (auto-generated from FastAPI Swagger)
3. `quickstart.md`: Step-by-step local setup guide (clone, venv, pip install, .env, run)
4. Updated backend context for fastapi-backend-dev agent

**Timeline**: After Phase 0, before Phase 2 tasks

### Phase 2: Tasks Breakdown

**Purpose**: Decompose into specific, testable, actionable implementation tasks

**Deliverables** (generated by `/sp.tasks`):
- `tasks.md`: Prioritized tasks organized by phase:
  - Setup: Project init, dependencies, database connection
  - Foundation: Models, schemas, database migrations
  - Auth Layer: JWT middleware, Depends, error handlers
  - Core API: 6 endpoints with ownership enforcement
  - Testing: Unit, integration, contract tests
  - Polish: Documentation, response models, Swagger tweaks

**Timeline**: After Phase 1, drives implementation phase

### Phase 3: Implementation

**Purpose**: Execute tasks using fastapi-backend-dev agent (no manual coding)

**Approach**:
- Each task creates a focused PR or commit
- All code generated via Claude Code agents
- No manual editing—agents handle all implementation
- Tests run after each major phase

**Timeline**: Longest phase, parallel opportunities for independent tasks

### Phase 4: Testing & Validation

**Purpose**: Verify all success criteria met, prepare for frontend integration

**Validation**:
- ✅ All 6 endpoints functional with correct HTTP methods and status codes
- ✅ JWT authentication verified (401 for missing/invalid tokens)
- ✅ Multi-user data isolation (User A cannot access User B's tasks)
- ✅ Database persistence (data survives restarts)
- ✅ Swagger UI documents all endpoints
- ✅ 90%+ test coverage
- ✅ <500ms API response time

**Timeline**: Parallel with implementation, final validation before frontend integration

## Testing Strategy

### Test Categories

#### 1. Unit Tests (pytest, test_models.py)
- **Purpose**: Validate Task model and schemas in isolation
- **Examples**:
  - Task model creation with valid/invalid fields
  - Pydantic schema validation (TaskCreate, TaskUpdate, TaskResponse)
  - Field constraints (title max 255, description max 2000)
- **Coverage**: 20-30 tests

#### 2. Authentication Tests (test_auth.py)
- **Purpose**: Verify JWT verification middleware
- **Examples**:
  - Request without Authorization header → 401
  - Request with malformed token → 401
  - Request with invalid signature → 401
  - Request with expired token → 401
  - Request with valid token → extracts user_id correctly
- **Coverage**: 8-10 tests

#### 3. Ownership Enforcement Tests (test_ownership.py)
- **Purpose**: Ensure multi-user data isolation
- **Examples**:
  - User A tries to GET tasks belonging to User B → 403 or 404
  - User A tries to PUT task belonging to User B → 403
  - User A tries to DELETE task belonging to User B → 403
  - User A tries to PATCH complete task of User B → 403
- **Coverage**: 12-15 tests

#### 4. Endpoint Integration Tests (test_endpoints.py)
- **Purpose**: Happy path + error cases for all 6 endpoints
- **Examples**:
  - POST /tasks with valid data → 201 + task object
  - POST /tasks with missing title → 400 + error message
  - GET /tasks with no tasks → 200 + empty list
  - GET /tasks/{id} with valid id → 200 + task object
  - GET /tasks/{id} with non-existent id → 404
  - PUT /tasks/{id} with valid update → 200 + updated task
  - PATCH /tasks/{id}/complete → toggles completed field
  - DELETE /tasks/{id} → 204 + task no longer exists
- **Coverage**: 20-25 tests

#### 5. Database Integration Tests (test_database.py)
- **Purpose**: Verify persistence, concurrent access, query filtering
- **Examples**:
  - Create task → query returns it
  - Update task → changes persisted
  - Delete task → query no longer returns it
  - Multiple users' tasks are isolated (SELECT * FROM tasks WHERE user_id=X)
  - Data survives application restart
- **Coverage**: 10-12 tests

#### 6. Contract Compliance Tests (test_api_contract.py)
- **Purpose**: Verify API matches OpenAPI spec
- **Examples**:
  - All 6 endpoints exist with correct HTTP methods
  - All status codes (200, 201, 204, 400, 401, 403, 404) are documented
  - Request/response schemas match spec
  - Required headers (Authorization) are documented
- **Coverage**: 6-8 tests

### Test Fixtures (conftest.py)

```python
@pytest.fixture
def test_client():
    """FastAPI test client for making requests"""
    from fastapi.testclient import TestClient
    return TestClient(app)

@pytest.fixture
def test_db():
    """In-memory SQLite database for testing (faster than Neon)"""
    # Create test database, populate with schema
    yield db
    # Cleanup after test

@pytest.fixture
def valid_jwt_token():
    """Valid JWT token for user-123"""
    import jwt
    return jwt.encode(
        {"user_id": "user-123"},
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256"
    )

@pytest.fixture
def user_a_task(test_db):
    """Pre-created task owned by user-123"""
    task = Task(user_id="user-123", title="Test task")
    test_db.add(task)
    test_db.commit()
    return task
```

### Test Execution Plan

1. **Before Implementation**:
   - Set up test fixtures and database schema
   - Write test file stubs (ensure imports work)

2. **After Phase 1 (Models)**:
   - Run unit tests: `pytest tests/unit/`
   - Expect: All model validation tests pass

3. **After Phase 2 (Auth)**:
   - Run auth tests: `pytest tests/integration/test_auth.py`
   - Expect: JWT verification works, 401 errors returned correctly

4. **After Phase 3 (Endpoints)**:
   - Run endpoint tests: `pytest tests/integration/test_endpoints.py`
   - Run ownership tests: `pytest tests/integration/test_ownership.py`
   - Expect: All CRUD operations work, multi-user isolation enforced

5. **After Phase 4 (Polish)**:
   - Run full test suite: `pytest tests/`
   - Target: 90%+ coverage
   - Manual verification: Open Swagger UI at http://localhost:8000/docs, test all 6 endpoints with curl or Postman

### Success Metrics

- **Test Coverage**: `pytest --cov=app tests/` → 90%+ coverage
- **All Tests Pass**: `pytest tests/` → 0 failures
- **Manual Verification**: All 6 endpoints work via Swagger UI
- **Performance**: Endpoints respond <500ms under local test load
- **Documentation**: Swagger UI displays all endpoints with request/response examples

## Deployment & Operations

### Local Development

```bash
# Clone repository
git clone <repo-url>
cd hackathon2-todo-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and fill in:
# - DATABASE_URL=postgresql://<user>:<pass>@<host>/<db>
# - BETTER_AUTH_SECRET=<shared-secret-from-better-auth>

# Run database migrations
alembic upgrade head  # or let SQLModel auto-create tables

# Start server
uvicorn app.main:app --reload

# Access API
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - API root: http://localhost:8000/

# Run tests
pytest tests/ -v --cov=app
```

### Production Deployment (Future)

- Use `gunicorn` or `uvicorn` with multiple workers
- Environment: Vercel/AWS Lambda/GCP Cloud Run (serverless FastAPI)
- Database: Neon PostgreSQL (already serverless)
- Monitoring: Log aggregation (Sentry, CloudWatch), metrics (Prometheus)
- CI/CD: GitHub Actions → run tests → deploy to production

## Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| JWT token verification fails | Medium | High | Comprehensive auth tests, manual Swagger verification |
| Database connectivity issues | Low | High | Connection pooling, retry logic, test with actual Neon instance early |
| User_id filtering not enforced | Medium | Critical | Ownership tests catch this, query-level filtering in ORM |
| Response format inconsistency | Low | Medium | Global exception handlers, Pydantic schemas enforce format |
| Test coverage incomplete | Medium | Medium | 90%+ coverage target, explicit mapping of tests to success criteria |

## Next Steps

1. **Phase 0 (Research)**: Already complete in this plan; no additional research needed
2. **Phase 1 (Design)**: Generate `data-model.md`, `contracts/api-openapi.yaml`, `quickstart.md`
3. **Phase 2 (Tasks)**: Run `/sp.tasks` to break into implementation tasks
4. **Phase 3 (Implementation)**: Execute tasks via `fastapi-backend-dev` agent
5. **Phase 4 (Testing)**: Run full test suite, manual Swagger verification, sign-off for frontend integration

---

**Status**: ✅ Planning Complete - Ready for `/sp.tasks` phase

**Plan Version**: 1.0.0 | **Created**: 2026-01-08 | **Last Updated**: 2026-01-08
