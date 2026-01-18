# Research: AI Agent & Chat Logic

**Feature**: 007-ai-agent-chat-logic
**Date**: 2026-01-14
**Status**: Complete

---

## Research Questions

### Q1: How to integrate OpenAI Agents SDK with existing MCP tools?

**Findings**: The OpenAI Agents SDK provides a `@function_tool` decorator that wraps Python functions and auto-generates JSON schemas from type hints and docstrings.

**Key Code Pattern**:
```python
from agents import Agent, Runner, function_tool

@function_tool
def add_task(title: str, description: str | None = None) -> dict:
    """Add a new task to your list.

    Args:
        title: The title of the task to add
        description: Optional description for the task
    """
    # Implementation
    return {"task_id": 1, "status": "created", "title": title}

agent = Agent(
    name="Task Assistant",
    instructions="You help manage todo tasks.",
    tools=[add_task, list_tasks, complete_task, delete_task, update_task],
    model="gpt-4o-mini"
)
```

**Decision**: Use `@function_tool` decorator to wrap existing `task_tools.py` functions.

---

### Q2: How to manage conversation history without SQLiteSession?

**Findings**: The SDK supports custom session implementations. Since Spec 1 provides database-backed conversation helpers that return OpenAI-compatible format, we can load history directly and pass it to `Runner.run()`.

**Key Code Pattern**:
```python
from agents import Agent, Runner

# Load history from our DB (Spec 1 helper returns OpenAI format)
history = get_conversation_history(conversation_id, user_id, db)
# history = [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

# Run agent with history as input
result = await Runner.run(
    agent,
    input=user_message,
    context=history  # Previous messages for context
)
```

**Decision**: Use Spec 1 `get_conversation_history()` instead of SQLiteSession.

---

### Q3: How to inject user_id into tool calls?

**Findings**: The `@function_tool` decorator supports a `RunContextWrapper` parameter that can carry context data. We can store `user_id` and `db` session in this context.

**Key Code Pattern**:
```python
from agents import function_tool, RunContextWrapper
from typing import Any

@function_tool
def add_task(ctx: RunContextWrapper[Any], title: str) -> dict:
    """Add a task."""
    user_id = ctx.context.get("user_id")
    db = ctx.context.get("db")
    return task_tools.add_task(user_id, title, db=db)
```

**Decision**: Use `RunContextWrapper` to pass `user_id` and `db` to tool functions.

---

### Q4: How to handle tool execution errors?

**Findings**: The `@function_tool` decorator accepts a `failure_error_function` parameter that provides custom error handling. Tool functions can also return error dicts that the agent interprets.

**Key Code Pattern**:
```python
def tool_error_handler(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """Provide user-friendly error message."""
    return f"Sorry, I couldn't complete that action. {str(error)}"

@function_tool(failure_error_function=tool_error_handler)
def complete_task(task_id: int) -> dict:
    """Mark task as complete."""
    # Returns {"error": "Task not found"} if not found
```

**Decision**: Existing tools return error dicts; agent handles gracefully in response.

---

### Q5: What model configuration is optimal?

**Findings**: The SDK supports model configuration per-agent. Model can be specified as string name or `OpenAIChatCompletionsModel` instance.

**Key Code Pattern**:
```python
from agents import Agent

agent = Agent(
    name="Task Assistant",
    instructions="...",
    model="gpt-4o-mini",  # Cost-effective for task management
    tools=[...]
)
```

**Decision**: Use `gpt-4o-mini` as default, configurable via `OPENAI_MODEL` env var.

---

## SDK Installation

```bash
pip install openai-agents
```

Package provides:
- `Agent`: Configures agent with model, tools, instructions
- `Runner`: Executes agent with input and handles tool loops
- `function_tool`: Decorator to create tools from Python functions
- `RunContextWrapper`: Context object for passing data to tools

---

## Best Practices Identified

1. **Type hints are required**: All tool parameters must have type annotations
2. **Docstrings become descriptions**: Tool and parameter descriptions come from docstrings
3. **Return types matter**: Return `dict` or Pydantic models for structured output
4. **Async is supported**: Both sync and async tool functions work
5. **Context injection**: Use `RunContextWrapper` for shared state like user_id

---

## References

- OpenAI Agents SDK Docs: https://github.com/openai/openai-agents-python
- Function Tools Guide: https://github.com/openai/openai-agents-python/blob/main/docs/tools.md
- Running Agents: https://github.com/openai/openai-agents-python/blob/main/docs/running_agents.md
