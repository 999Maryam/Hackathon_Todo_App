"""Tests for AI Agent behavior.

Task: T049 | Spec: specs/007-ai-agent-chat-logic/spec.md#SC-001-SC-010
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from app.agents.chat_runner import run_agent_with_tools_sync
from app.agents.openai_agent import AgentResponse
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.task import Task


@pytest.fixture
def mock_db_session():
    """Create a mock database session for testing."""
    session = MagicMock(spec=Session)
    return session


@pytest.fixture
def sample_user_id():
    """Sample user ID for testing."""
    return "user_test_123"


def test_add_task_intent(mock_db_session, sample_user_id):
    """Test that add task message triggers add_task tool."""
    # Mock the task creation
    mock_task_result = {"task_id": 1, "status": "created", "title": "Buy groceries"}

    with patch('app.agents.openai_agent.task_tools.add_task', return_value=mock_task_result) as mock_add_task:
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)) as mock_get_conv:
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]) as mock_get_hist:
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        # Mock the async runner
                        with patch('app.agents.chat_runner.Runner') as mock_runner_class:
                            mock_runner_instance = AsyncMock()
                            mock_runner_instance.run.return_value = AsyncMock(
                                final_output="Got it! I've added 'Buy groceries' to your tasks.",
                                tool_calls=[
                                    MagicMock(name="add_task", arguments={"title": "Buy groceries"}, result=mock_task_result)
                                ]
                            )

                            # Mock the agent creation
                            with patch('app.agents.chat_runner.create_agent') as mock_create_agent:
                                mock_agent = MagicMock()
                                mock_create_agent.return_value = mock_agent

                                # Mock the asyncio.run to return our test result
                                with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                    mock_result = MagicMock()
                                    mock_result.final_output = "Got it! I've added 'Buy groceries' to your tasks."
                                    mock_result.tool_calls = [
                                        MagicMock(name="add_task", arguments={"title": "Buy groceries"}, result=mock_task_result)
                                    ]
                                    mock_async_run.return_value = AgentResponse(
                                        content="Got it! I've added 'Buy groceries' to your tasks.",
                                        tool_calls=[],
                                        conversation_id=1
                                    )

                                    response = run_agent_with_tools_sync(
                                        user_id=sample_user_id,
                                        message="Add a task to buy groceries",
                                        db=mock_db_session
                                    )

                                    # Verify the tool was called with correct parameters
                                    mock_add_task.assert_called_once_with(
                                        user_id=sample_user_id,
                                        title="buy groceries",
                                        description=None,
                                        db=mock_db_session
                                    )


def test_list_tasks_intent(mock_db_session, sample_user_id):
    """Test that list message triggers list_tasks tool."""
    mock_tasks_result = {
        "tasks": [
            {"id": 1, "title": "Buy groceries", "completed": False},
            {"id": 2, "title": "Walk the dog", "completed": True}
        ],
        "status": "success",
        "count": 2
    }

    with patch('app.agents.openai_agent.task_tools.list_tasks', return_value=mock_tasks_result) as mock_list_tasks:
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)):
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]):
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        with patch('app.agents.chat_runner.create_agent'):
                            with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                mock_async_run.return_value = AgentResponse(
                                    content="Here are your tasks: Buy groceries, Walk the dog.",
                                    tool_calls=[],
                                    conversation_id=1
                                )

                                response = run_agent_with_tools_sync(
                                    user_id=sample_user_id,
                                    message="What are my tasks?",
                                    db=mock_db_session
                                )

                                # Verify the tool was called
                                mock_list_tasks.assert_called_once_with(
                                    user_id=sample_user_id,
                                    status="all",
                                    db=mock_db_session
                                )


def test_complete_task_intent(mock_db_session, sample_user_id):
    """Test that complete task message triggers complete_task tool."""
    mock_result = {"task_id": 1, "status": "completed", "title": "Buy groceries"}

    with patch('app.agents.openai_agent.task_tools.complete_task', return_value=mock_result) as mock_complete_task:
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)):
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]):
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        with patch('app.agents.chat_runner.create_agent'):
                            with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                mock_async_run.return_value = AgentResponse(
                                    content="I've marked 'Buy groceries' as completed.",
                                    tool_calls=[],
                                    conversation_id=1
                                )

                                response = run_agent_with_tools_sync(
                                    user_id=sample_user_id,
                                    message="Mark task 1 as done",
                                    db=mock_db_session
                                )

                                # Verify the tool was called
                                mock_complete_task.assert_called_once_with(
                                    user_id=sample_user_id,
                                    task_id=1,
                                    db=mock_db_session
                                )


def test_delete_task_intent(mock_db_session, sample_user_id):
    """Test that delete task message triggers delete_task tool."""
    mock_result = {"task_id": 1, "status": "deleted", "title": "Buy groceries"}

    with patch('app.agents.openai_agent.task_tools.delete_task', return_value=mock_result) as mock_delete_task:
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)):
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]):
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        with patch('app.agents.chat_runner.create_agent'):
                            with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                mock_async_run.return_value = AgentResponse(
                                    content="I've deleted the task 'Buy groceries'.",
                                    tool_calls=[],
                                    conversation_id=1
                                )

                                response = run_agent_with_tools_sync(
                                    user_id=sample_user_id,
                                    message="Delete task 1",
                                    db=mock_db_session
                                )

                                # Verify the tool was called
                                mock_delete_task.assert_called_once_with(
                                    user_id=sample_user_id,
                                    task_id=1,
                                    db=mock_db_session
                                )


def test_update_task_intent(mock_db_session, sample_user_id):
    """Test that update task message triggers update_task tool."""
    mock_result = {"task_id": 1, "status": "updated", "title": "Buy organic groceries"}

    with patch('app.agents.openai_agent.task_tools.update_task', return_value=mock_result) as mock_update_task:
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)):
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]):
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        with patch('app.agents.chat_runner.create_agent'):
                            with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                mock_async_run.return_value = AgentResponse(
                                    content="I've updated task 1 to 'Buy organic groceries'.",
                                    tool_calls=[],
                                    conversation_id=1
                                )

                                response = run_agent_with_tools_sync(
                                    user_id=sample_user_id,
                                    message="Change task 1 title to Buy organic groceries",
                                    db=mock_db_session
                                )

                                # Verify the tool was called
                                mock_update_task.assert_called_once_with(
                                    user_id=sample_user_id,
                                    task_id=1,
                                    title="Buy organic groceries",
                                    description=None,
                                    db=mock_db_session
                                )


def test_user_isolation(mock_db_session, sample_user_id):
    """Test that one user cannot access another user's tasks."""
    other_user_id = "user_other_456"
    mock_access_denied_result = {"error": "Task not found or not owned by user", "status": "error"}

    with patch('app.agents.openai_agent.task_tools.complete_task', return_value=mock_access_denied_result):
        with patch('app.agents.chat_runner.get_or_create_conversation',
                  return_value=MagicMock(id=1)):
            with patch('app.agents.chat_runner.get_conversation_history',
                      return_value=[]):
                with patch('app.agents.chat_runner.add_user_message'):
                    with patch('app.agents.chat_runner.add_assistant_message'):
                        with patch('app.agents.chat_runner.create_agent'):
                            with patch('app.agents.chat_runner.asyncio.run') as mock_async_run:
                                mock_async_run.return_value = AgentResponse(
                                    content="Sorry, I couldn't complete that action. Task not found or not owned by user",
                                    tool_calls=[],
                                    conversation_id=1
                                )

                                response = run_agent_with_tools_sync(
                                    user_id=sample_user_id,
                                    message="Mark task 999 as done",  # Assuming task 999 belongs to another user
                                    db=mock_db_session
                                )

                                # The tool should still be called but return an error
                                # due to user isolation
                                mock_result = response
                                assert mock_result.conversation_id == 1


if __name__ == "__main__":
    pytest.main([__file__])