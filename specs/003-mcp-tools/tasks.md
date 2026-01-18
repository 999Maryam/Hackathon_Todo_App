# Tasks: MCP Tools Server & Task Operations

**Feature**: MCP Tools Server & Task Operations
**Branch**: `003-mcp-tools`
**Spec**: [specs/003-mcp-tools/spec.md](spec.md)
**Plan**: [specs/003-mcp-tools/plan.md](plan.md)

## Overview

This feature implements 5 MCP tools for the OpenAI agent to manage todo tasks: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`. The tools provide AI-driven task management with strict user ownership isolation.

## Implementation Strategy

- **MVP Scope**: Implement User Story 1 (Add Task via AI) first, then other stories in priority order
- **Approach**: Top-down implementation following the quickstart guide
- **Testing**: Integration tests for each tool with user isolation validation

---

## Phase 1: Setup & Dependencies

**Goal**: Prepare development environment with MCP SDK and tools directory structure

- [X] T001 Add MCP SDK dependency to backend requirements
- [X] T002 Install MCP SDK in backend virtual environment
- [X] T003 Create tools directory structure in backend/app/tools/
- [X] T004 Create initial __init__.py file for tools package

---

## Phase 2: Tool Implementation Functions

**Goal**: Implement the 5 core tool functions with user isolation and proper error handling

- [X] T005 [P] [US1] Create task_tools.py with add_task function
- [X] T006 [P] [US2] Add list_tasks function to task_tools.py
- [X] T007 [P] [US3] Add complete_task function to task_tools.py
- [X] T008 [P] [US4] Add delete_task function to task_tools.py
- [X] T009 [P] [US5] Add update_task function to task_tools.py
- [X] T010 [P] Add _get_task_if_owned helper function for user isolation
- [X] T011 Update tools __init__.py to export all 5 functions

---

## Phase 3: MCP Server Implementation

**Goal**: Create FastMCP server that registers the 5 tools with proper context management

- [X] T012 Create mcp_server.py with FastMCP server setup
- [X] T013 Implement lifespan context for database session management
- [X] T014 Register add_task tool with MCP server
- [X] T015 Register list_tasks tool with MCP server
- [X] T016 Register complete_task tool with MCP server
- [X] T017 Register delete_task tool with MCP server
- [X] T018 Register update_task tool with MCP server
- [X] T019 Add server entry point with if __name__ == "__main__"

---

## Phase 4: User Story 1 - Add Task via AI

**Goal**: Enable AI to create tasks for users with proper validation and ownership

**Independent Test**: Call `add_task` with user_id and title, verify task exists in database with correct ownership and returns expected format

- [X] T020 [US1] Test add_task with valid inputs returns correct format
- [X] T021 [US1] Test add_task with missing title returns error
- [X] T022 [US1] Test add_task with empty title returns error
- [X] T023 [US1] Verify created task has correct user_id in database

---

## Phase 5: User Story 2 - List Tasks via AI

**Goal**: Enable AI to retrieve user's tasks with optional status filtering

**Independent Test**: Create tasks for a user, call `list_tasks`, verify only that user's tasks are returned

- [X] T024 [US2] Test list_tasks returns all tasks when status="all"
- [X] T025 [US2] Test list_tasks returns only pending tasks when status="pending"
- [X] T026 [US2] Test list_tasks returns only completed tasks when status="completed"
- [X] T027 [US2] Test list_tasks with invalid status defaults to "all"
- [X] T028 [US2] Verify user isolation - User A cannot see User B's tasks

---

## Phase 6: User Story 3 - Complete Task via AI

**Goal**: Enable AI to mark user's tasks as completed

**Independent Test**: Create incomplete task, call `complete_task`, verify task's completed field is true

- [X] T029 [US3] Test complete_task marks task as completed
- [X] T030 [US3] Test complete_task returns correct success format
- [X] T031 [US3] Test complete_task with non-existent task returns error
- [X] T032 [US3] Test complete_task with other user's task returns error
- [X] T033 [US3] Verify user isolation - User A cannot complete User B's task

---

## Phase 7: User Story 4 - Delete Task via AI

**Goal**: Enable AI to permanently remove user's tasks

**Independent Test**: Create task, call `delete_task`, verify task no longer exists in database

- [X] T034 [US4] Test delete_task removes task from database
- [X] T035 [US4] Test delete_task returns correct success format
- [X] T036 [US4] Test delete_task with non-existent task returns error
- [X] T037 [US4] Test delete_task with other user's task returns error
- [X] T038 [US4] Verify user isolation - User A cannot delete User B's task

---

## Phase 8: User Story 5 - Update Task via AI

**Goal**: Enable AI to modify user's task title and/or description

**Independent Test**: Create task, call `update_task` with new values, verify database reflects changes

- [X] T039 [US5] Test update_task updates title when provided
- [X] T040 [US5] Test update_task updates description when provided
- [X] T041 [US5] Test update_task preserves unchanged fields
- [X] T042 [US5] Test update_task with non-existent task returns error
- [X] T043 [US5] Test update_task with other user's task returns error
- [X] T044 [US5] Verify user isolation - User A cannot update User B's task

---

## Phase 9: Integration & Edge Case Testing

**Goal**: Comprehensive testing of all tools and edge cases

- [X] T045 Create comprehensive integration test suite
- [X] T046 Test all error scenarios across all tools
- [X] T047 Test UUID validation in all tools that accept task_id
- [X] T048 Test behavior when database is unavailable
- [X] T049 Test multiple users with overlapping task operations
- [X] T050 Test 100+ tasks per user performance

---

## Phase 10: Documentation & Polish

**Goal**: Complete documentation and ensure all success criteria are met

- [X] T051 Update API documentation with MCP tool schemas
- [X] T052 Create usage examples for all 5 tools
- [X] T053 Verify all 7 success criteria are met (SC-001 through SC-007)
- [X] T054 Run full test suite to verify no regressions
- [X] T055 Update quickstart guide with any implementation refinements

---

## Dependencies

**User Story Order**:
1. US1 (Add Task) - Foundation for all other operations
2. US2 (List Tasks) - Depends on US1 for test data
3. US3 (Complete Task) - Depends on US1 for test data
4. US4 (Delete Task) - Depends on US1 for test data
5. US5 (Update Task) - Depends on US1 for test data

**Parallel Opportunities**:
- Tools implementation (T005-T009) can be done in parallel by different developers
- Individual user story tests (T020-T044) can be developed in parallel

---

## MVP Scope

Minimum Viable Product includes:
- T001-T011: Complete tool implementation with MCP server
- T020-T023: Add task functionality with tests
- Basic integration tests for user isolation

This enables the core "Add Task via AI" functionality while establishing the foundation for other operations.