# Research: Phase V Part A - Advanced Features

**Feature**: 011-advanced-features
**Date**: 2026-01-26
**Status**: Complete

---

## Research Areas

### R1: Kafka Client for Python AsyncIO

**Question**: Which Kafka client library works best with FastAPI's async architecture?

**Decision**: `aiokafka`

**Rationale**:
- Native asyncio support, perfect for FastAPI
- Kafka protocol compatible (works with Redpanda)
- Well-maintained, production-ready
- Simple producer API

**Alternatives Considered**:
| Library | Pros | Cons | Verdict |
|---------|------|------|---------|
| aiokafka | Async native, simple API | Smaller community than confluent | SELECTED |
| kafka-python | Popular, stable | Sync only, would block event loop | Rejected |
| confluent-kafka | Official, performant | Requires librdkafka, complex setup | Rejected |

**Implementation Pattern**:
```python
from aiokafka import AIOKafkaProducer
import json

class KafkaEventPublisher:
    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def publish(self, topic: str, event: dict):
        await self.producer.send_and_wait(topic, event)
```

---

### R2: Redpanda Cloud Setup (Recommended Kafka Service)

**Question**: How to set up Redpanda Cloud for Kafka-compatible event streaming?

**Decision**: Use Redpanda Cloud Serverless (FREE tier)

**Setup Steps**:
1. Sign up at https://redpanda.com/cloud
2. Create a Serverless cluster (automatic, free)
3. Create topics: `task-events`, `reminders`, `task-updates`
4. Get bootstrap servers and SASL credentials
5. Configure aiokafka with SASL_SSL

**Connection Configuration**:
```python
producer = AIOKafkaProducer(
    bootstrap_servers="<cluster>.cloud.redpanda.com:9092",
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=os.getenv("REDPANDA_USERNAME"),
    sasl_plain_password=os.getenv("REDPANDA_PASSWORD"),
)
```

**Environment Variables**:
```
KAFKA_BOOTSTRAP_SERVERS=<cluster>.cloud.redpanda.com:9092
REDPANDA_USERNAME=<username>
REDPANDA_PASSWORD=<password>
```

---

### R3: PostgreSQL Full-Text Search vs ILIKE

**Question**: Which search approach for task search feature?

**Decision**: Start with ILIKE, document upgrade path to full-text

**Rationale**:
- ILIKE is simple and sufficient for <1000 tasks per user
- No additional setup or GIN index required initially
- Full-text search can be added later if needed

**ILIKE Implementation**:
```python
from sqlmodel import select, or_

def search_tasks(session, user_id: str, query: str):
    pattern = f"%{query}%"
    statement = select(Task).where(
        Task.user_id == user_id,
        or_(
            Task.title.ilike(pattern),
            Task.description.ilike(pattern)
        )
    )
    return session.exec(statement).all()
```

**Future Full-Text Search (if needed)**:
```sql
-- Add tsvector column
ALTER TABLE tasks ADD COLUMN search_vector tsvector;
CREATE INDEX tasks_search_idx ON tasks USING GIN(search_vector);

-- Update trigger
CREATE TRIGGER tasks_search_update
BEFORE INSERT OR UPDATE ON tasks
FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, description);
```

---

### R4: Recurring Task Date Calculation

**Question**: How to calculate next occurrence dates for recurring tasks?

**Decision**: Use `python-dateutil` for reliable date arithmetic

**Rationale**:
- Handles month boundaries correctly (Jan 31 + 1 month = Feb 28)
- Timezone-aware calculations
- Well-tested, production-grade

**Implementation Pattern**:
```python
from dateutil.relativedelta import relativedelta
from datetime import datetime

def calculate_next_occurrence(current_date: datetime, frequency: str) -> datetime:
    if frequency == "daily":
        return current_date + relativedelta(days=1)
    elif frequency == "weekly":
        return current_date + relativedelta(weeks=1)
    elif frequency == "monthly":
        return current_date + relativedelta(months=1)
    else:
        raise ValueError(f"Unknown frequency: {frequency}")
```

---

### R5: Event Publishing Strategy

**Question**: Should task operations wait for Kafka acknowledgment?

**Decision**: Fire-and-forget with local retry queue

**Rationale**:
- Task CRUD should not fail if Kafka is temporarily unavailable
- Events are important but not critical for immediate user experience
- Retry queue ensures eventual delivery

**Implementation Pattern**:
```python
import asyncio
from collections import deque

class EventPublisher:
    def __init__(self, producer):
        self.producer = producer
        self.retry_queue = deque(maxlen=1000)
        self._retry_task = None

    async def publish(self, topic: str, event: dict):
        try:
            # Fire and forget (with timeout)
            await asyncio.wait_for(
                self.producer.send(topic, event),
                timeout=1.0
            )
        except Exception as e:
            # Queue for retry
            self.retry_queue.append((topic, event))
            self._schedule_retry()

    def _schedule_retry(self):
        if self._retry_task is None or self._retry_task.done():
            self._retry_task = asyncio.create_task(self._retry_loop())

    async def _retry_loop(self):
        while self.retry_queue:
            topic, event = self.retry_queue.popleft()
            try:
                await self.producer.send_and_wait(topic, event)
            except Exception:
                self.retry_queue.append((topic, event))
                await asyncio.sleep(5)  # Backoff
```

---

### R6: Filter Query Composition

**Question**: How to build dynamic filter queries efficiently?

**Decision**: SQLModel query builder with method chaining

**Implementation Pattern**:
```python
from sqlmodel import select, and_
from typing import Optional, List
from datetime import datetime

def build_task_query(
    user_id: str,
    priority: Optional[List[str]] = None,
    tags: Optional[List[int]] = None,
    completed: Optional[bool] = None,
    due_from: Optional[datetime] = None,
    due_to: Optional[datetime] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc"
):
    statement = select(Task).where(Task.user_id == user_id)

    # Priority filter
    if priority:
        statement = statement.where(Task.priority.in_(priority))

    # Completion status
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Due date range
    if due_from:
        statement = statement.where(Task.due_date >= due_from)
    if due_to:
        statement = statement.where(Task.due_date <= due_to)

    # Search
    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(Task.title.ilike(pattern), Task.description.ilike(pattern))
        )

    # Tag filter (requires join)
    if tags:
        statement = statement.join(TaskTag).where(TaskTag.tag_id.in_(tags))

    # Sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    return statement
```

---

### R7: Frontend Date Picker Component

**Question**: Which date picker library for React/Next.js?

**Decision**: Use native HTML date input with `date-fns` for formatting

**Rationale**:
- Native date input is accessible and mobile-friendly
- `date-fns` provides excellent formatting utilities
- No heavy third-party date picker dependency

**Implementation Pattern**:
```tsx
import { format, parseISO, isAfter, isBefore, isToday, isTomorrow } from 'date-fns';

interface DueDatePickerProps {
  value: string | null;
  onChange: (date: string | null) => void;
}

export function DueDatePicker({ value, onChange }: DueDatePickerProps) {
  return (
    <input
      type="date"
      value={value || ''}
      onChange={(e) => onChange(e.target.value || null)}
      className="border rounded px-3 py-2"
    />
  );
}

export function formatDueDate(dateString: string): string {
  const date = parseISO(dateString);
  if (isToday(date)) return 'Today';
  if (isTomorrow(date)) return 'Tomorrow';
  return format(date, 'MMM d');
}

export function getDueDateStatus(dateString: string): 'overdue' | 'today' | 'soon' | 'normal' {
  const date = parseISO(dateString);
  const now = new Date();
  if (isBefore(date, now) && !isToday(date)) return 'overdue';
  if (isToday(date)) return 'today';
  if (isTomorrow(date)) return 'soon';
  return 'normal';
}
```

---

## Summary

All research areas resolved. Key decisions:

| Area | Decision |
|------|----------|
| Kafka Client | aiokafka (async native) |
| Kafka Service | Redpanda Cloud Serverless (FREE) |
| Search | PostgreSQL ILIKE (upgrade path documented) |
| Date Calculations | python-dateutil |
| Event Publishing | Fire-and-forget with retry queue |
| Filter Queries | SQLModel query builder |
| Date Picker | Native HTML + date-fns |

**Next Step**: Proceed to Phase 1 (data-model.md, contracts/)
