# Tasks: Docker Containerization

**Input**: Design documents from `/specs/008-docker-containerization/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Tests**: No automated tests requested. Verification is manual via docker build/run commands.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- Docker files placed directly in service directories

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify prerequisites and configure Next.js for standalone output

- [X] T001 Verify Docker and docker-compose are installed (run `docker --version` and `docker-compose --version`) - NOTE: Docker not available in WSL2, files created for external testing
- [X] T002 Configure Next.js standalone output mode in frontend/next.config.ts (add `output: 'standalone'`) - Already configured

**Checkpoint**: Prerequisites verified, Next.js configured for containerization

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create .dockerignore files to minimize build context - required before any Dockerfile work

**⚠️ CRITICAL**: .dockerignore files must exist before building images to ensure clean builds

- [X] T003 [P] Create backend/.dockerignore with exclusions for __pycache__, venv, .pytest_cache, .env, *.pyc, .git
- [X] T004 [P] Create frontend/.dockerignore with exclusions for node_modules, .next, .env*, *.log, .git, coverage
- [X] T004.1 Note: Ensure .env file with OPENROUTER_API_KEY is mounted as volume in docker-compose for backend service
**Checkpoint**: Build context exclusions configured - Dockerfile creation can now begin

---

## Phase 3: User Story 1 - Build Production Images (Priority: P1) 🎯 MVP

**Goal**: Create optimized multi-stage Dockerfiles for both frontend and backend services

**Independent Test**: Run `docker build` commands and verify images are created with correct sizes (<500MB backend, <300MB frontend)

**MVP Scope (Core Deliverable)**  
Phase 1–3 (T001–T010): Dockerfiles + build verification  
→ Enables first working containers: todo-backend & todo-frontend

### Implementation for User Story 1

- [X] T005 [P] [US1] Create multi-stage backend/Dockerfile with python:3.13-slim base, non-root user, port 8000
- [X] T006 [P] [US1] Create multi-stage frontend/Dockerfile with node:20-alpine base, standalone output, non-root user, port 3000
- [ ] T007 [US1] Build and verify backend image: `docker build -t todo-backend backend/` (verify size <500MB)
- [ ] T008 [US1] Build and verify frontend image: `docker build -t todo-frontend frontend/` (verify size <300MB)
- [ ] T009 [US1] Verify images run standalone: `docker run -p 8000:8000 todo-backend` and `docker run -p 3000:3000 todo-frontend`
- [ ] T010 [US1] Verify non-root user execution: `docker run todo-backend whoami` should return non-root user

**Checkpoint**: Both images build successfully and run standalone - MVP complete

---

## Phase 4: User Story 2 - Run Services with Docker Compose (Priority: P2)

**Goal**: Create docker-compose.yml for local multi-container orchestration

**Independent Test**: Run `docker-compose up` and verify both services start and communicate

### Implementation for User Story 2

- [X] T011 [US2] Create docker-compose.yml at project root with backend and frontend services
- [X] T012 [US2] Configure docker-compose networking for frontend-backend communication
- [X] T013 [US2] Add env_file configuration for both services in docker-compose.yml
- [X] T014 [US2] Add healthcheck to backend service in docker-compose.yml (curl http://localhost:8000/health)
- [ ] T015 [US2] Verify docker-compose up starts both services: `docker-compose up -d`
- [ ] T016 [US2] Verify backend health: `curl http://localhost:8000/health`
- [ ] T017 [US2] Verify frontend accessible: `curl -I http://localhost:3000`
- [ ] T018 [US2] Verify container health status: `docker-compose ps` shows healthy

**Checkpoint**: Both services run together via docker-compose with proper networking

---

## Phase 5: User Story 3 - Development Mode with Hot Reload (Priority: P3)

**Goal**: Add development profile with volume mounts for hot-reload

**Independent Test**: Start with dev profile, modify source files, verify changes reflect without restart

### Implementation for User Story 3

- [X] T019 [US3] Add dev profile to docker-compose.yml with backend volume mounts
- [X] T020 [US3] Add dev profile to docker-compose.yml with frontend volume mounts
- [X] T021 [US3] Configure uvicorn --reload flag for backend dev mode
- [ ] T022 [US3] Verify dev mode: `docker-compose --profile dev up`
- [ ] T023 [US3] Test backend hot-reload: modify Python file, verify auto-reload
- [ ] T024 [US3] Test frontend hot-reload: modify TypeScript file, verify HMR

**Checkpoint**: Development mode with hot-reload functional

---

## Phase 6: User Story 4 - Build Exclusions via .dockerignore (Priority: P4)

**Goal**: Verify build context optimization is working correctly

**Independent Test**: Measure build context size and verify it's under limits

### Implementation for User Story 4

- [ ] T025 [US4] Verify backend build context size under 50MB during docker build
- [ ] T026 [US4] Verify frontend build context size under 10MB during docker build
- [ ] T027 [US4] Verify excluded files not in images: `docker run todo-backend ls` should not show venv, __pycache__
- [ ] T028 [US4] Verify excluded files not in images: `docker run todo-frontend ls` should not show node_modules

**Checkpoint**: Build context optimized, excluded files verified

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final verification

- [X] T029 [P] Update README.md with Docker build commands section
- [X] T030 [P] Update README.md with docker-compose usage instructions
- [X] T031 [P] Update README.md with development mode instructions
- [X] T032 Add Dockerfile comments with Task ID and spec references
- [ ] T033 Run full verification: clean build, docker-compose up, health checks, dev mode
- [ ] T034 Run quickstart.md validation to ensure all commands work
- [ ] T035 Verify multi-stage builds reduce image size (check docker images command output)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - .dockerignore must exist before Dockerfiles
- **User Story 1 (Phase 3)**: Depends on Foundational - Dockerfiles need .dockerignore
- **User Story 2 (Phase 4)**: Depends on US1 - docker-compose needs built images
- **User Story 3 (Phase 5)**: Depends on US2 - dev profile extends base docker-compose
- **User Story 4 (Phase 6)**: Can run after Foundational (verifies .dockerignore effectiveness)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 (needs built images for compose)
- **User Story 3 (P3)**: Depends on US2 (extends docker-compose.yml)
- **User Story 4 (P4)**: Can start after Foundational - independent verification story

### Within Each User Story

- Create files before testing them
- Build images before running containers
- Base configuration before profile extensions

### Parallel Opportunities

- T003 and T004 can run in parallel (different .dockerignore files)
- T005 and T006 can run in parallel (different Dockerfiles)
- T029, T030, T031 can run in parallel (different README sections)

---

## Parallel Example: User Story 1

```bash
# Launch Dockerfile creation in parallel:
Task: "Create multi-stage backend/Dockerfile with python:3.13-slim base"
Task: "Create multi-stage frontend/Dockerfile with node:20-alpine base"

# Then sequentially verify:
Task: "Build and verify backend image"
Task: "Build and verify frontend image"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T004)
3. Complete Phase 3: User Story 1 (T005-T010)
4. **STOP and VALIDATE**: Both images build and run standalone
5. Demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → .dockerignore ready
2. Add User Story 1 → Images build → Demo (MVP!)
3. Add User Story 2 → docker-compose works → Demo
4. Add User Story 3 → Dev mode works → Demo
5. Add User Story 4 → Build optimization verified → Demo
6. Polish → Documentation complete → Final Demo

### Single Developer Strategy

Execute tasks in order: T001 → T002 → T003 → T004 → ... → T034

Parallel tasks ([P]) can be done sequentially by a single developer.

---

## Task Summary

| Phase | User Story | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| 1 | Setup | 2 | 0 |
| 2 | Foundational | 2 | 2 |
| 3 | US1 - Build Images (MVP) | 6 | 2 |
| 4 | US2 - Docker Compose | 8 | 0 |
| 5 | US3 - Dev Mode | 6 | 0 |
| 6 | US4 - Build Exclusions | 4 | 0 |
| 7 | Polish | 6 | 3 |
| **Total** | | **34** | **7** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story can be independently demonstrated after completion
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
- No automated tests required - verification is manual via docker commands
