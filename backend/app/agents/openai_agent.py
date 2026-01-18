"""OpenRouter Agent configuration for Todo AI Chatbot.

Task: T006 | Spec: specs/007-ai-agent-chat-logic/spec.md#FR-001-FR-009
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from openai import OpenAI

from app.tools import task_tools
from app.config import settings


# Load environment variables
load_dotenv(find_dotenv())

# Load system prompt
PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"
try:
    SYSTEM_PROMPT = PROMPT_PATH.read_text()
except FileNotFoundError:
    # Fallback system prompt when file doesn't exist
    SYSTEM_PROMPT = "You are a helpful assistant for managing tasks. You can help users add, list, update, complete, and delete tasks."


# Configure OpenRouter API
client = OpenAI(
    api_key=settings.openrouter_api_key,
    base_url=settings.base_url or "https://openrouter.ai/api/v1"
)

# Store model name and system prompt for dynamic model creation
MODEL_NAME = settings.openrouter_model or "mistralai/devstral-2512:free"
SYSTEM_PROMPT_CONTENT = SYSTEM_PROMPT


def get_model(model_name: str = None):
    """Get an OpenRouter model client with fallback handling."""
    if model_name is None:
        model_name = MODEL_NAME

    # Return a simple wrapper that holds the model name and client
    class OpenRouterModel:
        def __init__(self, client, model_name, system_prompt):
            self.client = client
            self.model_name = model_name
            self.system_prompt = system_prompt

        def start_chat(self, history=None):
            return OpenRouterChat(self, history or [])

    return OpenRouterModel(client, model_name, SYSTEM_PROMPT_CONTENT)


class OpenRouterChat:
    def __init__(self, model, history=None):
        self.model = model
        self.history = history or []

    def send_message(self, message: str):
        # Add user message to history
        self.history.append({"role": "user", "content": message})

        # Prepare messages for API call
        messages = [{"role": "system", "content": self.model.system_prompt}]
        messages.extend(self.history)

        try:
            # Call OpenRouter API with function calling support
            response = self.model.client.chat.completions.create(
                model=self.model.model_name,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool["description"],
                        "parameters": tool["parameters"]
                    }
                } for tool in TOOLS_DEFINITION],
                tool_choice="auto",  # Auto-select tools based on user request
                temperature=0.7,
            )

            # Check if the model wants to call a function
            choice = response.choices[0]
            message_obj = choice.message

            # Create a mock response object
            class MockResponse:
                def __init__(self, text, function_call=None):
                    self.text = text
                    self.candidates = []

                    # Create a candidate-like structure for function calls
                    if function_call:
                        class MockCandidate:
                            def __init__(self, func_call):
                                class MockContent:
                                    def __init__(self, fc):
                                        class MockPart:
                                            def __init__(self, function_call):
                                                self.function_call = function_call

                                        self.parts = [MockPart(fc)]

                                self.content = MockContent(func_call)

                        self.candidates = [MockCandidate(function_call)]

            # Check if there are tool calls
            if choice.finish_reason == "tool_calls" and message_obj.tool_calls:
                # Process tool calls
                tool_calls = message_obj.tool_calls
                final_response = ""

                for tool_call in tool_calls:
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        # Fallback if JSON parsing fails
                        function_args = {}

                    function_name = tool_call.function.name

                    # Execute the tool call
                    # Note: This is simplified - in a real implementation, you'd need to handle this differently
                    final_response += f"[Function {function_name} called with args: {function_args}] "

                # Add assistant response to history
                self.history.append({"role": "assistant", "content": final_response})

                # Create response with function call info
                try:
                    func_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    func_args = {}

                class MockFunctionCall:
                    def __init__(self, name, args):
                        self.name = name
                        self.args = args

                return MockResponse(final_response, MockFunctionCall(tool_call.function.name, func_args))

            else:
                # Regular response without tool calls
                response_content = message_obj.content
                if not response_content:
                    response_content = "I processed your request but don't have a specific response."

                # Add assistant response to history
                self.history.append({"role": "assistant", "content": response_content})

                return MockResponse(response_content)

        except Exception as e:
            # Return error message if API call fails
            error_msg = f"Error calling OpenRouter API: {str(e)}"
            class MockResponse:
                def __init__(self, text):
                    self.text = text
                    self.candidates = []

            return MockResponse(error_msg)


model = get_model()


# Define Pydantic models for responses
class ToolCallRecord(BaseModel):
    name: str
    arguments: dict
    result: dict


class AgentResponse(BaseModel):
    content: str
    tool_calls: list[ToolCallRecord]
    conversation_id: int


# Tool definitions for function calling simulation
TOOLS_DEFINITION = [
    {
        "name": "add_task",
        "description": "Add a new task to your list",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "The title of the task to add"},
                "description": {"type": "string", "description": "Optional description for the task"}
            },
            "required": ["title"]
        }
    },
    {
        "name": "list_tasks",
        "description": "List your tasks with optional filtering",
        "parameters": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "description": "Filter tasks by status (all, pending, completed)", "enum": ["all", "pending", "completed"]}
            },
            "required": []
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as complete using its task number (1, 2, 3...)",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The task number (1, 2, 3...) to mark as complete"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task permanently using its task number (1, 2, 3...)",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The task number (1, 2, 3...) to delete"}
            },
            "required": ["task_id"]
        }
    },
    {
        "name": "update_task",
        "description": "Update a task's title and/or description using its task number (1, 2, 3...)",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {"type": "integer", "description": "The task number (1, 2, 3...) to update"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {"type": "string", "description": "New description (optional)"}
            },
            "required": ["task_id"]
        }
    }
]


def execute_tool_call(name: str, arguments: dict, user_id: str, db) -> dict:
    """Execute a tool call with the provided context."""
    if name == "add_task":
        return task_tools.add_task(
            user_id=user_id,
            title=arguments.get("title"),
            description=arguments.get("description"),
            db=db
        )
    elif name == "list_tasks":
        return task_tools.list_tasks(
            user_id=user_id,
            status=arguments.get("status", "all"),
            db=db
        )
    elif name == "complete_task":
        return task_tools.complete_task(
            user_id=user_id,
            task_id=arguments.get("task_id"),
            db=db
        )
    elif name == "delete_task":
        return task_tools.delete_task(
            user_id=user_id,
            task_id=arguments.get("task_id"),
            db=db
        )
    elif name == "update_task":
        return task_tools.update_task(
            user_id=user_id,
            task_id=arguments.get("task_id"),
            title=arguments.get("title"),
            description=arguments.get("description"),
            db=db
        )
    else:
        raise ValueError(f"Unknown tool: {name}")


def create_agent():
    """Create a configured agent instance (returns the model)."""
    return get_model()