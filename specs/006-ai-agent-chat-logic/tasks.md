# Implementation Tasks: AI Agent & Chat Logic

**Feature**: 007-ai-agent-chat-logic
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md) | **Date**: 2026-01-15
**Input**: Feature specification with research, data model, contracts, and quickstart guide

---

## Overview

This document breaks down the AI Agent & Chat Logic feature into testable, actionable tasks. The implementation follows the Spec-Driven Development approach with the following phases:

- **Phase 1**: Setup (dependencies, directory structure)
- **Phase 2**: Foundational (core agent configuration)
- **Phase 3**: User Story 1 - Add Task via Natural Language (P1)
- **Phase 4**: User Story 2 - List Tasks via Natural Language (P1)
- **Phase 5**: User Story 3 - Complete Task via Natural Language (P1)
- **Phase 6**: User Story 4 - Delete Task via Natural Language (P2)
- **Phase 7**: User Story 5 - Update Task via Natural Language (P2)
- **Phase 8**: User Story 6 - Stateless Conversation Persistence (P1)
- **Phase 9**: User Story 7 - Tool Chaining for Complex Requests (P2)
- **Phase 10**: User Story 8 - Graceful Error Handling (P1)
- **Phase 11**: Polish & Cross-Cutting Concerns

Each user story represents a complete, independently testable increment of functionality.

---

## Phase 1: Setup

Goal: Prepare project infrastructure for agent implementation

- [X] T001 Install openai-agents dependency in backend requirements.txt
- [X] T002 Create agents directory structure: `backend/app/agents/` and `backend/app/agents/prompts/`
- [X] T003 Verify OPENAI_API_KEY environment variable is configured
- [X] T004 Confirm existing MCP tools from Spec 2 are available at `backend/app/tools/task_tools.py`

---

## Phase 2: Foundational

Goal: Establish core agent infrastructure and system prompt

- [X] T005 Create system prompt file at `backend/app/agents/prompts/system_prompt.txt` with behavior rules
- [X] T006 Note: Use Google Gemini API (free tier) instead of OpenAI Agents SDK. Install google-generativeai and   configure GEMINI_API_KEY. Replace OpenAI runner with Gemini function calling.
- [X] T006 Implement agent configuration in `backend/app/agents/openai_agent.py` with model and tools
- [X] T007 Create Pydantic models for AgentResponse and ToolCallRecord in `backend/app/agents/models.py`
- [X] T008 Set up agent context injection mechanism to pass user_id and db to tools

---

## Phase 3: [US1] Add Task via Natural Language (P1)

Goal: Enable users to add tasks through natural language commands

Independent Test: Send "Add a task to buy groceries" message to agent, verify add_task tool is called with correct parameters and response contains confirmation.

- [X] T009 [P] Create add_task wrapper tool that injects user_id context in `backend/app/agents/openai_agent.py`
- [X] T010 [P] [US1] Test that "Add a task to buy groceries" triggers add_task with title "buy groceries"
- [X] T011 [P] [US1] Test that "I need to call mom" triggers add_task with title "call mom"
- [X] T012 [P] [US1] Test that "Add buy milk and eggs to my list" triggers add_task appropriately
- [X] T013 [US1] Verify agent returns friendly confirmation messages like "Got it! I've added..."
- "Groceries khareedne ka task add kar do" → add_task
- "Pending tasks dikhao" → list_tasks(status="pending")
---

## Phase 4: [US2] List Tasks via Natural Language (P1)

Goal: Enable users to view their tasks through natural language commands

Independent Test: Create tasks for user, send "What are my tasks?" message, verify list_tasks is called and response includes task summaries.

- [X] T014 [P] Create list_tasks wrapper tool that injects user_id context in `backend/app/agents/openai_agent.py`
- [X] T015 [P] [US2] Test that "What are my tasks?" triggers list_tasks with status "all"
- [X] T016 [P] [US2] Test that "Show me pending tasks" triggers list_tasks with status "pending"
- [X] T017 [P] [US2] Test that "What have I completed?" triggers list_tasks with status "completed"
- [X] T018 [P] [US2] Test that "What are my tasks?" with no tasks returns helpful message
- [X] T019 [US2] Verify agent returns formatted task lists in readable format

---

## Phase 5: [US3] Complete Task via Natural Language (P1)

Goal: Enable users to mark tasks as complete through natural language commands

Independent Test: Create incomplete task, send completion message, verify complete_task called with correct task_id and success response returned.

- [X] T020 [P] Create complete_task wrapper tool that injects user_id context in `backend/app/agents/openai_agent.py`
- [X] T021 [P] [US3] Test that "Mark task 5 as done" triggers complete_task with task_id 5
- [X] T022 [P] [US3] Test that "I finished the groceries task" first calls list_tasks then complete_task with correct task_id
- [X] T023 [P] [US3] Test that referencing non-existent task returns polite error message
- [X] T024 [US3] Verify agent returns friendly completion confirmation messages

---

## Phase 6: [US4] Delete Task via Natural Language (P2)

Goal: Enable users to delete tasks through natural language commands

Independent Test: Create task, send delete message, verify delete_task called and task is removed.

- [X] T025 [P] Create delete_task wrapper tool that injects user_id context in `backend/app/agents/openai_agent.py`
- [X] T026 [P] [US4] Test that "Delete task 3" triggers delete_task with task_id 3
- [X] T027 [P] [US4] Test that "Remove the groceries task" finds task by title and calls delete_task
- [X] T028 [P] [US4] Test that deleting non-existent task returns polite error message
- [X] T029 [US4] Verify agent returns confirmation that task was removed

---

## Phase 7: [US5] Update Task via Natural Language (P2)

Goal: Enable users to update task details through natural language commands

Independent Test: Create task, send update message, verify update_task called with correct parameters.

- [X] T030 [P] Create update_task wrapper tool that injects user_id context in `backend/app/agents/openai_agent.py`
- [X] T031 [P] [US5] Test that "Change task 5 title to Buy organic groceries" triggers update_task with correct parameters
- [X] T032 [P] [US5] Test that "Update task 3 description to urgent" triggers update_task with new description
- [X] T033 [US5] Verify agent returns confirmation of task update

---

## Phase 8: [US6] Stateless Conversation Persistence (P1)

Goal: Implement stateless conversation cycle with full context loading

Independent Test: Send sequential messages in separate requests and verify agent remembers previous context.

- [X] T034 [P] Implement conversation history loading from database in `backend/app/agents/chat_runner.py`
- [X] T035 [P] Implement conversation history conversion to OpenAI message format
- [X] T036 [P] [US6] Test that user message and assistant response are saved to database
- [X] T037 [P] [US6] Test that previous messages are loaded and included in agent context
- [X] T038 [P] [US6] Test that conversation context persists across server restarts.Test that wrong user_id returns empty history or error (strict isolation)
- [X] T039 [P] [US6] Test that new conversation is created when conversation_id is not provided
- [X] T040 [US6] Verify runner is fully stateless with no in-memory storage between requests

---

## Phase 9: [US7] Tool Chaining for Complex Requests (P2)

Goal: Enable agent to chain multiple tools for complex user requests

Independent Test: Send multi-step request and verify multiple tools are called in sequence.

- [X] T041 [P] [US7] Test that "Show me my tasks and delete task 3" calls list_tasks then delete_task
- [X] T042 [P] [US7] Test that "Add buy eggs and show my list" calls add_task then list_tasks
- [X] T043 [US7] Verify agent provides combined response for chained operations

---

## Phase 10: [US8] Graceful Error Handling (P1)

Goal: Ensure agent responds with friendly, helpful messages for error scenarios

Independent Test: Send requests that trigger errors and verify responses are user-friendly.

- [X] T044 [P] [US8] Test that "Complete task 99999" (non-existent) returns helpful message
- [X] T045 [P] [US8] Test that ambiguous message "Do the thing" results in clarification request
- [X] T046 [P] [US8] Test that tool errors are translated to user-friendly messages
- [X] T047 [US8] Implement error handling in system prompt to guide agent behavior
- [X] T048 [US8] Verify no technical failure details are exposed to users

---

## Phase 11: Polish & Cross-Cutting Concerns

Goal: Complete implementation with testing and documentation

- [X] T049 Create comprehensive test suite in `backend/tests/test_agent.py` covering all user stories
- [X] T050 Add integration tests for conversation persistence and user isolation
- [X] T051 Document agent behavior patterns in `specs/007-ai-agent-chat-logic/agent-behavior.md`
- [X] T052 Optimize agent response time and performance
- [X] T053 Verify all 5 MCP tools can be successfully invoked through natural language
- [X] T054 Run full test suite to verify all acceptance criteria are met
- [X] T055 Update requirements.txt with openai-agents version constraint
- [X] T056 Verify agent can chain tools in single response (e.g., list → delete)
---

## Dependencies

**User Story Completion Order:**
- US6 (Persistence) must be implemented before other stories for full functionality
- US1, US2, US3 (Core CRUD) should be completed before US4, US5 (Less frequent operations)
- US8 (Error Handling) should be implemented throughout, not just at end

**Parallel Execution Opportunities:**
- Individual tool wrappers (T009, T014, T020, T025, T030) can be developed in parallel
- Individual user story tests (T010-T013, T015-T019, T021-T024, etc.) can be developed in parallel
- Agent configuration (T005-T008) can be developed in parallel with conversation persistence (T034-T040)

---

## Implementation Strategy

**MVP Scope (Core Deliverable)**  
T001–T013: Basic agent setup + Add Task via natural language  
→ Enables first working AI feature: "Add task via chat"

**Incremental Delivery:** Each user story builds upon the foundational agent infrastructure, with conversation persistence (US6) as a prerequisite for complete functionality.

**Testing Approach:** Each user story includes acceptance scenario tests that can be run independently to verify functionality before moving to next story.
