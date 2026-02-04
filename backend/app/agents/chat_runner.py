"""Stateless chat runner for Todo AI Chatbot.

Task: T034-T040 | Spec: specs/007-ai-agent-chat-logic/spec.md#FR-010-FR-019
"""

from typing import Any, List, Dict
from pydantic import BaseModel
from sqlmodel import Session
import asyncio
import json
import re
import logging

from app.agents.openai_agent import create_agent, ToolCallRecord, AgentResponse, execute_tool_call, TOOLS_DEFINITION
from app.services.conversation_service import (
    get_or_create_conversation,
    get_conversation_history,
    add_user_message,
    add_assistant_message
)


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

    try:
        # Get or create conversation
        conversation = get_or_create_conversation(user_id, db)
        conv_id = conversation.id

        # Load history
        history = get_conversation_history(conv_id, user_id, db)
    except Exception as e:
        db.rollback()
        logging.error(f"Error loading conversation for user {user_id}: {str(e)}")
        raise

    # Create agent
    agent = create_agent()

    # Prepare conversation history for the model (OpenAI-compatible format)
    # Only include messages with valid roles and non-empty content
    chat_history = []
    for msg in history:
        role = msg.get("role", "")
        content = msg.get("content", "")
        if not content or not content.strip():
            continue
        # Map to OpenAI-compatible roles (user/assistant only)
        if role == "user":
            chat_history.append({"role": "user", "content": content})
        else:
            chat_history.append({"role": "assistant", "content": content})

    # Create a chat session with the history
    chat = agent.start_chat(history=chat_history)

    # Send the new message to the model
    response = chat.send_message(message)

    # Extract text response
    response_text = response.text

    # Process potential function calls in the response
    tool_calls = []

    # Check for structured function calls in the response
    # The model may return structured function call information
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'function_call'):
                        # This is a function call from the model
                        func_call = part.function_call
                        tool_name = func_call.name

                        # Convert the arguments to a dictionary
                        arguments = {}
                        if hasattr(func_call, 'args'):
                            for key, value in func_call.args.items():
                                arguments[key] = value
                        elif hasattr(func_call, 'arguments'):
                            # In case arguments are stored differently
                            arguments = func_call.arguments

                        # Execute the tool call with proper error handling
                        try:
                            result = execute_tool_call(tool_name, arguments, user_id, db)
                        except Exception as e:
                            db.rollback()
                            logging.error(f"Error executing tool {tool_name}: {str(e)}")
                            result = {"error": str(e), "status": "error"}

                        # Create tool call record
                        tool_call_record = ToolCallRecord(
                            name=tool_name,
                            arguments=arguments,
                            result=result
                        )
                        tool_calls.append(tool_call_record)

                        # Update the response text to include the tool result
                        response_text += f"\n\nResult: {result}"

    # Save messages to database with error handling
    try:
        add_user_message(conv_id, user_id, message, db)
        add_assistant_message(conv_id, user_id, response_text, db)
    except Exception as e:
        db.rollback()
        logging.error(f"Error saving messages for user {user_id}: {str(e)}")
        # Continue anyway - we still want to return the response

    return AgentResponse(
        content=response_text,
        tool_calls=tool_calls,
        conversation_id=conv_id
    )


def run_agent_with_tools_sync(
    user_id: str,
    message: str,
    conversation_id: int | None = None,
    db: Session = None
) -> AgentResponse:
    """Sync wrapper for run_agent_with_tools."""
    # Since the agent runner is async, we need to run it in an event loop
    try:
        loop = asyncio.get_running_loop()
        # If we're already in a loop, schedule the coroutine
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                lambda: asyncio.run(run_agent_with_tools(user_id, message, conversation_id, db))
            )
            return future.result()
    except RuntimeError:
        # No event loop running, safe to call asyncio.run
        return asyncio.run(run_agent_with_tools(user_id, message, conversation_id, db))
