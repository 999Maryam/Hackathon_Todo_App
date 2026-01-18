"""Chat API schemas for Todo AI Chatbot.

Task: T007 | Spec: specs/008-chat-endpoint-ui/spec.md
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