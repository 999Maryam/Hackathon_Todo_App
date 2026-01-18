# Feature Specification: MCP Tools Server & Task Operations

**Feature Branch**: `002-mcp-tools`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "MCP Tools Server & Task Operations for Todo AI Chatbot (Phase III - Spec 2)"

---

## Overview

Build a stateless MCP (Model Context Protocol) server that exposes exactly 5 tools for the OpenAI agent to manage todo tasks. The tools enable AI-driven task management through natural language commands while enforcing strict user ownership isolation.

**Context**: This is Phase III - Spec 2 of the Todo AI Chatbot project. It builds on:
- Phase II: Existing Task model, database connection, JWT authentication
- Phase III - Spec 1: Conversation/Message persistence (separate feature)

**Scope**: MCP tool definitions and implementations only. Does NOT include:
- Agent setup or system prompts (Spec 3)
- Chat endpoint or frontend (Spec 4)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task via AI (Priority: P1)

A user tells the AI assistant "Add a task to buy groceries" and the AI uses the `add_task` tool to create the task in the user's todo list.

**Why this priority**: Task creation is the most fundamental operation. Without it, no other operations (list, complete, delete, update) are useful.

**Independent Test**: Can be tested by calling `add_task` with a user_id and title, then verifying the task exists in the database with correct ownership.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** the AI calls `add_task` with title "Buy groceries", **Then** a new task is created with the user's ID and the tool returns `{"task_id": <int>, "status": "created", "title": "Buy groceries"}`
2. **Given** an authenticated user, **When** the AI calls `add_task` with title and description, **Then** both fields are stored correctly
3. **Given** a request without title, **When** the AI calls `add_task`, **Then** the tool returns an error message indicating title is required

---

### User Story 2 - List Tasks via AI (Priority: P1)

A user asks the AI "What are my tasks?" or "Show me pending tasks" and the AI uses the `list_tasks` tool to retrieve and display the user's tasks.

**Why this priority**: Users need to see their tasks to know what to complete or manage. Core read operation.

**Independent Test**: Can be tested by creating tasks for a user, then calling `list_tasks` and verifying only that user's tasks are returned.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks, **When** the AI calls `list_tasks` with status "all", **Then** all 3 tasks are returned as an array
2. **Given** a user with 2 pending and 1 completed task, **When** the AI calls `list_tasks` with status "pending", **Then** only the 2 pending tasks are returned
3. **Given** a user with 2 pending and 1 completed task, **When** the AI calls `list_tasks` with status "completed", **Then** only the 1 completed task is returned
4. **Given** User A with tasks and User B calling `list_tasks`, **When** User B's request executes, **Then** User B sees only their own tasks (empty if none)

---

### User Story 3 - Complete Task via AI (Priority: P1)

A user tells the AI "Mark task 5 as done" and the AI uses the `complete_task` tool to toggle the task's completion status.

**Why this priority**: Core workflow completion. Users create tasks to eventually complete them.

**Independent Test**: Can be tested by creating an incomplete task, calling `complete_task`, and verifying the task's completed field is now true.

**Acceptance Scenarios**:

1. **Given** an incomplete task owned by the user, **When** the AI calls `complete_task` with task_id, **Then** the task is marked completed and returns `{"task_id": <int>, "status": "completed", "title": "<task title>"}`
2. **Given** a task_id that doesn't exist, **When** the AI calls `complete_task`, **Then** an error message "Task not found or not owned" is returned
3. **Given** a task owned by a different user, **When** User B calls `complete_task` with User A's task_id, **Then** User B gets "Task not found or not owned" error

---

### User Story 4 - Delete Task via AI (Priority: P2)

A user tells the AI "Delete task 5" or "Remove the groceries task" and the AI uses the `delete_task` tool to remove the task.

**Why this priority**: Important but less frequent than add/list/complete. Users occasionally need to remove tasks they no longer want.

**Independent Test**: Can be tested by creating a task, calling `delete_task`, and verifying the task no longer exists in the database.

**Acceptance Scenarios**:

1. **Given** a task owned by the user, **When** the AI calls `delete_task` with task_id, **Then** the task is removed and returns `{"task_id": <int>, "status": "deleted", "title": "<task title>"}`
2. **Given** a task_id that doesn't exist, **When** the AI calls `delete_task`, **Then** an error message "Task not found or not owned" is returned
3. **Given** a task owned by User A, **When** User B calls `delete_task` with User A's task_id, **Then** User B gets "Task not found or not owned" error

---

### User Story 5 - Update Task via AI (Priority: P2)

A user tells the AI "Change task 5 title to 'Buy organic groceries'" or "Update the description of task 3" and the AI uses the `update_task` tool.

**Why this priority**: Nice-to-have for task refinement. Less critical than CRUD basics.

**Independent Test**: Can be tested by creating a task, calling `update_task` with new values, and verifying the database reflects changes.

**Acceptance Scenarios**:

1. **Given** a task owned by the user, **When** the AI calls `update_task` with new title, **Then** the title is updated and returns `{"task_id": <int>, "status": "updated", "title": "<new title>"}`
2. **Given** a task owned by the user, **When** the AI calls `update_task` with new description only, **Then** only description changes, title remains
3. **Given** a task_id that doesn't exist, **When** the AI calls `update_task`, **Then** an error message "Task not found or not owned" is returned
4. **Given** a task owned by User A, **When** User B calls `update_task` with User A's task_id, **Then** User B gets "Task not found or not owned" error

---

### Edge Cases

- What happens when `list_tasks` is called with an invalid status filter (e.g., "invalid")? System returns an error or treats as "all".
- What happens when `add_task` receives an empty string title? System rejects with validation error.
- What happens when `update_task` is called with no fields to update? System returns the task unchanged or error.
- What happens when database is unavailable? Tools return appropriate error messages, not crash.

---

## Requirements *(mandatory)*

### Functional Requirements

**Tool Definitions**

- **FR-001**: System MUST expose exactly 5 MCP tools: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- **FR-002**: All tools MUST accept `user_id` as a required string parameter
- **FR-003**: Tools MUST be registered with the MCP SDK with proper JSON schemas

**add_task Tool**

- **FR-004**: `add_task` MUST accept parameters: `user_id` (str, required), `title` (str, required), `description` (str, optional)
- **FR-005**: `add_task` MUST return `{"task_id": int, "status": "created", "title": str}` on success
- **FR-006**: `add_task` MUST reject requests with empty or missing title

**list_tasks Tool**

- **FR-007**: `list_tasks` MUST accept parameters: `user_id` (str, required), `status` (str, optional: "all"|"pending"|"completed", default "all")
- **FR-008**: `list_tasks` MUST return an array of task objects (full task details)
- **FR-009**: `list_tasks` MUST filter by completion status when status parameter is provided

**complete_task Tool**

- **FR-010**: `complete_task` MUST accept parameters: `user_id` (str, required), `task_id` (int, required)
- **FR-011**: `complete_task` MUST mark the task as completed (set completed=true)
- **FR-012**: `complete_task` MUST return `{"task_id": int, "status": "completed", "title": str}` on success

**delete_task Tool**

- **FR-013**: `delete_task` MUST accept parameters: `user_id` (str, required), `task_id` (int, required)
- **FR-014**: `delete_task` MUST permanently remove the task from the database
- **FR-015**: `delete_task` MUST return `{"task_id": int, "status": "deleted", "title": str}` on success

**update_task Tool**

- **FR-016**: `update_task` MUST accept parameters: `user_id` (str, required), `task_id` (int, required), `title` (str, optional), `description` (str, optional)
- **FR-017**: `update_task` MUST update only provided fields, preserving others
- **FR-018**: `update_task` MUST return `{"task_id": int, "status": "updated", "title": str}` on success

**User Isolation**

- **FR-019**: All tools MUST filter/modify only tasks where `task.user_id == provided user_id`
- **FR-020**: Unauthorized access (wrong user_id) MUST return "Task not found or not owned" error
- **FR-021**: Tools MUST NOT expose tasks belonging to other users in any response

**Stateless Operation**

- **FR-022**: Tools MUST NOT maintain any in-memory state between calls
- **FR-023**: All data MUST be read from and written to the database on each call

**Error Handling**

- **FR-024**: Tools MUST return dict responses (not raise HTTP exceptions) with error messages
- **FR-025**: Non-existent task_id MUST result in "Task not found or not owned" message
- **FR-026**: Invalid parameters MUST result in descriptive error messages

### Key Entities

- **Task**: Existing Phase II model. Key attributes: id (int), user_id (str), title (str), description (str, nullable), completed (bool), created_at, updated_at. No new entities needed.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 MCP tools are implemented and callable through the MCP SDK
- **SC-002**: Each tool returns responses in the exact specified format (verified by integration tests)
- **SC-003**: User isolation is enforced: User A cannot read, modify, or delete User B's tasks (0% cross-user data leakage)
- **SC-004**: Tools handle at least 100 tasks per user without performance degradation
- **SC-005**: Error responses are clear and actionable (contain error type and guidance)
- **SC-006**: All 5 tools pass integration tests covering success paths, user isolation, and edge cases
- **SC-007**: Tools are stateless: calling same operation twice produces consistent results based only on database state

---

## Out of Scope

- OpenAI Agents SDK integration (Spec 3)
- Agent system prompt and behavior (Spec 3)
- /api/chat endpoint (Spec 4)
- Frontend ChatKit integration (Spec 4)
- Conversation/Message models (Spec 1 - already implemented)
- Pagination, sorting, or advanced filtering in list_tasks
- Custom HTTP status codes (tools return dict with status message)
- Authentication middleware changes (reuse Phase II)

---

## Assumptions

- Phase II database connection and Task model are functional and available
- MCP SDK is available and can be integrated with the existing FastAPI backend
- user_id will be passed to tools by the agent (derived from JWT in Spec 3/4)
- Standard MCP tool registration patterns will be followed

---

## Dependencies

- Phase II: Task model, database connection (DATABASE_URL), User model
- Phase III - Spec 1: Not a dependency (conversation/message is separate)
- MCP SDK: Official MCP SDK for Python

---

## Deliverables

1. MCP tool implementations in `backend/app/tools/` directory
2. MCP server registration/mounting code
3. Tool schema documentation at `specs/api/mcp-tools.md`
4. Integration tests at `backend/tests/test_mcp_tools.py`
