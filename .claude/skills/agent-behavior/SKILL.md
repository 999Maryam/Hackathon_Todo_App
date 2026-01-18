# Agent Behavior Patterns: AI Agent & Chat Logic

## Overview

This document describes the behavior patterns and interaction models for the AI-powered Todo Assistant. The agent is designed to understand natural language requests and perform task management operations using the available tools.

## Core Capabilities

### 1. Add Tasks
- **Intent Recognition**: "Add a task to buy groceries", "I need to call mom", "Create a task for walking the dog"
- **Tool Used**: `add_task(title, description?)`
- **Response Pattern**: "Got it! I've added 'Buy groceries' to your tasks."

### 2. List Tasks
- **Intent Recognition**: "What are my tasks?", "Show me pending tasks", "What have I completed?"
- **Tool Used**: `list_tasks(status=all|pending|completed)`
- **Response Pattern**: "Here are your tasks: [formatted list]"

### 3. Complete Tasks
- **Intent Recognition**: "Mark task 5 as done", "Complete task 3", "I finished the groceries task"
- **Tool Used**: `complete_task(task_id)`
- **Response Pattern**: "I've marked 'Buy groceries' as completed."

### 4. Delete Tasks
- **Intent Recognition**: "Delete task 3", "Remove the groceries task", "Cancel task 1"
- **Tool Used**: `delete_task(task_id)`
- **Response Pattern**: "I've deleted the task 'Buy groceries'."

### 5. Update Tasks
- **Intent Recognition**: "Change task 5 title to Buy organic groceries", "Update task 3 description to urgent"
- **Tool Used**: `update_task(task_id, title?, description?)`
- **Response Pattern**: "I've updated task 5 to 'Buy organic groceries'."

## Error Handling Patterns

### 1. Missing Tasks
- **Input**: "Mark task 999 as done" (non-existent task)
- **Response**: "I couldn't find that task. Please check the task number and try again."

### 2. Ambiguous Requests
- **Input**: "Do the thing"
- **Response**: "I'm not sure what you'd like me to do. Could you please be more specific about the task you want to manage?"

### 3. Permission Issues
- **Input**: Attempt to access another user's tasks
- **Response**: The system maintains strict user isolation, so this shouldn't occur within the agent's scope.

## Conversation Flow Patterns

### 1. Multi-step Operations
- **Input**: "Show me my tasks and delete task 3"
- **Flow**: `list_tasks()` → `delete_task()`
- **Response**: Combined response showing remaining tasks after deletion

### 2. Contextual Understanding
- **Input**: "Mark the groceries task as done" (when multiple tasks exist)
- **Flow**: May require disambiguation or smart matching based on recent context

## User Experience Guidelines

### 1. Friendly Responses
- Always acknowledge user requests
- Provide clear confirmation of actions taken
- Use natural, conversational language

### 2. Helpful Feedback
- When tasks don't exist, suggest alternatives
- When requests are unclear, ask for clarification
- Provide helpful error messages instead of technical jargon

### 3. Consistent Formatting
- Task lists should be easy to read
- Confirmation messages should be clear and specific
- Error messages should guide users toward resolution

## Technical Implementation Notes

### 1. Tool Calling
- The agent uses function calling to invoke backend tools
- All tools receive user context (user_id, db session) via context injection
- Tool responses are formatted as structured data for reliable parsing

### 2. Conversation State
- Each conversation maintains its own context
- History is loaded for continuity but user isolation is maintained
- No server-side state is preserved between requests

### 3. User Isolation
- Strict enforcement that users can only access their own tasks
- All database queries include user_id filters
- Access violations result in appropriate error responses