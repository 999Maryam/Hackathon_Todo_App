"""Kafka producer service for event publishing.

Provides async event publishing with graceful fallback when Kafka is unavailable.
Uses fire-and-forget pattern with local retry queue for resilience.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional, List
from collections import deque

from app.config import settings

logger = logging.getLogger(__name__)

# Global producer instance
_producer: Optional["KafkaProducer"] = None


class KafkaProducer:
    """Async Kafka producer with retry queue and graceful fallback.

    Features:
    - Fire-and-forget publishing (non-blocking)
    - Local retry queue for failed events
    - Exponential backoff for retries
    - Graceful fallback when Kafka unavailable (logs events)
    """

    # Kafka topics
    TOPIC_TASK_EVENTS = "task-events"
    TOPIC_REMINDERS = "reminders"
    TOPIC_TASK_UPDATES = "task-updates"

    def __init__(self):
        """Initialize Kafka producer."""
        self._producer = None
        self._connected = False
        self._retry_queue: deque = deque(maxlen=1000)  # Max 1000 pending events
        self._retry_task: Optional[asyncio.Task] = None

    async def connect(self) -> bool:
        """Connect to Kafka broker.

        Returns:
            bool: True if connected successfully, False otherwise.
        """
        if not settings.kafka_enabled:
            logger.info("Kafka is disabled via KAFKA_ENABLED=false")
            return False

        try:
            from aiokafka import AIOKafkaProducer

            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers,
                value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
                # Add SASL authentication if credentials provided
                **(
                    {
                        "security_protocol": "SASL_SSL",
                        "sasl_mechanism": "SCRAM-SHA-256",
                        "sasl_plain_username": settings.redpanda_username,
                        "sasl_plain_password": settings.redpanda_password,
                    }
                    if settings.redpanda_username and settings.redpanda_password
                    else {}
                ),
            )
            await self._producer.start()
            self._connected = True
            logger.info(f"Connected to Kafka at {settings.kafka_bootstrap_servers}")

            # Start retry task
            self._retry_task = asyncio.create_task(self._retry_loop())

            return True

        except ImportError:
            logger.warning("aiokafka not installed - Kafka publishing disabled")
            return False
        except Exception as e:
            logger.warning(f"Failed to connect to Kafka: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Kafka broker."""
        if self._retry_task:
            self._retry_task.cancel()
            try:
                await self._retry_task
            except asyncio.CancelledError:
                pass

        if self._producer:
            await self._producer.stop()
            self._producer = None
            self._connected = False
            logger.info("Disconnected from Kafka")

    async def publish(
        self,
        topic: str,
        event: Dict[str, Any],
        key: Optional[str] = None,
    ) -> bool:
        """Publish event to Kafka topic.

        Fire-and-forget pattern - returns immediately.
        Failed events are queued for retry.

        Args:
            topic: Kafka topic name
            event: Event data dictionary
            key: Optional partition key

        Returns:
            bool: True if published or queued, False if failed completely.
        """
        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat()

        if self._connected and self._producer:
            try:
                await self._producer.send_and_wait(
                    topic,
                    value=event,
                    key=key.encode("utf-8") if key else None,
                )
                logger.debug(f"Published event to {topic}: {event.get('event_type', 'unknown')}")
                return True
            except Exception as e:
                logger.warning(f"Failed to publish to {topic}: {e}")
                self._queue_for_retry(topic, event, key)
                return True  # Queued for retry

        # Kafka not connected - log and queue
        logger.info(f"Kafka unavailable - logging event: {topic}/{event.get('event_type', 'unknown')}")
        self._queue_for_retry(topic, event, key)
        return True

    def _queue_for_retry(
        self,
        topic: str,
        event: Dict[str, Any],
        key: Optional[str],
    ) -> None:
        """Queue event for retry."""
        self._retry_queue.append({
            "topic": topic,
            "event": event,
            "key": key,
            "attempts": 0,
            "next_retry": datetime.utcnow(),
        })

    async def _retry_loop(self) -> None:
        """Background task to retry failed events with exponential backoff."""
        while True:
            try:
                await asyncio.sleep(10)  # Check every 10 seconds

                if not self._retry_queue or not self._connected:
                    continue

                now = datetime.utcnow()
                events_to_retry: List[Dict] = []

                # Collect events ready for retry
                while self._retry_queue:
                    item = self._retry_queue[0]
                    if item["next_retry"] <= now:
                        events_to_retry.append(self._retry_queue.popleft())
                    else:
                        break

                # Retry events
                for item in events_to_retry:
                    try:
                        await self._producer.send_and_wait(
                            item["topic"],
                            value=item["event"],
                            key=item["key"].encode("utf-8") if item["key"] else None,
                        )
                        logger.info(f"Retry succeeded for {item['topic']}")
                    except Exception as e:
                        item["attempts"] += 1
                        if item["attempts"] < 5:  # Max 5 retries
                            # Exponential backoff: 10s, 20s, 40s, 80s, 160s
                            backoff = 10 * (2 ** item["attempts"])
                            item["next_retry"] = datetime.utcnow() + asyncio.timedelta(seconds=backoff)
                            self._retry_queue.append(item)
                            logger.warning(f"Retry {item['attempts']} failed for {item['topic']}: {e}")
                        else:
                            logger.error(f"Event dropped after 5 retries: {item['topic']}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in retry loop: {e}")

    @property
    def is_connected(self) -> bool:
        """Check if producer is connected to Kafka."""
        return self._connected

    @property
    def pending_count(self) -> int:
        """Get count of events pending retry."""
        return len(self._retry_queue)


async def get_kafka_producer() -> KafkaProducer:
    """Get or create global Kafka producer instance.

    Returns:
        KafkaProducer: Global producer instance.
    """
    global _producer
    if _producer is None:
        _producer = KafkaProducer()
    return _producer


async def init_kafka() -> None:
    """Initialize Kafka producer on application startup."""
    producer = await get_kafka_producer()
    await producer.connect()


async def shutdown_kafka() -> None:
    """Shutdown Kafka producer on application shutdown."""
    global _producer
    if _producer:
        await _producer.disconnect()
        _producer = None
