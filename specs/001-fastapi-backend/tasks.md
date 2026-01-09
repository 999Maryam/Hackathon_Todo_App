---
description: "Implementation tasks for Backend API"
---

# Tasks: Backend API for Todo Full-Stack Web Application

**Input**: Design documents from `/specs/001-fastapi-backend/`
**Prerequisites**: plan.md (✅ complete), spec.md (✅ complete), data-model.md (✅ complete), contracts/api-openapi.yaml (✅ complete)

**Tests**: Full pytest suite with unit, integration, and contract tests required per specification success criteria

**Organization**: Tasks are grouped by phase, with user stories (US1-US6) as independent implementation and testing units

---

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

---

## Path Conventions

- Backend application: `backend/app/`
- Backend tests: `backend/tests/`
- Configuration: `backend/app/config.py`
- Database: `backend/app/database.py`
- Models: `backend/app/models/`
- API routes: `backend/app/api/`
- Services: `backend/app/services/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend project structure with app/, tests/, migrations/ directories
- [ ] T002 Create requirements.txt with FastAPI, SQLModel, PyJWT, psycopg2, pytest dependencies
- [ ] T003 [P] Create .env.example with DATABASE_URL and BETTER_AUTH_SECRET placeholders
- [ ] T004 [P] Create .gitignore to ignore .env, __pycache__, venv, .pytest_cache
- [ ] T005 Create backend/app/__init__.py and backend/tests/__init__.py
- [ ] T006 [P] Create Makefile with targets: install, test, run, lint (optional)
- [ ] T007 [P] Create README.md linking to specs/001-fastapi-backend/quickstart.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create backend/app/config.py with Pydantic BaseSettings for DATABASE_URL and BETTER_AUTH_SECRET
- [ ] T009 Create backend/app/database.py with SQLAlchemy engine, session factory, and create_db_and_tables() function
- [ ] T010 [P] Create backend/app/models/task.py with SQLModel Task entity (id, user_id, title, description, completed, created_at, updated_at)
- [ ] T011 [P] Create backend/app/models/schemas.py with Pydantic schemas: TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, ErrorResponse
- [ ] T012 Create backend/app/api/dependencies.py with current_user() Depends function for JWT verification using PyJWT
- [ ] T013 Create backend/app/utils/errors.py with custom HTTPException handlers for 401, 403, 404 errors
- [ ] T014 Create backend/app/main.py with FastAPI app initialization, route mounting, and global exception handlers
- [ ] T015 Create backend/app/services/task_service.py with TaskService class stub (get_all_tasks, get_task, create_task, update_task, delete_task, toggle_complete methods)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a Task (Priority: P1) 🎯 MVP

**Goal**: Implement POST /api/{user_id}/tasks endpoint with JWT authentication and validation

**Independent Test**: Can be fully tested by making POST request with valid JWT, verifying 201 response with task object, and confirming task is stored in database with correct user_id

### Tests for User Story 1 (Required - TDD approach)

- [ ] T016 [P] [US1] Create backend/tests/integration/test_endpoints_create.py with test for POST /tasks with valid JWT → 201 Created
- [ ] T017 [P] [US1] Add test for POST /tasks without JWT token → 401 Unauthorized
- [ ] T018 [P] [US1] Add test for POST /tasks with invalid JWT → 401 Unauthorized
- [ ] T019 [P] [US1] Add test for POST /tasks with expired JWT → 401 Unauthorized
- [ ] T020 [P] [US1] Add test for POST /tasks with missing title → 400 Bad Request
- [ ] T021 [P] [US1] Add test for POST /tasks with title too long → 400 Bad Request
- [ ] T022 [P] [US1] Add test for POST /tasks with description too long → 400 Bad Request
- [ ] T023 [P] [US1] Create backend/tests/integration/test_database_create.py to verify task is persisted with correct user_id

### Implementation for User Story 1

- [ ] T024 [US1] Implement TaskService.create_task() in backend/app/services/task_service.py with Pydantic validation and database insertion
- [ ] T025 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/app/api/routes.py with ownership validation and error handling
- [ ] T026 [US1] Add logging for task creation operations in backend/app/api/routes.py
- [ ] T027 [US1] Verify Swagger UI auto-documents POST endpoint with request/response schemas

**Checkpoint**: User Story 1 (Create Task) is fully functional and independently testable

---

## Phase 4: User Story 2 - List All Tasks (Priority: P1)

**Goal**: Implement GET /api/{user_id}/tasks endpoint with multi-user data isolation

**Independent Test**: Can be fully tested by creating multiple tasks for one user, retrieving via GET, and verifying only that user's tasks are returned with correct filtering

### Tests for User Story 2 (Required - TDD approach)

- [ ] T028 [P] [US2] Create backend/tests/integration/test_endpoints_list.py with test for GET /tasks with valid JWT → 200 OK with list
- [ ] T029 [P] [US2] Add test for GET /tasks with no tasks → 200 OK with empty list
- [ ] T030 [P] [US2] Add test for GET /tasks with 3 tasks → 200 OK with all 3 tasks
- [ ] T031 [P] [US2] Add test for GET /tasks without JWT token → 401 Unauthorized
- [ ] T032 [P] [US2] Create backend/tests/integration/test_ownership.py with test for GET /api/user_A_id/tasks with user_B's JWT → 403 Forbidden
- [ ] T033 [P] [US2] Add test for user_A cannot see user_B's tasks even with valid JWT in URL mismatch scenario

### Implementation for User Story 2

- [ ] T034 [US2] Implement TaskService.get_all_tasks(user_id) in backend/app/services/task_service.py with user_id filtering
- [ ] T035 [US2] Implement GET /api/{user_id}/tasks endpoint in backend/app/api/routes.py with ownership check
- [ ] T036 [US2] Add logging for task list retrieval operations
- [ ] T037 [US2] Verify Swagger UI documents GET /tasks endpoint with query parameters and response schema

**Checkpoint**: User Stories 1 and 2 (Create and List) both work independently

---

## Phase 5: User Story 3 - Get Single Task (Priority: P1)

**Goal**: Implement GET /api/{user_id}/tasks/{id} endpoint with ownership validation

**Independent Test**: Can be fully tested by creating a task, retrieving it by ID, and verifying all fields are returned

### Tests for User Story 3 (Required - TDD approach)

- [ ] T038 [P] [US3] Create backend/tests/integration/test_endpoints_get.py with test for GET /tasks/{id} with valid JWT → 200 OK
- [ ] T039 [P] [US3] Add test for GET /tasks/{id} with non-existent ID → 404 Not Found
- [ ] T040 [P] [US3] Add test for GET /tasks/{id} without JWT token → 401 Unauthorized
- [ ] T041 [P] [US3] Add test for user_A GET /tasks/{id} where task belongs to user_B → 404 Not Found (filtered view)
- [ ] T042 [P] [US3] Add test for GET returns all task fields including timestamps

### Implementation for User Story 3

- [ ] T043 [US3] Implement TaskService.get_task(user_id, task_id) in backend/app/services/task_service.py with ownership filtering
- [ ] T044 [US3] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/app/api/routes.py
- [ ] T045 [US3] Add logging for single task retrieval operations
- [ ] T046 [US3] Verify Swagger UI documents GET /tasks/{id} endpoint with path parameters

**Checkpoint**: User Stories 1, 2, and 3 (Create, List, Get) all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P1)

**Goal**: Implement PUT /api/{user_id}/tasks/{id} endpoint with partial updates and ownership validation

**Independent Test**: Can be fully tested by creating a task, updating title/description, and verifying changes persist

### Tests for User Story 4 (Required - TDD approach)

- [ ] T047 [P] [US4] Create backend/tests/integration/test_endpoints_update.py with test for PUT /tasks/{id} with valid JWT → 200 OK
- [ ] T048 [P] [US4] Add test for PUT /tasks/{id} updating only title → 200 OK with updated task
- [ ] T049 [P] [US4] Add test for PUT /tasks/{id} updating only description → 200 OK with updated task
- [ ] T050 [P] [US4] Add test for PUT /tasks/{id} with empty title → 400 Bad Request
- [ ] T051 [P] [US4] Add test for PUT /tasks/{id} with non-existent ID → 404 Not Found
- [ ] T052 [P] [US4] Add test for PUT /tasks/{id} without JWT token → 401 Unauthorized
- [ ] T053 [P] [US4] Add test for user_A PUT /tasks/{id} where task belongs to user_B → 403 Forbidden
- [ ] T054 [P] [US4] Add test for PUT /tasks/{id} updates updated_at timestamp but not created_at

### Implementation for User Story 4

- [ ] T055 [US4] Implement TaskService.update_task(user_id, task_id, task_update) in backend/app/services/task_service.py with partial updates
- [ ] T056 [US4] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/app/api/routes.py with ownership check
- [ ] T057 [US4] Add logging for task update operations
- [ ] T058 [US4] Verify Swagger UI documents PUT /tasks/{id} endpoint with request body schema

**Checkpoint**: User Stories 1-4 (Create, List, Get, Update) all work independently

---

## Phase 7: User Story 5 - Toggle Completion (Priority: P1)

**Goal**: Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint to toggle completion status

**Independent Test**: Can be fully tested by creating a task, toggling completion, and verifying status changes persist

### Tests for User Story 5 (Required - TDD approach)

- [ ] T059 [P] [US5] Create backend/tests/integration/test_endpoints_complete.py with test for PATCH /tasks/{id}/complete with completed=false → 200 OK with completed=true
- [ ] T060 [P] [US5] Add test for PATCH /tasks/{id}/complete with completed=true → 200 OK with completed=false (toggle behavior)
- [ ] T061 [P] [US5] Add test for PATCH /tasks/{id}/complete with non-existent ID → 404 Not Found
- [ ] T062 [P] [US5] Add test for PATCH /tasks/{id}/complete without JWT token → 401 Unauthorized
- [ ] T063 [P] [US5] Add test for user_A PATCH /tasks/{id}/complete where task belongs to user_B → 403 Forbidden
- [ ] T064 [P] [US5] Add test for PATCH /tasks/{id}/complete updates updated_at timestamp

### Implementation for User Story 5

- [ ] T065 [US5] Implement TaskService.toggle_complete(user_id, task_id) in backend/app/services/task_service.py
- [ ] T066 [US5] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/app/api/routes.py with ownership check
- [ ] T067 [US5] Add logging for completion toggle operations
- [ ] T068 [US5] Verify Swagger UI documents PATCH /tasks/{id}/complete endpoint

**Checkpoint**: User Stories 1-5 (Create, List, Get, Update, Toggle) all work independently

---

## Phase 8: User Story 6 - Delete Task (Priority: P1)

**Goal**: Implement DELETE /api/{user_id}/tasks/{id} endpoint with permanent deletion and ownership validation

**Independent Test**: Can be fully tested by creating a task, deleting it, and verifying it no longer appears in queries

### Tests for User Story 6 (Required - TDD approach)

- [ ] T069 [P] [US6] Create backend/tests/integration/test_endpoints_delete.py with test for DELETE /tasks/{id} with valid JWT → 204 No Content
- [ ] T070 [P] [US6] Add test for DELETE /tasks/{id} removes task from database (verified by subsequent GET)
- [ ] T071 [P] [US6] Add test for DELETE /tasks/{id} with non-existent ID → 404 Not Found
- [ ] T072 [P] [US6] Add test for DELETE /tasks/{id} without JWT token → 401 Unauthorized
- [ ] T073 [P] [US6] Add test for user_A DELETE /tasks/{id} where task belongs to user_B → 403 Forbidden
- [ ] T074 [P] [US6] Add test for DELETE /tasks/{id} twice → first 204, second 404

### Implementation for User Story 6

- [ ] T075 [US6] Implement TaskService.delete_task(user_id, task_id) in backend/app/services/task_service.py
- [ ] T076 [US6] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/app/api/routes.py with ownership check and 204 response
- [ ] T077 [US6] Add logging for task deletion operations
- [ ] T078 [US6] Verify Swagger UI documents DELETE /tasks/{id} endpoint with 204 response code

**Checkpoint**: All 6 user stories (Complete CRUD + completion toggle) are independently functional

---

## Phase 9: Cross-Cutting Concerns & Polish

**Purpose**: Improvements affecting multiple endpoints and overall quality

- [ ] T079 [P] Create backend/tests/unit/test_models.py with unit tests for Task model validation (title length, description length, etc.)
- [ ] T080 [P] Create backend/tests/unit/test_schemas.py with Pydantic schema validation tests
- [ ] T081 [P] Create backend/tests/contract/test_api_contract.py to verify all 6 endpoints match OpenAPI spec
- [ ] T082 Create backend/tests/integration/test_auth.py consolidating all JWT authentication tests (missing, invalid, expired tokens)
- [ ] T083 Create backend/tests/integration/test_multiuser.py consolidating all multi-user isolation tests (cross-user access attempts)
- [ ] T084 [P] Create backend/tests/conftest.py with pytest fixtures (test client, test database, valid JWT tokens, test users)
- [ ] T085 Create backend/app/utils/logging.py for structured logging across all endpoints
- [ ] T086 Verify all endpoints return consistent error response format with error, status, detail fields
- [ ] T087 Add comprehensive inline comments explaining non-obvious logic in routes, services, middleware
- [ ] T088 Run full test suite: `pytest backend/tests/ -v --cov=backend/app` and verify 90%+ coverage
- [ ] T089 Verify all 6 endpoints appear in Swagger UI at http://localhost:8000/docs with full documentation
- [ ] T090 [P] Create backend/app/middleware/logging.py to log all requests/responses for debugging
- [ ] T091 Verify response times are <500ms for all endpoints under local test load
- [ ] T092 Update backend/README.md with quick start instructions and link to specs/001-fastapi-backend/quickstart.md
- [ ] T093 Create backend/.env.local file with example values (for local development)
- [ ] T094 [P] Verify PEP 8 compliance: `flake8 backend/app backend/tests`
- [ ] T095 [P] Format code: `black backend/app backend/tests`
- [ ] T096 [P] Sort imports: `isort backend/app backend/tests`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories**
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - All 6 stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (all P1, so any order)
  - Each story is independently testable
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (Create Task)**: Depends only on Foundational
- **US2 (List Tasks)**: Depends only on Foundational (and optionally US1 for test data)
- **US3 (Get Task)**: Depends only on Foundational (and optionally US1 for test data)
- **US4 (Update Task)**: Depends only on Foundational (and optionally US1 for test data)
- **US5 (Toggle Complete)**: Depends only on Foundational (and optionally US1 for test data)
- **US6 (Delete Task)**: Depends only on Foundational (and optionally US1 for test data)

**All user stories can be developed in parallel after Foundational phase.**

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Once Foundational phase completes, all 6 user stories can start in parallel:
  - Different teams can work on US1, US2, US3, US4, US5, US6 simultaneously
  - Each story writes tests first (TDD), then implementation
- Within each user story, test tasks marked [P] can run in parallel
- Polish phase tasks marked [P] can run in parallel (unit tests, schema tests, linting, formatting)

---

## Parallel Execution Examples

### Setup Phase (P1)
```
Task: Create project structure
Task: Create requirements.txt
Task: Create .env.example
Task: Create .gitignore
(All can run in parallel - different files, no dependencies)
```

### Foundational Phase (P2 - Note: T008-T015 must complete sequentially for proper setup, but individual components can be worked on)
```
Task: Create config.py (needs to be done before main.py)
Task: Create database.py (needs to be done before services)
Task: Create models (can start once database.py exists)
Task: Create schemas (can start anytime)
Task: Create dependencies.py (needs models ready)
```

### All User Stories in Parallel (P3-P8, after Foundational complete)
```
Developer A: US1 (Create Task) - Tests first, then implementation
Developer B: US2 (List Tasks) - Tests first, then implementation
Developer C: US3 (Get Task) - Tests first, then implementation
Developer D: US4 (Update Task) - Tests first, then implementation
Developer E: US5 (Toggle Complete) - Tests first, then implementation
Developer F: US6 (Delete Task) - Tests first, then implementation
(All 6 stories run in parallel - independent files and functionality)
```

### Polish Phase Tests in Parallel (P9)
```
Task: Unit tests for models
Task: Unit tests for schemas
Task: Contract tests for OpenAPI
Task: Linting (flake8)
Task: Formatting (black)
Task: Import sorting (isort)
(All can run in parallel or sequential based on team capacity)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Create Task)
4. **STOP and VALIDATE**: Run tests, verify via Swagger UI
5. Deploy/demo if ready

### Incremental Delivery (Recommended for Hackathon)

1. Complete Setup → Foundational → Foundation ready
2. Add US1 (Create) → Test independently → Demo
3. Add US2 (List) → Test independently → Demo
4. Add US3 (Get Single) → Test independently → Demo
5. Add US4 (Update) → Test independently → Demo
6. Add US5 (Toggle Complete) → Test independently → Demo
7. Add US6 (Delete) → Test independently → Demo
8. Polish phase (tests, docs, formatting)
9. Final validation: All success criteria met

**Each story adds value independently. Can stop at any checkpoint.**

### Parallel Team Strategy (If Multiple Developers)

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Create)
   - Developer B: US2 (List)
   - Developer C: US3 (Get)
   - Developer D: US4 (Update)
   - Developer E: US5 (Toggle)
   - Developer F: US6 (Delete)
3. Stories complete independently and integrate
4. Polish phase: Full test suite, formatting, docs

---

## Testing Execution Plan

### Run Tests in Phases

**After Foundational (Phase 2)**:
```bash
pytest backend/tests/unit/ -v
# Verify model validation works
```

**After Each User Story**:
```bash
pytest backend/tests/integration/test_endpoints_create.py -v  # US1
pytest backend/tests/integration/test_endpoints_list.py -v    # US2
pytest backend/tests/integration/test_endpoints_get.py -v     # US3
pytest backend/tests/integration/test_endpoints_update.py -v  # US4
pytest backend/tests/integration/test_endpoints_complete.py -v # US5
pytest backend/tests/integration/test_endpoints_delete.py -v  # US6
```

**Full Test Suite (Final)**:
```bash
pytest backend/tests/ -v --cov=backend/app --cov-report=html
# Target: 90%+ coverage, 0 failures
```

**Manual Verification**:
```bash
# Start dev server
uvicorn backend/app.main:app --reload

# In browser: http://localhost:8000/docs
# Test all 6 endpoints with Swagger UI
# Verify error responses (401, 403, 404)
```

---

## Task Checklist Summary

| Phase | Task Count | Description |
|-------|-----------|-------------|
| Setup (P1) | 7 | Project structure, dependencies, configuration |
| Foundational (P2) | 8 | Database, models, schemas, middleware |
| US1 - Create (P3) | 10 | 7 tests + 4 implementation tasks |
| US2 - List (P4) | 10 | 6 tests + 4 implementation tasks |
| US3 - Get (P5) | 10 | 5 tests + 4 implementation tasks |
| US4 - Update (P6) | 12 | 8 tests + 4 implementation tasks |
| US5 - Toggle (P7) | 10 | 6 tests + 4 implementation tasks |
| US6 - Delete (P8) | 10 | 6 tests + 4 implementation tasks |
| Polish (P9) | 18 | Unit tests, integration tests, linting, formatting |
| **TOTAL** | **96** | **All tasks required for production-ready implementation** |

---

## Success Criteria Verification

### Per User Story (Independent Testability)

- [ ] **US1**: POST /api/{user_id}/tasks creates task, returns 201, task stored with correct user_id
- [ ] **US2**: GET /api/{user_id}/tasks lists tasks, returns 200, only authenticated user's tasks shown
- [ ] **US3**: GET /api/{user_id}/tasks/{id} retrieves task, returns 200, 404 for non-existent or other user's task
- [ ] **US4**: PUT /api/{user_id}/tasks/{id} updates task, returns 200, changes persist, ownership enforced
- [ ] **US5**: PATCH /api/{user_id}/tasks/{id}/complete toggles status, returns 200, toggle is idempotent
- [ ] **US6**: DELETE /api/{user_id}/tasks/{id} deletes task, returns 204, task no longer appears

### Authentication & Authorization (Cross-Cutting)

- [ ] Missing JWT token → 401 Unauthorized for all endpoints
- [ ] Invalid JWT token → 401 Unauthorized for all endpoints
- [ ] Expired JWT token → 401 Unauthorized for all endpoints
- [ ] Valid JWT + URL user_id mismatch → 403 Forbidden
- [ ] Cross-user access attempt → 403 Forbidden or 404 Not Found

### Data Integrity & Persistence

- [ ] Tasks persist in Neon PostgreSQL and survive app restart
- [ ] created_at never changes (immutable)
- [ ] updated_at updates only on modification
- [ ] user_id foreign key enforces referential integrity
- [ ] Query-level filtering ensures multi-user isolation

### API Quality

- [ ] All 6 endpoints documented in Swagger UI with examples
- [ ] All HTTP status codes (200, 201, 204, 400, 401, 403, 404, 500) handled
- [ ] Error responses consistent JSON format (error, status, detail)
- [ ] Request validation via Pydantic with clear error messages
- [ ] Response time <500ms for all endpoints

### Code Quality

- [ ] 90%+ test coverage (`pytest --cov=backend/app`)
- [ ] All tests pass (`pytest backend/tests/ -v`)
- [ ] PEP 8 compliance (`flake8 backend/app`)
- [ ] Type hints on all functions and classes
- [ ] Comprehensive inline comments
- [ ] No unused imports or variables

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label = task belongs to specific user story
- Each user story is independently testable and deployable
- Tests written before implementation (TDD approach)
- All tasks reference exact file paths for clarity
- Parallel execution recommended for Phases 3-8 (user stories)
- Polish phase (P9) ensures production-ready quality
- Stop at any checkpoint and have working MVP

---

**Status**: ✅ Ready for implementation

**Total Tasks**: 96 | **Testable Stories**: 6 (US1-US6) | **Parallel Stories**: Yes (all 6 in parallel after Foundational)

**Recommended Start**: Phase 1 (Setup) → Phase 2 (Foundational) → Phase 3-8 in parallel (US1-US6) → Phase 9 (Polish)
