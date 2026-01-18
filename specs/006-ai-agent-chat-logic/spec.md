# Feature Specification: AI Agent & Chat Logic for Todo AI Chatbot

**Feature Branch**: `007-ai-agent-chat-logic`
**Created**: 2026-01-14
**Status**: Draft
**Phase**: III - Spec 3 of 4
**Input**: User description: "AI Agent & Chat Logic for Todo AI Chatbot (Phase III - Spec 3)"

---

## Overview

This specification defines the core AI intelligence layer for the Todo AI Chatbot. The agent interprets natural language user messages, selects appropriate MCP tools to manage tasks, and returns friendly, confirmatory responses. The agent operates statelessly, loading full conversation context from the database on each request.

**Context**: This is Phase III - Spec 3 of the Todo AI Chatbot project. It builds on:
- Phase II: JWT authentication (current_user), existing Task model
- Phase III - Spec 1: Conversation/Message persistence layer (CRUD helpers)
- Phase III - Spec 2: MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

**Scope**: Agent configuration, behavior rules, and stateless conversation cycle. Does NOT include:
- Database models (Spec 1 - already implemented)
- MCP tools (Spec 2 - already implemented)
- Chat API endpoint /api/chat (Spec 4)
- Frontend ChatKit integration (Spec 4)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task via Natural Language (Priority: P1)

A user sends a chat message like "Add a task to buy groceries" and the AI agent interprets this intent, calls the `add_task` tool, and responds with a friendly confirmation like "Got it! I've added 'buy groceries' to your tasks."

**Why this priority**: Task creation through natural language is the primary value proposition. Users expect to create tasks by simply typing what they want.

**Independent Test**: Can be tested by sending a task creation message to the agent runner, verifying the correct tool was called, and confirming the response contains confirmation language.

**Acceptance Scenarios**:

1. **Given** a user message "Add a task to buy groceries", **When** the agent processes it, **Then** the agent calls `add_task` with title "buy groceries" and returns a confirmation message containing the task title.
2. **Given** a user message "I need to call mom tomorrow", **When** the agent processes it, **Then** the agent calls `add_task` with title "call mom tomorrow" and confirms the addition.
3. **Given** a user message "Add buy milk and eggs to my list", **When** the agent processes it, **Then** the agent calls `add_task` with appropriate title and confirms.

---

### User Story 2 - List Tasks via Natural Language (Priority: P1)

A user sends a chat message like "What are my tasks?" or "Show me my pending tasks" and the AI agent calls `list_tasks` and presents the results in a readable, friendly format.

**Why this priority**: Users need to see their tasks to know what to work on. This is the core read operation that enables all task management.

**Independent Test**: Can be tested by creating tasks for a user, sending a list request message, verifying `list_tasks` was called, and confirming the response includes task summaries.

**Acceptance Scenarios**:

1. **Given** a user with 3 tasks asks "What are my tasks?", **When** the agent processes it, **Then** the agent calls `list_tasks` and returns a formatted list of all tasks.
2. **Given** a user asks "Show me pending tasks", **When** the agent processes it, **Then** the agent calls `list_tasks` with status "pending" and returns only incomplete tasks.
3. **Given** a user asks "What have I completed?", **When** the agent processes it, **Then** the agent calls `list_tasks` with status "completed" and returns completed tasks.
4. **Given** a user with no tasks asks "What are my tasks?", **When** the agent processes it, **Then** the agent responds that there are no tasks yet with a helpful suggestion.

---

### User Story 3 - Complete Task via Natural Language (Priority: P1)

A user sends a chat message like "Mark task 5 as done" or "I finished buying groceries" and the AI agent identifies the task and marks it complete.

**Why this priority**: Completing tasks is the core workflow outcome. Users create tasks to eventually mark them done.

**Independent Test**: Can be tested by creating an incomplete task, sending a completion message, verifying `complete_task` was called with correct task_id, and confirming the success response.

**Acceptance Scenarios**:

1. **Given** a user says "Mark task 5 as done", **When** the agent processes it, **Then** the agent calls `complete_task` with task_id 5 and confirms completion.
2. **Given** a user says "I finished the groceries task", **When** the agent processes it, **Then** the agent first calls `list_tasks` to find the task, then calls `complete_task` with the correct task_id.
3. **Given** a user references a non-existent task, **When** the agent processes it, **Then** the agent returns a polite message indicating the task was not found.

---

### User Story 4 - Delete Task via Natural Language (Priority: P2)

A user sends a chat message like "Delete task 3" or "Remove the groceries task" and the AI agent deletes the specified task.

**Why this priority**: Task deletion is important but less frequent than add/list/complete.

**Independent Test**: Can be tested by creating a task, sending a delete message, verifying `delete_task` was called, and confirming the task is removed.

**Acceptance Scenarios**:

1. **Given** a user says "Delete task 3", **When** the agent processes it, **Then** the agent calls `delete_task` with task_id 3 and confirms deletion.
2. **Given** a user says "Remove the call mom task", **When** the agent processes it, **Then** the agent finds the task by title, calls `delete_task`, and confirms.
3. **Given** a user tries to delete a non-existent task, **When** the agent processes it, **Then** the agent responds politely that the task was not found.

---

### User Story 5 - Update Task via Natural Language (Priority: P2)

A user sends a chat message like "Change task 5 title to 'Buy organic groceries'" and the AI agent updates the task.

**Why this priority**: Task updates are useful for refinement but less critical than core CRUD.

**Independent Test**: Can be tested by creating a task, sending an update message, verifying `update_task` was called with correct parameters.

**Acceptance Scenarios**:

1. **Given** a user says "Change task 5 title to Buy organic groceries", **When** the agent processes it, **Then** the agent calls `update_task` with task_id 5 and new title.
2. **Given** a user says "Update task 3 description to urgent", **When** the agent processes it, **Then** the agent calls `update_task` with task_id 3 and new description.

---

### User Story 6 - Stateless Conversation Persistence (Priority: P1)

When a user sends a message, the system loads their full conversation history from the database, processes the new message with full context, and saves both the user message and assistant response back to the database.

**Why this priority**: Stateless operation is fundamental to the architecture. Without it, the agent cannot maintain context across requests.

**Independent Test**: Can be tested by sending sequential messages in separate requests and verifying the agent remembers previous context.

**Acceptance Scenarios**:

1. **Given** a user sends "Add a task to buy milk", **When** the response is generated, **Then** both the user message and assistant response are saved to the database with correct conversation_id.
2. **Given** a user with 5 previous messages sends a new message, **When** the agent processes it, **Then** all 5 previous messages are loaded and included in the agent context.
3. **Given** a server restart between messages, **When** the user sends a follow-up message, **Then** the agent responds with full context of previous conversation.

---

### User Story 7 - Tool Chaining for Complex Requests (Priority: P2)

A user sends a complex request like "What tasks do I have? Then delete the completed ones" and the agent chains multiple tool calls to fulfill the request.

**Why this priority**: Advanced capability that improves user experience but not required for basic functionality.

**Independent Test**: Can be tested by sending a multi-step request and verifying multiple tools are called in sequence.

**Acceptance Scenarios**:

1. **Given** a user says "Show me my tasks and delete task 3", **When** the agent processes it, **Then** the agent calls `list_tasks` then `delete_task` and provides a combined response.
2. **Given** a user says "Add buy eggs and show my list", **When** the agent processes it, **Then** the agent calls `add_task` then `list_tasks` and responds with both results.

---

### User Story 8 - Graceful Error Handling (Priority: P1)

When the agent encounters errors (invalid task ID, database issues, malformed requests), it responds with friendly, helpful error messages rather than technical failures.

**Why this priority**: Error handling is critical for user experience. Technical failures frustrate users.

**Independent Test**: Can be tested by sending requests that trigger errors and verifying responses are user-friendly.

**Acceptance Scenarios**:

1. **Given** a user says "Complete task 99999" (non-existent), **When** the agent processes it, **Then** the agent responds "I couldn't find a task with that ID. Would you like to see your task list?"
2. **Given** a user sends an ambiguous message like "Do the thing", **When** the agent processes it, **Then** the agent asks for clarification politely.
3. **Given** a tool returns an error, **When** the agent processes the error, **Then** the agent translates it into a helpful user message.

---

### Edge Cases

- What happens when the user sends an empty message? Agent responds asking how it can help.
- What happens when the user sends a very long message? Agent processes normally (truncation handled by model limits).
- What happens when the user sends non-English text? Agent attempts to understand and respond in kind.
- What happens when multiple tool calls fail? Agent reports each failure gracefully.
- What happens when conversation history is extremely long? Agent processes with full context (model handles truncation).
- What happens when user_id is missing or invalid? Agent runner rejects with authentication error before processing.

---

## Requirements *(mandatory)*

### Functional Requirements

**Agent Configuration**

- **FR-001**: System MUST configure an agent using OpenAI Agents SDK with model "gpt-4o-mini" (or configurable via environment)
- **FR-002**: Agent MUST be configured with all 5 MCP tools from Spec 2 (add_task, list_tasks, complete_task, delete_task, update_task)
- **FR-003**: Agent MUST have a system prompt that defines behavior rules, tone, and tool selection guidance
- **FR-004**: Agent configuration MUST be reusable across requests (singleton or factory pattern)

**System Prompt Behavior Rules**

- **FR-005**: System prompt MUST instruct agent to always confirm actions with friendly language (e.g., "Got it!", "Done!", "Here are your tasks:")
- **FR-006**: System prompt MUST define when to call each tool based on user intent keywords:
  - add/create/new/remind → add_task
  - list/show/what/display → list_tasks
  - complete/done/finish/mark → complete_task
  - delete/remove/cancel → delete_task
  - update/change/edit/rename → update_task
- **FR-007**: System prompt MUST instruct agent to ask for clarification when intent is ambiguous
- **FR-008**: System prompt MUST instruct agent to handle errors gracefully with user-friendly messages
- **FR-009**: System prompt MUST instruct agent to chain tools when request requires multiple operations

**Stateless Conversation Cycle**

- **FR-010**: System MUST implement a runner function that executes the full stateless cycle:
  1. Accept user_id, conversation_id (optional), and message content as input
  2. Load full conversation history from database (using Spec 1 helpers)
  3. Append new user message to history
  4. Run agent with conversation history and available tools
  5. Execute any tool calls returned by agent, passing user_id to each
  6. Save user message to database (using Spec 1 helpers)
  7. Save assistant response to database (using Spec 1 helpers)
  8. Return response text and array of tool calls made
- **FR-011**: Runner MUST create a new conversation if conversation_id is not provided (using Spec 1 get_or_create)
- **FR-012**: Runner MUST NOT store any state in memory between requests (fully stateless)
- **FR-013**: Runner MUST pass user_id to all tool calls for ownership enforcement

**Message Format Conversion**

- **FR-014**: System MUST convert database Message records to OpenAI message format for agent input
- **FR-015**: System MUST convert agent output to database Message format for persistence
- **FR-016**: Tool call results MUST be included in conversation history for context

**Response Format**

- **FR-017**: Runner MUST return a structured response containing:
  - `content`: The assistant's text response
  - `tool_calls`: Array of tool calls made (name, arguments, result)
  - `conversation_id`: The conversation ID used
- **FR-018**: Responses MUST be concise, friendly, and action-oriented
- **FR-019**: When listing tasks, response MUST format tasks in a readable way (numbered list or summary)

**Error Handling**

- **FR-020**: Runner MUST catch tool execution errors and include them in agent context for graceful handling
- **FR-021**: Runner MUST handle missing/invalid user_id by raising appropriate authentication error
- **FR-022**: Runner MUST handle database connection failures gracefully
- **FR-023**: Agent MUST NOT expose internal error details to users (translate to friendly messages)

**Integration with Existing Systems**

- **FR-024**: Runner MUST use conversation/message helpers from Spec 1 for all persistence
- **FR-025**: Runner MUST use MCP tools from Spec 2 for all task operations
- **FR-026**: OPENAI_API_KEY MUST be loaded from environment variables

### Key Entities

- **Agent**: The configured AI agent instance. Not a database entity - exists only in runtime. Configured with model, tools, and system prompt.

- **AgentRunner**: The stateless function that executes the conversation cycle. Not a database entity - a pure function that orchestrates loading, processing, and saving.

- **Conversation**: Existing entity from Spec 1. Contains conversation metadata and links messages.

- **Message**: Existing entity from Spec 1. Stores individual messages with role (user/assistant) and content.

- **Tool Call**: Runtime data structure representing a tool invocation. Contains tool name, arguments passed, and result returned. Logged in response but not separately persisted.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Agent correctly identifies user intent and selects appropriate tool for at least 90% of standard task commands (add, list, complete, delete, update)

- **SC-002**: All responses include friendly confirmation language - no technical jargon in user-facing messages

- **SC-003**: Conversation context is fully preserved across server restarts - verified by sending follow-up messages after restart

- **SC-004**: User A cannot trigger tools that affect User B's tasks - verified by multi-user isolation tests

- **SC-005**: Agent handles ambiguous requests by asking clarifying questions rather than guessing incorrectly

- **SC-006**: Error scenarios (invalid task ID, database errors) result in helpful user messages, not technical failures

- **SC-007**: Tool chaining works for multi-step requests - verified by "list then delete" type commands

- **SC-008**: Agent response time for typical requests is under 3 seconds (excluding network latency)

- **SC-009**: All 5 MCP tools can be successfully invoked through natural language commands

- **SC-010**: Test suite passes with coverage of: intent detection, tool selection, conversation persistence, user isolation, error handling

---

## Out of Scope

- MCP tools implementation (Spec 2 - already implemented)
- Conversation/Message database models (Spec 1 - already implemented)
- /api/chat endpoint (Spec 4)
- Frontend ChatKit integration (Spec 4)
- Voice input processing
- Multi-language support (respond in user's language is acceptable, but no translation features)
- Reminder/scheduling features
- Recurring task patterns
- Advanced agent memory or context summarization
- Custom tool schemas (use MCP SDK defaults)
- Conversation threading or branching
- Message editing or deletion by users

---

## Assumptions

- OpenAI API is accessible and OPENAI_API_KEY is configured in environment
- OpenAI Agents SDK is compatible with the configured model (gpt-4o-mini or similar)
- Spec 1 conversation/message helpers are functional and tested
- Spec 2 MCP tools are functional and return expected response formats
- JWT authentication from Phase II provides valid user_id
- Database connection from Phase II is stable
- Single conversation per user is sufficient (no need for multiple parallel conversations)

---

## Dependencies

- **Phase II**: JWT authentication (user_id extraction), Database connection
- **Phase III - Spec 1**: Conversation/Message models and CRUD helpers
- **Phase III - Spec 2**: MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **External**: OpenAI API, OpenAI Agents SDK

---

## Deliverables

1. **Agent Setup Code**: `backend/app/agents/openai_agent.py`
   - Agent configuration with model and tools
   - System prompt definition
   - Tool binding setup

2. **Stateless Runner Function**: `backend/app/agents/chat_runner.py` (or in same file)
   - `run_agent_with_tools(user_id, message, conversation_id=None) -> AgentResponse`
   - Full conversation cycle implementation
   - Message format conversion utilities

3. **System Prompt**: In code or `backend/app/agents/prompts/system_prompt.txt`
   - Behavior rules for tool selection
   - Tone and response style guidelines
   - Error handling instructions

4. **Pytest Tests**: `backend/tests/test_agent.py`
   - Test correct tool selection for sample commands
   - Test conversation persistence across requests
   - Test user isolation (wrong user_id returns empty history)
   - Test error recovery (invalid task_id produces polite message)
   - Test tool chaining for multi-step requests

5. **Behavior Documentation**: `specs/007-ai-agent-chat-logic/agent-behavior.md`
   - Intent-to-tool mapping examples
   - Sample conversations with expected tool calls
   - Error handling examples

---

## Natural Language Examples

The following examples illustrate expected agent behavior:

### Task Addition
| User Message | Expected Tool | Expected Response Pattern |
|--------------|---------------|---------------------------|
| "Add a task to buy groceries" | add_task(title="buy groceries") | "Got it! I've added 'buy groceries' to your tasks." |
| "I need to call mom" | add_task(title="call mom") | "Done! 'call mom' has been added to your list." |
| "Remind me to pay bills" | add_task(title="pay bills") | "Added! 'pay bills' is now on your task list." |

### Task Listing
| User Message | Expected Tool | Expected Response Pattern |
|--------------|---------------|---------------------------|
| "What are my tasks?" | list_tasks(status="all") | "Here are your tasks: 1. Buy groceries 2. Call mom..." |
| "Show pending tasks" | list_tasks(status="pending") | "You have 3 pending tasks: 1. ..." |
| "What have I completed?" | list_tasks(status="completed") | "Great progress! You've completed: 1. ..." |

### Task Completion
| User Message | Expected Tool | Expected Response Pattern |
|--------------|---------------|---------------------------|
| "Mark task 5 as done" | complete_task(task_id=5) | "Nice work! Task 5 is now complete." |
| "I finished the groceries" | list_tasks → complete_task | "Great! I've marked 'buy groceries' as done." |

### Task Deletion
| User Message | Expected Tool | Expected Response Pattern |
|--------------|---------------|---------------------------|
| "Delete task 3" | delete_task(task_id=3) | "Done! Task 3 has been removed." |
| "Remove the call mom task" | list_tasks → delete_task | "Removed! 'call mom' is no longer on your list." |

### Task Update
| User Message | Expected Tool | Expected Response Pattern |
|--------------|---------------|---------------------------|
| "Change task 5 to 'Buy organic groceries'" | update_task(task_id=5, title="Buy organic groceries") | "Updated! Task 5 is now 'Buy organic groceries'." |

### Error Handling
| User Message | Scenario | Expected Response Pattern |
|--------------|----------|---------------------------|
| "Complete task 99999" | Task not found | "I couldn't find that task. Want me to show your task list?" |
| "Do the thing" | Ambiguous | "I'm not sure what you'd like me to do. Would you like to add a task, see your list, or something else?" |
