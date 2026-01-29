"""Event publisher for task lifecycle events.

Phase V US9: Publishes task events to Kafka for downstream processing.
Provides sync-friendly interface for TaskService integration.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.models.task import Task
from app.schemas.events import TaskEvent, TaskUpdateEvent, ReminderEvent

logger = logging.getLogger(__name__)


class EventPublisher:
    """Publisher for task and reminder events.

    Provides sync-friendly fire-and-forget event publishing.
    Events are logged for audit trail even when Kafka is unavailable.
    """

    # Event types
    EVENT_TASK_CREATED = "task_created"
    EVENT_TASK_UPDATED = "task_updated"
    EVENT_TASK_COMPLETED = "task_completed"
    EVENT_TASK_DELETED = "task_deleted"
    EVENT_REMINDER_DUE = "reminder_due"

    @staticmethod
    def _task_to_dict(task: Task) -> Dict[str, Any]:
        """Convert task to dictionary for event payload."""
        return {
            "id": str(task.id),
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "is_recurring": task.is_recurring,
            "recurring_config_id": task.recurring_config_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        }

    @staticmethod
    def _schedule_publish(topic: str, event_dict: Dict[str, Any], key: Optional[str] = None) -> None:
        """Schedule async publish without blocking.

        Uses asyncio to fire-and-forget the publish operation.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Create task in running loop
                asyncio.create_task(EventPublisher._async_publish(topic, event_dict, key))
            else:
                # No running loop - just log
                logger.info(f"Event logged (no event loop): {topic}/{event_dict.get('event_type')}")
        except RuntimeError:
            # No event loop available - just log
            logger.info(f"Event logged (no event loop): {topic}/{event_dict.get('event_type')}")

    @staticmethod
    async def _async_publish(topic: str, event_dict: Dict[str, Any], key: Optional[str] = None) -> None:
        """Async publish to Kafka."""
        try:
            from app.services.kafka_producer import get_kafka_producer, KafkaProducer

            producer = await get_kafka_producer()
            await producer.publish(topic, event_dict, key)
        except Exception as e:
            logger.error(f"Failed to publish event to {topic}: {e}")

    @staticmethod
    def publish_task_created(task: Task) -> None:
        """Publish task_created event.

        T101: Called after TaskService.create_task().
        T107: Logs event for audit trail.

        Args:
            task: The created task.
        """
        event = TaskEvent(
            event_type=EventPublisher.EVENT_TASK_CREATED,
            task_id=str(task.id),
            task_data=EventPublisher._task_to_dict(task),
            user_id=task.user_id,
        )

        event_dict = event.model_dump()

        # T107: Log for audit trail
        logger.info(
            f"AUDIT: {EventPublisher.EVENT_TASK_CREATED} | "
            f"task_id={task.id} | user_id={task.user_id} | title={task.title}"
        )

        # Publish to Kafka
        from app.services.kafka_producer import KafkaProducer
        EventPublisher._schedule_publish(
            KafkaProducer.TOPIC_TASK_EVENTS,
            event_dict,
            key=task.user_id
        )

    @staticmethod
    def publish_task_updated(
        task: Task,
        changed_fields: Optional[List[str]] = None,
        previous_values: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Publish task_updated event.

        T102: Called after TaskService.update_task().
        T107: Logs event for audit trail.

        Args:
            task: The updated task.
            changed_fields: List of field names that changed.
            previous_values: Previous values of changed fields.
        """
        event = TaskUpdateEvent(
            event_type=EventPublisher.EVENT_TASK_UPDATED,
            task_id=str(task.id),
            task_data=EventPublisher._task_to_dict(task),
            user_id=task.user_id,
            changed_fields=changed_fields or [],
            previous_values=previous_values or {},
        )

        event_dict = event.model_dump()

        # T107: Log for audit trail
        logger.info(
            f"AUDIT: {EventPublisher.EVENT_TASK_UPDATED} | "
            f"task_id={task.id} | user_id={task.user_id} | "
            f"changed={changed_fields or []}"
        )

        # Publish to Kafka
        from app.services.kafka_producer import KafkaProducer
        EventPublisher._schedule_publish(
            KafkaProducer.TOPIC_TASK_EVENTS,
            event_dict,
            key=task.user_id
        )

    @staticmethod
    def publish_task_completed(task: Task) -> None:
        """Publish task_completed event.

        T103: Called after TaskService.toggle_complete() when completing.
        T107: Logs event for audit trail.

        Args:
            task: The completed task.
        """
        event = TaskEvent(
            event_type=EventPublisher.EVENT_TASK_COMPLETED,
            task_id=str(task.id),
            task_data=EventPublisher._task_to_dict(task),
            user_id=task.user_id,
        )

        event_dict = event.model_dump()

        # T107: Log for audit trail
        logger.info(
            f"AUDIT: {EventPublisher.EVENT_TASK_COMPLETED} | "
            f"task_id={task.id} | user_id={task.user_id} | title={task.title}"
        )

        # Publish to Kafka
        from app.services.kafka_producer import KafkaProducer
        EventPublisher._schedule_publish(
            KafkaProducer.TOPIC_TASK_EVENTS,
            event_dict,
            key=task.user_id
        )

    @staticmethod
    def publish_task_deleted(task_id: str, user_id: str, task_title: str) -> None:
        """Publish task_deleted event.

        T104: Called after TaskService.delete_task().
        T107: Logs event for audit trail.

        Args:
            task_id: The deleted task's ID.
            user_id: The task owner's ID.
            task_title: The task title (for logging).
        """
        event = TaskEvent(
            event_type=EventPublisher.EVENT_TASK_DELETED,
            task_id=task_id,
            task_data={"id": task_id, "deleted": True},
            user_id=user_id,
        )

        event_dict = event.model_dump()

        # T107: Log for audit trail
        logger.info(
            f"AUDIT: {EventPublisher.EVENT_TASK_DELETED} | "
            f"task_id={task_id} | user_id={user_id} | title={task_title}"
        )

        # Publish to Kafka
        from app.services.kafka_producer import KafkaProducer
        EventPublisher._schedule_publish(
            KafkaProducer.TOPIC_TASK_EVENTS,
            event_dict,
            key=user_id
        )

    @staticmethod
    def publish_reminder_due(
        task_id: str,
        task_title: str,
        due_at: datetime,
        remind_at: datetime,
        user_id: str,
    ) -> None:
        """Publish reminder_due event.

        T105: Called when a reminder is due to be sent.
        T107: Logs event for audit trail.

        Args:
            task_id: The task's ID.
            task_title: The task title.
            due_at: The task's due date.
            remind_at: The reminder time.
            user_id: The task owner's ID.
        """
        event = ReminderEvent(
            task_id=task_id,
            title=task_title,
            due_at=due_at,
            remind_at=remind_at,
            user_id=user_id,
        )

        event_dict = event.model_dump()

        # T107: Log for audit trail
        logger.info(
            f"AUDIT: {EventPublisher.EVENT_REMINDER_DUE} | "
            f"task_id={task_id} | user_id={user_id} | title={task_title}"
        )

        # Publish to Kafka
        from app.services.kafka_producer import KafkaProducer
        EventPublisher._schedule_publish(
            KafkaProducer.TOPIC_REMINDERS,
            event_dict,
            key=user_id
        )
