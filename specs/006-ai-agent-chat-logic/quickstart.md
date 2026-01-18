# Quickstart: AI Agent & Chat Logic

**Feature**: 007-ai-agent-chat-logic
**Date**: 2026-01-14

---

## Prerequisites

Before implementing this feature, ensure:

1. **Phase II Complete**: JWT authentication working, Task model in database
2. **Spec 1 Complete**: Conversation/Message models and CRUD helpers
3. **Spec 2 Complete**: MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
4. **Environment**: `OPENAI_API_KEY` configured in `.env`

---

## Installation

Add the OpenAI Agents SDK to your dependencies:

```bash
cd backend
pip install openai-agents
```

Or add to `requirements.txt`:
```
openai-agents>=0.0.1
```

---

## Directory Setup

Create the agents directory structure:

```bash
mkdir -p backend/app/agents/prompts
touch backend/app/agents/__init__.py
touch backend/app/agents/openai_agent.py
touch backend/app/agents/chat_runner.py
touch backend/app/agents/prompts/system_prompt.txt
```

---

## Quick Implementation Guide

### Step 1: Create System Prompt

Create `backend/app/agents/prompts/system_prompt.txt`:

```
You are a helpful AI assistant for managing todo tasks...
[Full prompt from plan.md]
```

### Step 2: Configure Agent with Tools

Create `backend/app/agents/openai_agent.py`:

```python
"""OpenAI Agent configuration for Todo AI Chatbot.

Task: T001 | Spec: specs/007-ai-agent-chat-logic/spec.md#FR-001-FR-009
"""

import os
from pathlib import Path
from agents import Agent, function_tool, RunContextWrapper
from typing import Any

from app.tools import task_tools

# Load system prompt
PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"
SYSTEM_PROMPT = PROMPT_PATH.read_text()

# Model configuration
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


# Tool wrappers that inject user context
@function_tool
def add_task(ctx: RunContextWrapper[Any], title: str,
             description: str | None = None) -> dict:
    """Add a new task to your list."""
    return task_tools.add_task(
        user_id=ctx.context["user_id"],
        title=title,
        description=description,
        db=ctx.context["db"]
    )


@function_tool
def list_tasks(ctx: RunContextWrapper[Any], status: str = "all") -> dict:
    """List your tasks with optional filtering."""
    return task_tools.list_tasks(
        user_id=ctx.context["user_id"],
        status=status,
        db=ctx.context["db"]
    )


# ... similar wrappers for complete_task, delete_task, update_task


def create_agent() -> Agent:
    """Create configured agent instance."""
    return Agent(
        name="Todo Assistant",
        instructions=SYSTEM_PROMPT,
        model=MODEL,
        tools=[add_task, list_tasks, complete_task, delete_task, update_task]
    )
```

### Step 3: Implement Chat Runner

Create `backend/app/agents/chat_runner.py`:

```python
"""Stateless chat runner for Todo AI Chatbot.

Task: T002 | Spec: specs/007-ai-agent-chat-logic/spec.md#FR-010-FR-019
"""

from pydantic import BaseModel
from sqlmodel import Session
from agents import Runner

from app.agents.openai_agent import create_agent
from app.services.conversation_service import (
    get_or_create_conversation,
    get_conversation_history,
    add_user_message,
    add_assistant_message
)


class ToolCallRecord(BaseModel):
    name: str
    arguments: dict
    result: dict


class AgentResponse(BaseModel):
    content: str
    tool_calls: list[ToolCallRecord]
    conversation_id: int


async def run_agent_with_tools(
    user_id: str,
    message: str,
    conversation_id: int | None = None,
    db: Session = None
) -> AgentResponse:
    """Execute stateless conversation cycle."""

    # Validate user_id
    if not user_id or not user_id.strip():
        raise ValueError("user_id is required")

    # Get or create conversation
    conversation = get_or_create_conversation(user_id, db)
    conv_id = conversation.id

    # Load history
    history = get_conversation_history(conv_id, user_id, db)

    # Create agent with context
    agent = create_agent()
    context = {"user_id": user_id, "db": db}

    # Run agent
    result = await Runner.run(
        agent,
        input=message,
        context=context
        # History handled via context or input formatting
    )

    # Save messages
    add_user_message(conv_id, user_id, message, db)
    add_assistant_message(conv_id, user_id, result.final_output, db)

    # Extract tool calls from result
    tool_calls = [
        ToolCallRecord(
            name=tc.name,
            arguments=tc.arguments,
            result=tc.result
        )
        for tc in getattr(result, 'tool_calls', [])
    ]

    return AgentResponse(
        content=result.final_output,
        tool_calls=tool_calls,
        conversation_id=conv_id
    )
```

### Step 4: Test the Agent

Create `backend/tests/test_agent.py`:

```python
"""Tests for AI Agent behavior.

Task: T003 | Spec: specs/007-ai-agent-chat-logic/spec.md#SC-001-SC-010
"""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.chat_runner import run_agent_with_tools


@pytest.mark.asyncio
async def test_add_task_intent():
    """Test that add task message triggers add_task tool."""
    # Mock dependencies and run test
    pass


@pytest.mark.asyncio
async def test_list_tasks_intent():
    """Test that list message triggers list_tasks tool."""
    pass
```

---

## Environment Variables

Ensure these are set in `backend/.env`:

```env
# Required
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db

# Optional
OPENAI_MODEL=gpt-4o-mini
```

---

## Verification Checklist

After implementation, verify:

- [ ] Agent responds to "Add a task to buy groceries" with confirmation
- [ ] Agent responds to "What are my tasks?" with task list
- [ ] Agent responds to "Mark task 1 as done" with completion confirmation
- [ ] Conversation history persists across requests
- [ ] User A cannot see User B's tasks or conversations
- [ ] Invalid requests get friendly error messages

---

## Common Issues

### 1. "OPENAI_API_KEY not found"
Ensure `.env` file exists and contains valid API key.

### 2. "Tool not found in agent"
Check that all 5 tools are registered in `create_agent()`.

### 3. "Conversation not found"
Ensure Spec 1 database migrations have been run.

### 4. "User isolation failed"
Verify `user_id` is passed to all tool calls via context.

---

## Next Steps

After completing this spec:

1. Run `/sp.tasks` to generate actionable tasks
2. Implement tasks using `/sp.implement`
3. Move to Spec 4 to create `/api/chat` endpoint
