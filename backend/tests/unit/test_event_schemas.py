"""Unit tests for event schema serialization (T108, T109).

Phase V US9: Verifies TaskEvent and ReminderEvent schemas serialize correctly
for Kafka publishing.
"""

import json
import uuid
from datetime import datetime, timedelta

import pytest

from app.schemas.events import TaskEvent, TaskUpdateEvent, ReminderEvent


# =============================================================================
# T108: TaskEvent Schema Compliance Tests
# =============================================================================


class TestTaskEventSerialization:
    """Test TaskEvent schema serialization for Kafka publishing."""

    @pytest.mark.unit
    def test_task_event_creation(self):
        """T108: TaskEvent creates with all required fields."""
        task_id = str(uuid.uuid4())
        user_id = "user-123"
        event = TaskEvent(
            event_type="task_created",
            task_id=task_id,
            task_data={"id": task_id, "title": "Test task"},
            user_id=user_id,
        )

        assert event.event_type == "task_created"
        assert event.task_id == task_id
        assert event.task_data["title"] == "Test task"
        assert event.user_id == user_id
        assert event.timestamp is not None

    @pytest.mark.unit
    def test_task_event_timestamp_default(self):
        """T108: TaskEvent auto-generates timestamp if not provided."""
        before = datetime.utcnow()
        event = TaskEvent(
            event_type="task_created",
            task_id="task-123",
            task_data={"id": "task-123"},
            user_id="user-123",
        )
        after = datetime.utcnow()

        assert before <= event.timestamp <= after

    @pytest.mark.unit
    def test_task_event_timestamp_custom(self):
        """T108: TaskEvent accepts custom timestamp."""
        custom_time = datetime(2025, 1, 15, 12, 0, 0)
        event = TaskEvent(
            event_type="task_updated",
            task_id="task-123",
            task_data={"id": "task-123"},
            user_id="user-123",
            timestamp=custom_time,
        )

        assert event.timestamp == custom_time

    @pytest.mark.unit
    def test_task_event_model_dump(self):
        """T108: TaskEvent model_dump returns correct structure."""
        task_id = str(uuid.uuid4())
        timestamp = datetime(2025, 1, 15, 12, 0, 0)
        task_data = {
            "id": task_id,
            "title": "Test task",
            "completed": False,
            "priority": "high",
        }

        event = TaskEvent(
            event_type="task_created",
            task_id=task_id,
            task_data=task_data,
            user_id="user-123",
            timestamp=timestamp,
        )

        dump = event.model_dump()

        assert dump["event_type"] == "task_created"
        assert dump["task_id"] == task_id
        assert dump["task_data"] == task_data
        assert dump["user_id"] == "user-123"
        assert dump["timestamp"] == timestamp

    @pytest.mark.unit
    def test_task_event_json_serialization(self):
        """T108: TaskEvent serializes to JSON correctly."""
        task_id = str(uuid.uuid4())
        timestamp = datetime(2025, 1, 15, 12, 0, 0)
        task_data = {
            "id": task_id,
            "title": "Test task",
            "due_date": "2025-01-20T10:00:00",
        }

        event = TaskEvent(
            event_type="task_created",
            task_id=task_id,
            task_data=task_data,
            user_id="user-123",
            timestamp=timestamp,
        )

        # Serialize to JSON
        json_str = event.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["event_type"] == "task_created"
        assert parsed["task_id"] == task_id
        assert parsed["user_id"] == "user-123"
        # Timestamp should be ISO format string
        assert "2025-01-15" in parsed["timestamp"]

    @pytest.mark.unit
    def test_task_event_all_event_types(self):
        """T108: TaskEvent works with all event types."""
        event_types = ["task_created", "task_updated", "task_completed", "task_deleted"]

        for event_type in event_types:
            event = TaskEvent(
                event_type=event_type,
                task_id="task-123",
                task_data={"id": "task-123"},
                user_id="user-123",
            )
            assert event.event_type == event_type


class TestTaskUpdateEventSerialization:
    """Test TaskUpdateEvent extended schema serialization."""

    @pytest.mark.unit
    def test_task_update_event_with_changes(self):
        """T108: TaskUpdateEvent includes changed_fields and previous_values."""
        task_id = str(uuid.uuid4())
        event = TaskUpdateEvent(
            event_type="task_updated",
            task_id=task_id,
            task_data={"id": task_id, "title": "New title", "priority": "high"},
            user_id="user-123",
            changed_fields=["title", "priority"],
            previous_values={"title": "Old title", "priority": "medium"},
        )

        assert event.changed_fields == ["title", "priority"]
        assert event.previous_values["title"] == "Old title"
        assert event.previous_values["priority"] == "medium"

    @pytest.mark.unit
    def test_task_update_event_defaults(self):
        """T108: TaskUpdateEvent has empty defaults for change tracking."""
        event = TaskUpdateEvent(
            event_type="task_updated",
            task_id="task-123",
            task_data={"id": "task-123"},
            user_id="user-123",
        )

        assert event.changed_fields == []
        assert event.previous_values == {}

    @pytest.mark.unit
    def test_task_update_event_json_serialization(self):
        """T108: TaskUpdateEvent serializes change tracking to JSON."""
        event = TaskUpdateEvent(
            event_type="task_updated",
            task_id="task-123",
            task_data={"id": "task-123", "title": "Updated"},
            user_id="user-123",
            changed_fields=["title"],
            previous_values={"title": "Original"},
            timestamp=datetime(2025, 1, 15, 12, 0, 0),
        )

        json_str = event.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["changed_fields"] == ["title"]
        assert parsed["previous_values"] == {"title": "Original"}


# =============================================================================
# T109: ReminderEvent Schema Compliance Tests
# =============================================================================


class TestReminderEventSerialization:
    """Test ReminderEvent schema serialization for Kafka publishing."""

    @pytest.mark.unit
    def test_reminder_event_creation(self):
        """T109: ReminderEvent creates with all required fields."""
        task_id = str(uuid.uuid4())
        due_at = datetime(2025, 1, 20, 10, 0, 0)
        remind_at = datetime(2025, 1, 20, 9, 0, 0)

        event = ReminderEvent(
            task_id=task_id,
            title="Complete report",
            due_at=due_at,
            remind_at=remind_at,
            user_id="user-123",
        )

        assert event.task_id == task_id
        assert event.title == "Complete report"
        assert event.due_at == due_at
        assert event.remind_at == remind_at
        assert event.user_id == "user-123"
        assert event.timestamp is not None

    @pytest.mark.unit
    def test_reminder_event_timestamp_default(self):
        """T109: ReminderEvent auto-generates timestamp if not provided."""
        before = datetime.utcnow()
        event = ReminderEvent(
            task_id="task-123",
            title="Test task",
            due_at=datetime.utcnow() + timedelta(hours=1),
            remind_at=datetime.utcnow(),
            user_id="user-123",
        )
        after = datetime.utcnow()

        assert before <= event.timestamp <= after

    @pytest.mark.unit
    def test_reminder_event_model_dump(self):
        """T109: ReminderEvent model_dump returns correct structure."""
        task_id = str(uuid.uuid4())
        due_at = datetime(2025, 1, 20, 10, 0, 0)
        remind_at = datetime(2025, 1, 20, 9, 0, 0)
        timestamp = datetime(2025, 1, 20, 9, 0, 0)

        event = ReminderEvent(
            task_id=task_id,
            title="Test reminder",
            due_at=due_at,
            remind_at=remind_at,
            user_id="user-123",
            timestamp=timestamp,
        )

        dump = event.model_dump()

        assert dump["task_id"] == task_id
        assert dump["title"] == "Test reminder"
        assert dump["due_at"] == due_at
        assert dump["remind_at"] == remind_at
        assert dump["user_id"] == "user-123"
        assert dump["timestamp"] == timestamp

    @pytest.mark.unit
    def test_reminder_event_json_serialization(self):
        """T109: ReminderEvent serializes all datetime fields to JSON correctly."""
        task_id = str(uuid.uuid4())
        due_at = datetime(2025, 1, 20, 10, 0, 0)
        remind_at = datetime(2025, 1, 20, 9, 0, 0)
        timestamp = datetime(2025, 1, 20, 9, 0, 0)

        event = ReminderEvent(
            task_id=task_id,
            title="Test reminder",
            due_at=due_at,
            remind_at=remind_at,
            user_id="user-123",
            timestamp=timestamp,
        )

        # Serialize to JSON
        json_str = event.model_dump_json()
        parsed = json.loads(json_str)

        assert parsed["task_id"] == task_id
        assert parsed["title"] == "Test reminder"
        assert parsed["user_id"] == "user-123"
        # All datetime fields should be ISO format strings
        assert "2025-01-20" in parsed["due_at"]
        assert "2025-01-20" in parsed["remind_at"]
        assert "2025-01-20" in parsed["timestamp"]

    @pytest.mark.unit
    def test_reminder_event_remind_at_before_due_at(self):
        """T109: ReminderEvent can have remind_at before due_at (expected usage)."""
        due_at = datetime(2025, 1, 20, 10, 0, 0)
        remind_at = due_at - timedelta(hours=1)  # 1 hour before

        event = ReminderEvent(
            task_id="task-123",
            title="Test task",
            due_at=due_at,
            remind_at=remind_at,
            user_id="user-123",
        )

        assert event.remind_at < event.due_at

    @pytest.mark.unit
    def test_reminder_event_json_roundtrip(self):
        """T109: ReminderEvent survives JSON roundtrip for Kafka compatibility."""
        task_id = str(uuid.uuid4())
        due_at = datetime(2025, 1, 20, 10, 0, 0)
        remind_at = datetime(2025, 1, 20, 9, 0, 0)

        event = ReminderEvent(
            task_id=task_id,
            title="Roundtrip test",
            due_at=due_at,
            remind_at=remind_at,
            user_id="user-123",
        )

        # Serialize to JSON then parse back
        json_str = event.model_dump_json()
        parsed = json.loads(json_str)

        # Verify all required fields survive roundtrip
        assert "task_id" in parsed
        assert "title" in parsed
        assert "due_at" in parsed
        assert "remind_at" in parsed
        assert "user_id" in parsed
        assert "timestamp" in parsed

        # Values should match
        assert parsed["task_id"] == task_id
        assert parsed["title"] == "Roundtrip test"
        assert parsed["user_id"] == "user-123"


# =============================================================================
# Kafka Integration Compatibility Tests
# =============================================================================


class TestKafkaMessageCompatibility:
    """Test event schemas are compatible with Kafka message format."""

    @pytest.mark.unit
    def test_task_event_as_kafka_value(self):
        """Events can be serialized as Kafka message values (bytes)."""
        event = TaskEvent(
            event_type="task_created",
            task_id="task-123",
            task_data={"id": "task-123", "title": "Test"},
            user_id="user-123",
        )

        # Kafka expects bytes
        json_bytes = event.model_dump_json().encode("utf-8")
        assert isinstance(json_bytes, bytes)
        assert len(json_bytes) > 0

    @pytest.mark.unit
    def test_reminder_event_as_kafka_value(self):
        """ReminderEvent can be serialized as Kafka message value (bytes)."""
        event = ReminderEvent(
            task_id="task-123",
            title="Test task",
            due_at=datetime.utcnow() + timedelta(hours=1),
            remind_at=datetime.utcnow(),
            user_id="user-123",
        )

        # Kafka expects bytes
        json_bytes = event.model_dump_json().encode("utf-8")
        assert isinstance(json_bytes, bytes)
        assert len(json_bytes) > 0

    @pytest.mark.unit
    def test_event_key_from_user_id(self):
        """User ID can be used as Kafka partition key."""
        event = TaskEvent(
            event_type="task_created",
            task_id="task-123",
            task_data={"id": "task-123"},
            user_id="user-123",
        )

        # Key for partitioning
        key = event.user_id.encode("utf-8")
        assert isinstance(key, bytes)
        assert key == b"user-123"
