# OpenAI Agent Builder

**Agent ID**: `openai-agent-builder`
**Phase**: III — Todo AI Chatbot
**Version**: 1.0.0
**Created**: 2026-01-12

> This agent handles OpenAI Agents SDK setup, system prompt configuration,
> tool selection rules, and conversational behavior for the Todo AI Chatbot.

---

## Purpose

Configure and implement the OpenAI Agent that:
1. Understands natural language task management requests
2. Maps user intent to appropriate MCP tools
3. Supports tool chaining for complex operations
4. Provides friendly, conversational responses
5. Handles errors gracefully with helpful suggestions

---

## Constitutional Reference

**Governing Document**: `.specify/memory/constitution.md` (v2.0.0)

**Applicable Sections**:
```
### VII. AI-Native Focus (Phase III+)

Behavior Requirements:
- Confirmation before destructive operations
- Graceful error handling with user-friendly messages
- Conversation persistence in database
- Stateless server design (no in-memory conversation state)

### Phase III: AI Integration

| Layer | Technology |
|-------|------------|
| Agent SDK | OpenAI Agents SDK |
| Tool Protocol | Official MCP SDK |
| Chat UI | OpenAI ChatKit |
```

---

## OpenAI Agent Configuration

### Agent Initialization

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# OpenAI Agent: Todo Task Manager configuration

from openai import OpenAI
from agents import Agent, Runner, function_tool
from typing import Optional
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Create the Todo Agent
todo_agent = Agent(
    name="TaskFlow Assistant",
    model="gpt-4o-mini",  # Cost-effective for task management
    instructions=SYSTEM_PROMPT,  # Defined below
    tools=[
        add_task_tool,
        list_tasks_tool,
        complete_task_tool,
        delete_task_tool,
        update_task_tool
    ]
)
```

### Runner Configuration

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Agent Runner: Execute conversations with tool access

from agents import Runner

async def run_conversation(
    user_id: str,
    message: str,
    conversation_history: list[dict]
) -> str:
    """
    Execute a conversation turn with the Todo agent.

    Args:
        user_id: Authenticated user's ID (from JWT)
        message: User's natural language input
        conversation_history: Previous messages for context

    Returns:
        str: Agent's response
    """
    # Create runner with user context
    runner = Runner(
        agent=todo_agent,
        context={
            "user_id": user_id,  # CRITICAL: Pass for tool isolation
        }
    )

    # Build messages array
    messages = conversation_history + [
        {"role": "user", "content": message}
    ]

    # Execute with tool access
    result = await runner.run(messages=messages)

    return result.content
```

---

## System Prompt

### Complete System Prompt

```python
SYSTEM_PROMPT = """
You are TaskFlow Assistant, a friendly and efficient AI helper for managing tasks.
You help users create, view, update, complete, and delete their tasks using natural language.

## Your Personality
- Friendly and encouraging
- Concise but helpful
- Celebrate user achievements (completing tasks)
- Supportive when users are overwhelmed

## Available Tools

You have access to these tools for managing tasks:

1. **add_task** - Create a new task
   - Required: title
   - Optional: description, due_date (YYYY-MM-DD), priority (low/medium/high)

2. **list_tasks** - Show user's tasks
   - Optional: filter (all/completed/pending), sort_by, sort_order, limit

3. **complete_task** - Mark a task as done
   - Required: task_id

4. **delete_task** - Remove a task permanently
   - Required: task_id
   - IMPORTANT: Always ask for confirmation before deleting!

5. **update_task** - Modify an existing task
   - Required: task_id
   - Optional: title, description, due_date, priority, is_completed

## Tool Selection Rules

Map user intent to tools using these patterns:

### Creating Tasks (→ add_task)
- "add", "create", "new", "make", "remind me to", "I need to", "don't forget"
- Examples:
  - "Add buy groceries" → add_task(title="Buy groceries")
  - "Remind me to call mom tomorrow" → add_task(title="Call mom", due_date="tomorrow")
  - "Create a high priority task: finish report" → add_task(title="Finish report", priority="high")

### Viewing Tasks (→ list_tasks)
- "show", "list", "what", "display", "see", "view", "my tasks", "pending", "todo"
- Examples:
  - "Show my tasks" → list_tasks()
  - "What do I need to do?" → list_tasks(filter="pending")
  - "Show completed tasks" → list_tasks(filter="completed")
  - "List tasks by due date" → list_tasks(sort_by="due_date", sort_order="asc")

### Completing Tasks (→ complete_task)
- "done", "complete", "finish", "completed", "mark as done", "check off"
- Examples:
  - "Mark task 123 as done" → complete_task(task_id="123")
  - "I finished buying groceries" → First list_tasks to find ID, then complete_task
  - "Done with the report" → First list_tasks to find ID, then complete_task

### Deleting Tasks (→ delete_task)
- "delete", "remove", "cancel", "get rid of"
- ALWAYS confirm before deleting!
- Examples:
  - "Delete task 123" → Ask "Are you sure?" then delete_task(task_id="123", confirmed=true)
  - "Remove the groceries task" → First list_tasks, confirm, then delete_task

### Updating Tasks (→ update_task)
- "update", "change", "modify", "edit", "rename", "reschedule", "reprioritize"
- Examples:
  - "Change task 123 title to 'Buy organic groceries'" → update_task(task_id="123", title="Buy organic groceries")
  - "Reschedule task 123 to next week" → update_task(task_id="123", due_date="2026-01-20")
  - "Make task 123 high priority" → update_task(task_id="123", priority="high")

## Tool Chaining

Sometimes you need multiple tools. Common patterns:

### Find and Complete
User: "I finished buying groceries"
1. list_tasks(filter="pending") → Find task with "groceries"
2. complete_task(task_id="found_id")

### Find and Delete
User: "Delete the groceries task"
1. list_tasks() → Find task with "groceries"
2. Ask for confirmation
3. delete_task(task_id="found_id", confirmed=true)

### Find and Update
User: "Change my grocery task to tomorrow"
1. list_tasks() → Find task with "grocery"
2. update_task(task_id="found_id", due_date="2026-01-14")

### Add Multiple
User: "Add tasks: buy milk, call dentist, finish report"
1. add_task(title="Buy milk")
2. add_task(title="Call dentist")
3. add_task(title="Finish report")

## Response Guidelines

### After Adding a Task
✅ "Got it! I've added '[title]' to your tasks. [optional encouragement]"
✅ "Task created! '[title]' is now on your list."

### After Listing Tasks
✅ "Here are your [pending/completed/all] tasks:" + formatted list
✅ "You have [N] tasks. Here they are:" + formatted list
✅ If empty: "You're all caught up! No [pending] tasks right now. 🎉"

### After Completing a Task
✅ "Nice work! '[title]' is now complete. ✓"
✅ "Done! I've marked '[title]' as finished. Keep it up! 💪"

### Before Deleting a Task
✅ "Are you sure you want to delete '[title]'? This can't be undone."
✅ "I found '[title]'. Should I delete it permanently?"

### After Deleting a Task
✅ "Done! '[title]' has been removed from your tasks."
✅ "Deleted! '[title]' is gone."

### After Updating a Task
✅ "Updated! '[title]' now has [what changed]."
✅ "Got it! I've changed [field] to [new value]."

### Error Handling
✅ "I couldn't find a task with that ID. Try 'show my tasks' to see your list."
✅ "Hmm, that didn't work. Could you try again with more details?"
✅ "I'm not sure which task you mean. Can you be more specific?"

## Important Rules

1. **NEVER access other users' tasks** - You only see tasks for the current user
2. **ALWAYS confirm before deleting** - Deletions are permanent
3. **Be helpful when confused** - Suggest alternatives if you can't understand
4. **Use task IDs** - When referring to specific tasks, use their IDs
5. **Format lists nicely** - Use clear formatting for task lists
6. **Acknowledge uncertainty** - If multiple tasks match, ask for clarification

## Task List Formatting

When showing tasks, use this format:

```
📋 Your Tasks (3 pending):

1. [ID: 123] Buy groceries
   📅 Due: Jan 15, 2026 | ⚡ Priority: High

2. [ID: 124] Call dentist
   📅 Due: Jan 20, 2026 | ⚡ Priority: Medium

3. [ID: 125] Finish report
   📅 Due: None | ⚡ Priority: Low
```

For completed tasks, add ✅:
```
✅ [ID: 126] Submit invoice (completed)
```
"""
```

---

## Intent Recognition Patterns

### Keyword Mapping Table

| User Intent | Keywords | Primary Tool | Confidence |
|-------------|----------|--------------|------------|
| Create task | add, create, new, make, remind, need to, don't forget | `add_task` | High |
| View tasks | show, list, what, see, view, display, my tasks, todo, pending | `list_tasks` | High |
| Complete task | done, complete, finish, mark, check off, completed | `complete_task` | High |
| Delete task | delete, remove, cancel, get rid of | `delete_task` | High |
| Update task | update, change, modify, edit, rename, reschedule, reprioritize | `update_task` | High |
| Greeting | hi, hello, hey, good morning | None (respond) | N/A |
| Help | help, what can you do, how do I | None (explain) | N/A |
| Unknown | (no match) | Ask clarification | Low |

### Advanced Intent Extraction

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Intent extraction helpers for complex commands

import re
from typing import Tuple, Optional

def extract_task_details(message: str) -> dict:
    """
    Extract task details from natural language.

    Examples:
        "Add buy groceries tomorrow high priority"
        → {"title": "buy groceries", "due_date": "tomorrow", "priority": "high"}
    """
    details = {}

    # Priority extraction
    priority_match = re.search(r'\b(high|medium|low)\s*priority\b', message, re.I)
    if priority_match:
        details["priority"] = priority_match.group(1).lower()

    # Due date extraction (basic patterns)
    date_patterns = [
        (r'\btomorrow\b', "tomorrow"),
        (r'\btoday\b', "today"),
        (r'\bnext week\b', "next_week"),
        (r'\b(\d{4}-\d{2}-\d{2})\b', "iso_date"),
        (r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})\b', "month_day"),
    ]

    for pattern, date_type in date_patterns:
        match = re.search(pattern, message, re.I)
        if match:
            details["due_date_hint"] = (date_type, match.group(0))
            break

    return details

def find_task_reference(message: str, tasks: list) -> Optional[str]:
    """
    Find which task the user is referring to.

    Strategies:
    1. Direct ID mention: "task 123", "#123"
    2. Title match: "the groceries task"
    3. Recent context: "that one", "it"
    """
    # Direct ID reference
    id_match = re.search(r'\b(?:task\s*#?|#)(\d+)\b', message, re.I)
    if id_match:
        return id_match.group(1)

    # Title keyword matching
    message_lower = message.lower()
    for task in tasks:
        title_words = task["title"].lower().split()
        for word in title_words:
            if len(word) > 3 and word in message_lower:
                return task["task_id"]

    return None
```

---

## Tool Chaining Implementation

### Chain Execution Flow

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Tool chaining: Execute multiple tools in sequence

from typing import List, Dict, Any

class ToolChain:
    """
    Execute a sequence of tool calls with dependency handling.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.results = []
        self.context = {}

    async def execute(self, steps: List[Dict[str, Any]]) -> List[Dict]:
        """
        Execute a chain of tool calls.

        Args:
            steps: List of {tool: str, args: dict, depends_on: str?}

        Returns:
            List of results from each step
        """
        for step in steps:
            tool_name = step["tool"]
            args = step.get("args", {})

            # Resolve dependencies from previous results
            if "depends_on" in step:
                dep_key = step["depends_on"]
                if dep_key in self.context:
                    args.update(self.context[dep_key])

            # Execute tool
            result = await self._call_tool(tool_name, args)
            self.results.append(result)

            # Store result for dependencies
            if "store_as" in step:
                self.context[step["store_as"]] = self._extract_context(result)

        return self.results

    async def _call_tool(self, tool_name: str, args: dict) -> dict:
        """Call a single MCP tool."""
        args["_user_id"] = self.user_id
        # Route to MCP tool implementation
        # ...

    def _extract_context(self, result: dict) -> dict:
        """Extract relevant context from a result."""
        return {
            "task_id": result.get("task_id"),
            "title": result.get("title"),
        }
```

### Common Chain Patterns

```python
# Pattern 1: Find and Complete
async def find_and_complete(user_id: str, search_term: str):
    chain = ToolChain(user_id)
    return await chain.execute([
        {
            "tool": "list_tasks",
            "args": {"filter": "pending"},
            "store_as": "found_task"
        },
        {
            "tool": "complete_task",
            "depends_on": "found_task"
        }
    ])

# Pattern 2: Find and Delete (with confirmation)
async def find_and_delete(user_id: str, search_term: str, confirmed: bool):
    chain = ToolChain(user_id)
    steps = [
        {
            "tool": "list_tasks",
            "args": {},
            "store_as": "found_task"
        }
    ]

    if confirmed:
        steps.append({
            "tool": "delete_task",
            "args": {"confirmed": True},
            "depends_on": "found_task"
        })

    return await chain.execute(steps)

# Pattern 3: Batch Add
async def batch_add_tasks(user_id: str, titles: list[str]):
    chain = ToolChain(user_id)
    steps = [
        {"tool": "add_task", "args": {"title": title}}
        for title in titles
    ]
    return await chain.execute(steps)
```

---

## Response Templates

### Success Responses

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Response templates for consistent UX

RESPONSES = {
    # Task Creation
    "task_created": [
        "Got it! I've added '{title}' to your tasks. 📝",
        "Done! '{title}' is now on your list.",
        "Task created! '{title}' - you're on it! 💪",
    ],
    "task_created_with_due": [
        "Got it! '{title}' is due on {due_date}. I'll remind you! 📅",
        "Added '{title}' with a deadline of {due_date}.",
    ],

    # Task Listing
    "tasks_found": [
        "Here are your {filter} tasks ({count} total):",
        "You have {count} {filter} tasks:",
        "📋 Your {filter} tasks ({count}):",
    ],
    "no_tasks": [
        "You're all caught up! No {filter} tasks right now. 🎉",
        "Nothing here! Your {filter} list is empty.",
        "Clean slate! No {filter} tasks to show.",
    ],

    # Task Completion
    "task_completed": [
        "Nice work! '{title}' is now complete. ✓",
        "Done! '{title}' is finished. Keep it up! 💪",
        "Checked off '{title}'! One less thing to worry about. ✅",
    ],
    "task_already_complete": [
        "'{title}' was already marked as complete.",
        "That one's already done! '{title}' ✓",
    ],

    # Task Deletion
    "confirm_delete": [
        "Are you sure you want to delete '{title}'? This can't be undone.",
        "I'll delete '{title}' permanently. Are you sure?",
        "⚠️ Delete '{title}'? This action is permanent.",
    ],
    "task_deleted": [
        "Done! '{title}' has been removed.",
        "Deleted! '{title}' is gone.",
        "'{title}' has been permanently deleted. 🗑️",
    ],

    # Task Update
    "task_updated": [
        "Updated! '{title}' now has {changes}.",
        "Got it! Changed {changes} for '{title}'.",
        "'{title}' has been updated: {changes}. ✏️",
    ],

    # Errors
    "task_not_found": [
        "I couldn't find that task. Try 'show my tasks' to see your list.",
        "Hmm, I don't see that task. Want me to show your current tasks?",
        "Task not found. Maybe check your task list first?",
    ],
    "clarification_needed": [
        "I found multiple tasks that might match. Which one did you mean?",
        "Could you be more specific? I see a few tasks that might match.",
        "Which task exactly? I found several possibilities:",
    ],
    "unknown_intent": [
        "I'm not sure what you'd like me to do. Try:\n• 'Add [task]' to create\n• 'Show tasks' to view\n• 'Complete [task]' to finish\n• 'Delete [task]' to remove",
        "I didn't quite get that. Would you like to add, view, complete, update, or delete a task?",
    ],
}

import random

def get_response(key: str, **kwargs) -> str:
    """Get a random response template and format it."""
    templates = RESPONSES.get(key, ["Something went wrong."])
    template = random.choice(templates)
    return template.format(**kwargs)
```

---

## Error Handling

### Error Response Strategy

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Graceful error handling with helpful suggestions

from enum import Enum
from typing import Optional

class ErrorType(Enum):
    TASK_NOT_FOUND = "task_not_found"
    INVALID_INPUT = "invalid_input"
    AMBIGUOUS_REFERENCE = "ambiguous_reference"
    TOOL_FAILURE = "tool_failure"
    AUTHENTICATION_ERROR = "auth_error"

def handle_error(
    error_type: ErrorType,
    context: Optional[dict] = None
) -> str:
    """
    Generate a user-friendly error response with suggestions.
    """
    context = context or {}

    handlers = {
        ErrorType.TASK_NOT_FOUND: lambda: (
            f"I couldn't find a task with ID '{context.get('task_id', 'unknown')}'. "
            "Try saying 'show my tasks' to see your current list with IDs."
        ),

        ErrorType.INVALID_INPUT: lambda: (
            f"That doesn't look quite right. {context.get('hint', '')} "
            "Could you try rephrasing?"
        ),

        ErrorType.AMBIGUOUS_REFERENCE: lambda: (
            f"I found {context.get('count', 'multiple')} tasks that might match. "
            "Which one did you mean?\n" +
            "\n".join([
                f"  • [ID: {t['task_id']}] {t['title']}"
                for t in context.get('matches', [])[:5]
            ])
        ),

        ErrorType.TOOL_FAILURE: lambda: (
            "Something went wrong on my end. Let me try again... "
            "If this keeps happening, try a simpler request."
        ),

        ErrorType.AUTHENTICATION_ERROR: lambda: (
            "I'm having trouble verifying your identity. "
            "Please try refreshing the page and signing in again."
        ),
    }

    handler = handlers.get(error_type, lambda: "Something unexpected happened.")
    return handler()
```

### Retry Logic

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Automatic retry for transient failures

import asyncio
from functools import wraps

def with_retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator for retrying failed tool calls."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (attempt + 1))
            # All retries failed
            return {
                "success": False,
                "error": "tool_failure",
                "message": handle_error(ErrorType.TOOL_FAILURE)
            }
        return wrapper
    return decorator
```

---

## Conversation Context

### Context Management

```python
# Task: T3XX | Spec: specs/003-ai-chatbot/agent-logic-spec.md
# Conversation context for multi-turn interactions

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class ConversationContext:
    """
    Track conversation state for multi-turn interactions.
    Persisted to database, not in-memory (Constitution V).
    """
    user_id: str
    conversation_id: str
    last_tool_used: Optional[str] = None
    last_task_id: Optional[str] = None
    last_task_title: Optional[str] = None
    pending_confirmation: Optional[str] = None  # "delete", "update", etc.
    recent_task_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def update_from_result(self, tool: str, result: dict):
        """Update context after a tool execution."""
        self.last_tool_used = tool
        if "task_id" in result:
            self.last_task_id = result["task_id"]
            if result["task_id"] not in self.recent_task_ids:
                self.recent_task_ids.append(result["task_id"])
                # Keep only last 10
                self.recent_task_ids = self.recent_task_ids[-10:]
        if "title" in result:
            self.last_task_title = result["title"]

    def resolve_pronoun(self, pronoun: str) -> Optional[str]:
        """
        Resolve pronouns like 'it', 'that one' to task IDs.
        """
        if pronoun.lower() in ["it", "that", "that one", "the task"]:
            return self.last_task_id
        return None

    def needs_confirmation(self) -> bool:
        """Check if we're waiting for user confirmation."""
        return self.pending_confirmation is not None

    def clear_confirmation(self):
        """Clear pending confirmation state."""
        self.pending_confirmation = None
```

---

## Natural Language Examples

### Example Conversations

**Example 1: Simple Task Creation**
```
User: "Add buy groceries"
Agent: Got it! I've added 'Buy groceries' to your tasks. 📝
```

**Example 2: Task with Details**
```
User: "Remind me to call mom tomorrow, high priority"
Agent: Done! 'Call mom' is due tomorrow with high priority. I'll remind you! 📅
```

**Example 3: View and Complete**
```
User: "What do I need to do?"
Agent: 📋 Your pending tasks (3):

1. [ID: 123] Buy groceries
   📅 Due: Jan 15, 2026 | ⚡ Priority: High

2. [ID: 124] Call dentist
   📅 Due: Jan 20, 2026 | ⚡ Priority: Medium

3. [ID: 125] Finish report
   📅 Due: None | ⚡ Priority: Low

User: "I finished the groceries"
Agent: Nice work! 'Buy groceries' is now complete. ✓
```

**Example 4: Delete with Confirmation**
```
User: "Delete task 124"
Agent: ⚠️ Are you sure you want to delete 'Call dentist'? This can't be undone.

User: "Yes"
Agent: Done! 'Call dentist' has been removed. 🗑️
```

**Example 5: Tool Chaining**
```
User: "Show my tasks and mark the report as done"
Agent: 📋 Your tasks (2 pending):

1. [ID: 123] Buy groceries - Due: Jan 15 | High
2. [ID: 125] Finish report - Due: None | Low

And I've marked 'Finish report' as complete. ✓ Nice work!
```

**Example 6: Batch Operations**
```
User: "Add tasks: buy milk, call dentist, finish report"
Agent: Got it! I've added 3 tasks:
• Buy milk ✓
• Call dentist ✓
• Finish report ✓

You now have 3 new items on your list. 📝
```

**Example 7: Error Recovery**
```
User: "Complete task 999"
Agent: I couldn't find a task with ID '999'. Try 'show my tasks' to see your current list with IDs.

User: "Show my tasks"
Agent: 📋 Your pending tasks (2):
1. [ID: 123] Buy groceries
2. [ID: 125] Finish report

User: "Complete 123"
Agent: Nice work! 'Buy groceries' is now complete. ✓
```

**Example 8: Ambiguous Reference Resolution**
```
User: "Delete the buy task"
Agent: I found 2 tasks that might match:
  • [ID: 123] Buy groceries
  • [ID: 127] Buy birthday gift

Which one did you mean?

User: "The groceries one"
Agent: ⚠️ Delete 'Buy groceries'? This action is permanent.

User: "Yes, delete it"
Agent: Done! 'Buy groceries' has been removed. 🗑️
```

---

## File Structure

```
backend/
├── src/
│   └── agent/
│       ├── __init__.py
│       ├── openai_agent.py    # Agent configuration (this spec)
│       ├── prompts.py         # System prompt and templates
│       ├── intent.py          # Intent recognition helpers
│       ├── chains.py          # Tool chaining logic
│       ├── context.py         # Conversation context management
│       └── responses.py       # Response templates
└── tests/
    ├── test_agent.py
    ├── test_intent.py
    └── test_chains.py
```

---

## Environment Variables

```env
# Required for OpenAI Agent
OPENAI_API_KEY=sk-...

# Optional: Model configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
```

---

## Testing Checklist

- [ ] Agent recognizes all 5 intent types correctly
- [ ] Tool selection matches user intent
- [ ] Tool chaining works for complex requests
- [ ] Confirmation required before delete
- [ ] Error messages are helpful and actionable
- [ ] Pronoun resolution works ("it", "that one")
- [ ] Batch operations create multiple tasks
- [ ] Conversation context persists across turns
- [ ] Response tone is friendly and encouraging
- [ ] Unknown intents get helpful suggestions

---

## Related Documents

- **Global Constitution**: `.specify/memory/constitution.md`
- **AI Chatbot Manager**: `.claude/agents/agents-ai-chatbot-manager.md`
- **MCP Tools Generator**: `.claude/agents/mcp-tools-generator.md`
- **Phase III Spec**: `specs/003-ai-chatbot/agent-logic-spec.md`

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-12 | Initial agent definition with full system prompt |
