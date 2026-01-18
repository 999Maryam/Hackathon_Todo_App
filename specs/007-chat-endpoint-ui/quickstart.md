# Quickstart: Chat Endpoint & Beautiful Responsive Chat UI

**Feature**: 008-chat-endpoint-ui
**Date**: 2026-01-15

---

## Prerequisites

Before implementing this feature, ensure:

1. **Phase II Complete**: JWT authentication working, Task model in database
2. **Spec 1 Complete**: Conversation/Message models and CRUD helpers
3. **Spec 2 Complete**: MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
4. **Spec 3 Complete**: Gemini AI agent and chat runner
5. **Environment**: `GEMINI_API_KEY` configured in `.env`

---

## Installation

### Backend Setup
1. Verify required dependencies in `backend/requirements.txt`:
   ```
   google-generativeai>=0.4.1
   fastapi>=0.104.1
   ```

2. Verify environment variables in `backend/.env`:
   ```env
   GEMINI_API_KEY=your-gemini-api-key-here
   BETTER_AUTH_SECRET=your-secret-key
   DATABASE_URL=postgresql://...
   ```

### Frontend Setup
1. Install required dependencies in `frontend/package.json`:
   ```json
   {
     "dependencies": {
       "@radix-ui/react-*": "^1.0.0",
       "framer-motion": "^10.0.0",
       "tailwindcss": "^3.0.0",
       "next": "^16.0.0"
     }
   }
   ```

---

## Implementation Guide

### Step 1: Create Chat Endpoint (backend/app/routers/chat.py)

```python
"""Chat endpoint for Todo AI Chatbot.

Task: T001 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-001-FR-009
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.user import User
from app.agents.chat_runner import run_agent_with_tools
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/{user_id}", tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Process chat messages with AI assistant."""
    # Validate user authorization
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Run AI agent with tools
    response = await run_agent_with_tools(
        user_id=user_id,
        message=request.message,
        conversation_id=request.conversation_id,
        db=db
    )

    return ChatResponse(
        conversation_id=response.conversation_id,
        response=response.content,
        tool_calls=response.tool_calls
    )
```

### Step 2: Create Request/Response Models (backend/app/schemas/chat.py)

```python
"""Chat API schemas for Todo AI Chatbot.

Task: T002 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-003-FR-004
"""
from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ToolCallRecord(BaseModel):
    """Record of a tool invocation during agent execution."""
    name: str
    arguments: dict
    result: dict


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: List[ToolCallRecord]
```

### Step 3: Create Chat Page (frontend/app/chat/page.tsx)

```tsx
"use client";

/**
 * Chat page for Todo AI Chatbot.
 *
 * Task: T003 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-009-FR-023
 */
import { useState, useRef, useEffect } from 'react';
import { useAuth } from 'better-auth/react';
import ChatBubble from '@/components/ChatBubble';
import ChatInput from '@/components/ChatInput';
import TypingIndicator from '@/components/TypingIndicator';
import { sendMessage } from '@/lib/api';

export default function ChatPage() {
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const { auth } = useAuth();

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Add user message to UI immediately
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send to API
      const response = await sendMessage(text, auth.session?.user?.id);

      // Add assistant response
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.response,
          tool_calls: response.tool_calls,
          timestamp: new Date()
        }
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      setMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered an error. Please try again.',
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6">
        <h1 className="text-xl font-semibold text-gray-800">AI Task Assistant</h1>
      </header>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <ChatBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <TypingIndicator />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Bar */}
      <div className="bg-white border-t border-gray-200 p-4">
        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
        />
      </div>
    </div>
  );
}
```

### Step 4: Create ChatBubble Component (frontend/components/ChatBubble.tsx)

```tsx
/**
 * Chat bubble component for Todo AI Chatbot.
 *
 * Task: T004 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-010-FR-011
 */
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export default function ChatBubble({ role, content, timestamp }: ChatBubbleProps) {
  const isUser = role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`
          max-w-[80%] md:max-w-[70%] rounded-2xl px-4 py-3 my-1
          ${isUser
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-br-none'
            : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none'
          }
        `}
      >
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          className={`
            ${isUser ? 'text-white' : 'text-gray-800'}
            prose prose-sm max-w-none
          `}
        >
          {content}
        </ReactMarkdown>

        {timestamp && (
          <div className={`
            text-xs mt-1 opacity-70
            ${isUser ? 'text-blue-100' : 'text-gray-500'}
          `}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </motion.div>
  );
}
```

### Step 5: Create API Client (frontend/lib/api.ts)

```ts
/**
 * API client with JWT support for Todo AI Chatbot.
 *
 * Task: T005 | Spec: specs/008-chat-endpoint-ui/spec.md#FR-021
 */

interface ChatRequest {
  conversation_id?: number;
  message: string;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}

export async function sendMessage(
  message: string,
  userId: string | undefined,
  conversationId?: number
): Promise<ChatResponse> {
  if (!userId) {
    throw new Error('User not authenticated');
  }

  const token = localStorage.getItem('auth-token'); // Or however you store JWT

  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message: message,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}
```

---

## Testing the Feature

### Backend Tests
1. Test that authenticated user can send messages:
   - Send "Add buy groceries to my tasks" → verify add_task called
   - Send "What are my tasks?" → verify list_tasks called
   - Send without JWT → verify 401 Unauthorized

### Frontend Tests
1. Navigate to `/chat` page
2. Type "Add buy groceries to my tasks" → verify message appears in UI
3. Verify typing indicator shows while AI processes
4. Verify assistant response appears in bubble
5. Test on mobile - verify input bar stays at bottom

---

## Environment Variables

Ensure these are set in `backend/.env`:

```env
# Required
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE_URL=postgresql://user:pass@host:5432/db
BETTER_AUTH_SECRET=your-secret-key

# Optional
GEMINI_MODEL=gemini-1.5-flash
```

---

## Verification Checklist

After implementation, verify:

- [ ] Chat endpoint accessible at `/api/{user_id}/chat`
- [ ] JWT authentication working (401 without token)
- [ ] AI responds to natural language task commands
- [ ] User messages appear in right-aligned gradient bubbles
- [ ] Assistant responses appear in left-aligned clean bubbles
- [ ] Typing indicator shows during AI processing
- [ ] Markdown formatting works in assistant responses
- [ ] Page works responsively on mobile/tablet/desktop
- [ ] Conversation persists across page reloads
- [ ] Different users cannot see each other's conversations
- [ ] Error messages are user-friendly
- [ ] Enter key sends message, Esc clears input