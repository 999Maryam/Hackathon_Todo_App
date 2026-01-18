# Research: Chat Endpoint & Beautiful Responsive Chat UI

**Feature**: 008-chat-endpoint-ui
**Date**: 2026-01-15
**Status**: Complete

---

## Research Questions

### Q1: How to implement JWT-protected FastAPI endpoint for chat?

**Findings**: The endpoint needs to follow the same JWT authentication pattern as Phase II. We can reuse the existing JWT dependencies and authentication middleware from the previous phases.

**Key Code Pattern**:
```python
from fastapi import Depends, HTTPException
from app.auth import get_current_user  # Reuse from Phase II
from app.models.user import User

@app.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    # Validate user_id matches current_user.id for security
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Process chat request with Gemini agent
    # ... implementation
```

**Decision**: Reuse existing JWT authentication pattern from Phase II for consistency and security.

### Q2: How to integrate Google Gemini API with conversation history?

**Findings**: The Gemini API supports conversation history through the content parameter. We need to load conversation history from the database and format it appropriately for the API.

**Key Code Pattern**:
```python
from google import generativemodel as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Load conversation history
history = get_conversation_history(conversation_id, user_id, db)

# Format for Gemini API
formatted_history = []
for msg in history:
    formatted_history.append({
        "role": "user" if msg.role == "user" else "model",
        "parts": [{"text": msg.content}]
    })

# Generate response
chat = model.start_chat(history=formatted_history)
response = chat.send_message(user_input)
```

**Decision**: Use Google Gemini API with conversation history formatted appropriately.

### Q3: How to execute MCP tools called by Gemini agent?

**Findings**: The Gemini agent will return function calls that need to be executed. We need to map these to the existing MCP tools from Spec 2.

**Key Code Pattern**:
```python
def execute_tool_call(tool_name: str, args: dict, user_id: str, db: Session):
    """Execute a tool call from the AI agent."""
    if tool_name == "add_task":
        return task_tools.add_task(
            user_id=user_id,
            title=args.get("title"),
            description=args.get("description"),
            db=db
        )
    elif tool_name == "list_tasks":
        return task_tools.list_tasks(
            user_id=user_id,
            status=args.get("status", "all"),
            db=db
        )
    # ... other tools

def process_tool_calls(tool_calls: list, user_id: str, db: Session):
    """Process multiple tool calls from the agent."""
    results = []
    for call in tool_calls:
        result = execute_tool_call(call.name, call.args, user_id, db)
        results.append(result)
    return results
```

**Decision**: Map Gemini function calls to existing Spec 2 MCP tools with proper user context injection.

### Q4: What UI library to use for beautiful chat interface?

**Findings**: For a premium, responsive chat UI, we have several options:
- shadcn/ui: Excellent for accessible, customizable components with Tailwind
- Material UI: Robust but heavier
- Custom Tailwind components: Maximum flexibility

**Comparison**:
- shadcn/ui: Pros - Accessible, well-designed, Tailwind-based, extensive components; Cons - Additional dependency
- Custom: Pros - Complete control, minimal dependencies; Cons - More implementation work

**Decision**: Use shadcn/ui with Tailwind CSS for premium look and accessibility.

### Q5: How to implement message bubbles with animations?

**Findings**: Message bubbles require different styling for user vs assistant messages, with animations for smooth appearance.

**Key Code Pattern**:
```tsx
// User message bubble (right-aligned, gradient)
<div className="flex justify-end mb-4">
  <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl px-4 py-2 max-w-xs md:max-w-md">
    {message.content}
  </div>
</div>

// Assistant message bubble (left-aligned, clean)
<div className="flex justify-start mb-4">
  <div className="bg-gray-100 border border-gray-200 text-gray-800 rounded-2xl px-4 py-2 max-w-xs md:max-w-md">
    {renderMarkdown(message.content)}
  </div>
</div>

// Animation using Framer Motion
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {/* Message content */}
</motion.div>
```

**Decision**: Implement gradient user bubbles with clean assistant bubbles, using Framer Motion for animations.

### Q6: How to handle typing indicators and loading states?

**Findings**: Typing indicators are essential for AI chat experiences. Three bouncing dots is the standard pattern.

**Key Code Pattern**:
```tsx
// Typing indicator component
const TypingIndicator = () => (
  <div className="flex space-x-1 p-2">
    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
  </div>
);

// Loading states
const [isLoading, setIsLoading] = useState(false);
```

**Decision**: Implement three-dot bouncing animation for typing indicators.

### Q7: How to persist conversation_id across page reloads?

**Findings**: Using localStorage is the standard approach for maintaining conversation state across page reloads.

**Key Code Pattern**:
```tsx
// Store conversation ID
const storeConversationId = (id: number) => {
  localStorage.setItem('currentConversationId', id.toString());
};

// Retrieve conversation ID
const getStoredConversationId = (): number | null => {
  const id = localStorage.getItem('currentConversationId');
  return id ? parseInt(id, 10) : null;
};

// Clear when starting new conversation
const clearStoredConversationId = () => {
  localStorage.removeItem('currentConversationId');
};
```

**Decision**: Use localStorage for conversation persistence across page reloads.

---

## Technology Decisions Summary

1. **Backend**: FastAPI with reused JWT auth from Phase II
2. **AI**: Google Gemini API with conversation history support
3. **Tools**: Reuse existing MCP tools from Spec 2 with proper context injection
4. **Frontend**: Next.js 16+ with TypeScript, Tailwind CSS, and shadcn/ui
5. **Animations**: Framer Motion for smooth transitions
6. **State**: localStorage for conversation persistence

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Google Gemini API: https://ai.google.dev/
- shadcn/ui: https://ui.shadcn.com/
- Framer Motion: https://www.framer.com/motion/