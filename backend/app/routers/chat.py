"""Chat endpoint for Todo AI Chatbot.

Task: T008 | Spec: specs/008-chat-endpoint-ui/spec.md
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.auth import get_current_user
from app.database import get_session
from app.models.user import User
from app.agents.chat_runner import run_agent_with_tools
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])

@router.post("/{user_id}/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Process natural language chat message with AI agent and tools.

    - Validates user authorization
    - Runs Gemini agent with conversation context
    - Executes any tool calls (task management)
    - Returns response with tool call details
    """
    # Strict user isolation check
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only chat with your own tasks and data"
        )

    try:
        # Run the full agent + tools cycle
        agent_result = await run_agent_with_tools(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id,
            db=db
        )

        # Convert tool_calls to dicts to avoid Pydantic model type mismatch
        # (openai_agent.ToolCallRecord vs schemas.ToolCallRecord)
        tool_calls_data = [
            tc.model_dump() if hasattr(tc, 'model_dump') else tc.dict()
            for tc in (agent_result.tool_calls or [])
        ]

        return ChatResponse(
            conversation_id=agent_result.conversation_id,
            response=agent_result.content,
            tool_calls=tool_calls_data
        )

    except Exception as e:
        # Catch any unexpected errors and return user-friendly message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing failed. Please try again. ({str(e)})"
        )