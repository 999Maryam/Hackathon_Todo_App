---
name: chat-response-formatter-skill
description: Format final responses for the /api/chat endpoint with clean output, tool call summaries, and user-friendly presentation.
version: 1.0.0
---

# Chat Response Formatter Skill

This skill formats the final response for the /api/chat endpoint.

## Purpose

Transforms raw agent output into a clean, user-friendly API response:
- Structures response as consistent JSON
- Cleans assistant messages of internal artifacts
- Summarizes tool calls for transparency
- Adds friendly tone when appropriate

## Input/Output Specification

### Input
- `agent_response`: Raw response from OpenAI agent
- `tool_calls`: List of tools invoked during processing
- `conversation_id`: Session identifier

### Output
```json
{
    "conversation_id": "uuid-string",
    "response": "Clean, user-friendly message",
    "tool_calls": [
        {"tool": "tool_name", "status": "success|error", "summary": "brief description"}
    ]
}
```

## Core Function

```python
from typing import Optional
import re

def format_chat_response(
    agent_response: str,
    tool_calls: Optional[list] = None,
    conversation_id: str = None
) -> dict:
    """
    Format the final response for /api/chat endpoint.

    Args:
        agent_response: Raw response from OpenAI agent
        tool_calls: List of tool invocations with results
        conversation_id: UUID of the conversation

    Returns:
        dict: Formatted API response

    Reference: Phase III Spec - Chat API Response Format
    """
    # Clean the assistant message
    cleaned_response = clean_assistant_message(agent_response)

    # Add friendly tone if message is too terse
    cleaned_response = add_friendly_tone(cleaned_response)

    # Format tool calls for transparency
    formatted_tools = format_tool_calls(tool_calls) if tool_calls else []

    return {
        "conversation_id": conversation_id,
        "response": cleaned_response,
        "tool_calls": formatted_tools
    }
```

## Helper Functions

### 1. clean_assistant_message

Removes internal artifacts and formatting issues.

```python
def clean_assistant_message(message: str) -> str:
    """
    Remove internal tool thoughts and clean up formatting.

    Args:
        message: Raw assistant message

    Returns:
        str: Cleaned message for user display
    """
    if not message:
        return ""

    cleaned = message

    # Remove internal thinking blocks
    # Pattern: <thinking>...</thinking> or [INTERNAL]...[/INTERNAL]
    cleaned = re.sub(r'<thinking>.*?</thinking>', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'\[INTERNAL\].*?\[/INTERNAL\]', '', cleaned, flags=re.DOTALL)

    # Remove tool call artifacts
    # Pattern: [Calling tool: ...] or {tool_call: ...}
    cleaned = re.sub(r'\[Calling tool:.*?\]', '', cleaned)
    cleaned = re.sub(r'\{tool_call:.*?\}', '', cleaned, flags=re.DOTALL)

    # Remove function call notation
    cleaned = re.sub(r'```function_call\n.*?```', '', cleaned, flags=re.DOTALL)

    # Remove debug markers
    cleaned = re.sub(r'\[DEBUG\].*?\n', '', cleaned)
    cleaned = re.sub(r'<!-- .* -->', '', cleaned)

    # Clean up whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)  # Max 2 newlines
    cleaned = cleaned.strip()

    return cleaned
```

### 2. add_friendly_tone

Enhances terse responses with friendly language.

```python
def add_friendly_tone(message: str) -> str:
    """
    Add friendly tone to terse or robotic responses.

    Args:
        message: Cleaned assistant message

    Returns:
        str: Message with improved tone
    """
    if not message:
        return "I'm here to help! What would you like to do?"

    # Check if message is very short/terse
    if len(message) < 20:
        # Add contextual friendliness
        if message.lower() in ["done", "ok", "completed"]:
            return f"Done! Is there anything else you'd like me to help with?"
        if message.lower() in ["error", "failed"]:
            return f"Something went wrong. Let me know if you'd like to try again."

    # Ensure messages don't end abruptly
    if message and not message[-1] in '.!?':
        message += '.'

    return message
```

### 3. format_tool_calls

Structures tool calls for API response.

```python
def format_tool_calls(tool_calls: list) -> list[dict]:
    """
    Format tool calls for transparency in API response.

    Args:
        tool_calls: Raw list of tool invocations

    Returns:
        list[dict]: Formatted tool call summaries
    """
    if not tool_calls:
        return []

    formatted = []
    for call in tool_calls:
        formatted.append({
            "tool": call.get("name", "unknown"),
            "status": "success" if call.get("success", True) else "error",
            "summary": generate_tool_summary(call)
        })

    return formatted


def generate_tool_summary(tool_call: dict) -> str:
    """
    Generate human-readable summary of tool action.

    Args:
        tool_call: Tool call with name and parameters

    Returns:
        str: Brief description of what the tool did
    """
    name = tool_call.get("name", "")
    params = tool_call.get("parameters", {})
    result = tool_call.get("result", {})

    summaries = {
        "list_todos": "Retrieved your todos",
        "create_todo": f"Created todo: {params.get('title', 'new task')[:30]}",
        "update_todo": f"Updated todo: {params.get('todo_id', 'task')[:20]}",
        "delete_todo": f"Deleted todo: {params.get('todo_id', 'task')[:20]}",
    }

    return summaries.get(name, f"Executed {name}")
```

## Response Examples

### Successful Todo List
```json
{
    "conversation_id": "abc-123-def",
    "response": "Here are your todos:\n\n1. Buy groceries (pending)\n2. Call mom (completed)\n3. Finish report (pending, high priority)\n\nWould you like to add, update, or complete any of these?",
    "tool_calls": [
        {"tool": "list_todos", "status": "success", "summary": "Retrieved your todos"}
    ]
}
```

### Todo Created
```json
{
    "conversation_id": "abc-123-def",
    "response": "Done! I've added 'Schedule dentist appointment' to your todos. Is there anything else you'd like me to help with?",
    "tool_calls": [
        {"tool": "create_todo", "status": "success", "summary": "Created todo: Schedule dentist appointment"}
    ]
}
```

### Error Response
```json
{
    "conversation_id": "abc-123-def",
    "response": "I couldn't find that todo. Could you show me your list first so we can identify the right one?",
    "tool_calls": [
        {"tool": "delete_todo", "status": "error", "summary": "Deleted todo: unknown"}
    ]
}
```

### Chained Operations
```json
{
    "conversation_id": "abc-123-def",
    "response": "I found 3 completed todos and removed them. Your list now has 2 pending items remaining.",
    "tool_calls": [
        {"tool": "list_todos", "status": "success", "summary": "Retrieved your todos"},
        {"tool": "delete_todo", "status": "success", "summary": "Deleted todo: Buy groceries"},
        {"tool": "delete_todo", "status": "success", "summary": "Deleted todo: Call mom"},
        {"tool": "delete_todo", "status": "success", "summary": "Deleted todo: Old task"}
    ]
}
```

## Best Practices

- Always return valid JSON structure
- Never expose internal errors to users
- Keep tool summaries concise (under 50 chars)
- Maintain consistent response format across all endpoints
- Log raw responses before cleaning for debugging
- Test with edge cases (empty responses, long messages)
- Ensure conversation_id is always present
- Use friendly language without being excessive
