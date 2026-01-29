# Data Model: Phase V Part A - Advanced Features

**Feature**: 011-advanced-features
**Date**: 2026-01-26
**Status**: Complete

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id (PK)         │
│ email           │
│ name            │
│ password_hash   │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         │ *
┌────────▼────────┐         ┌─────────────────┐
│      Task       │         │       Tag       │
│─────────────────│         │─────────────────│
│ id (PK)         │         │ id (PK)         │
│ user_id (FK)    │◀────────│ user_id (FK)    │
│ title           │    *  * │ name            │
│ description     │◀───────▶│ created_at      │
│ completed       │ TaskTag └─────────────────┘
│ priority        │ (M:M)
│ due_date        │
│ is_recurring    │         ┌─────────────────┐
│ recurring_id(FK)│────────▶│ RecurringConfig │
│ created_at      │    1    │─────────────────│
│ updated_at      │         │ id (PK)         │
└────────┬────────┘         │ frequency       │
         │ 1                │ next_occurrence │
         │                  │ created_at      │
         │ *                └─────────────────┘
┌────────▼────────┐
│    Reminder     │
│─────────────────│
│ id (PK)         │
│ task_id (FK)    │
│ remind_at       │
│ sent            │
│ created_at      │
└─────────────────┘
```

---

## Entity Definitions

### Task (Extended)

Extends existing Task model with new fields for advanced features.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Task identifier |
| user_id | VARCHAR(255) | FK → users.id, NOT NULL | Owner reference |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Task details |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| **priority** | VARCHAR(10) | DEFAULT 'medium' | NEW: high/medium/low |
| **due_date** | TIMESTAMP | NULLABLE | NEW: Task deadline |
| **is_recurring** | BOOLEAN | DEFAULT FALSE | NEW: Recurrence flag |
| **recurring_config_id** | INTEGER | FK → recurring_configs.id, NULLABLE | NEW: Recurrence config |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Indexes**:
- `idx_tasks_user_id` on (user_id)
- `idx_tasks_priority` on (priority)
- `idx_tasks_due_date` on (due_date)
- `idx_tasks_user_priority` on (user_id, priority)
- `idx_tasks_user_due_date` on (user_id, due_date)

**Validation Rules**:
- priority MUST be one of: 'high', 'medium', 'low'
- due_date MUST be a valid timestamp or NULL
- is_recurring requires recurring_config_id to be set

---

### Tag (NEW)

User-defined labels for task categorization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Tag identifier |
| user_id | VARCHAR(255) | FK → users.id, NOT NULL | Owner reference |
| name | VARCHAR(50) | NOT NULL | Tag name |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_tags_user_id` on (user_id)
- `idx_tags_user_name` UNIQUE on (user_id, name)

**Validation Rules**:
- name MUST be 1-50 characters
- name MUST be unique per user (case-insensitive)
- name MUST NOT be empty or whitespace-only

---

### TaskTag (NEW)

Many-to-many relationship between tasks and tags.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| task_id | INTEGER | FK → tasks.id, NOT NULL | Task reference |
| tag_id | INTEGER | FK → tags.id, NOT NULL | Tag reference |

**Primary Key**: (task_id, tag_id)

**Indexes**:
- Primary key index on (task_id, tag_id)
- `idx_task_tags_tag_id` on (tag_id) for reverse lookups

**Cascade Rules**:
- DELETE task → DELETE all task_tag entries
- DELETE tag → DELETE all task_tag entries

---

### RecurringConfig (NEW)

Configuration for recurring task patterns.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Config identifier |
| frequency | VARCHAR(20) | NOT NULL | daily/weekly/monthly |
| next_occurrence | TIMESTAMP | NOT NULL | Next scheduled date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Validation Rules**:
- frequency MUST be one of: 'daily', 'weekly', 'monthly'
- next_occurrence MUST be in the future (on creation)

---

### Reminder (NEW)

Scheduled reminders for tasks with due dates.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PK, AUTO | Reminder identifier |
| task_id | INTEGER | FK → tasks.id, NOT NULL | Task reference |
| remind_at | TIMESTAMP | NOT NULL | When to send reminder |
| sent | BOOLEAN | DEFAULT FALSE | Whether reminder was sent |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Indexes**:
- `idx_reminders_task_id` on (task_id)
- `idx_reminders_remind_at` on (remind_at) for scheduled queries
- `idx_reminders_pending` on (sent, remind_at) for unsent reminders

**Cascade Rules**:
- DELETE task → DELETE all reminders

**Validation Rules**:
- remind_at MUST be before task.due_date
- Only one active (sent=false) reminder per task

---

## SQLModel Definitions

### Task (Extended)

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False, index=True)

    # NEW: Advanced features
    priority: str = Field(default="medium", max_length=10)
    due_date: Optional[datetime] = Field(default=None, index=True)
    is_recurring: bool = Field(default=False)
    recurring_config_id: Optional[int] = Field(
        default=None, foreign_key="recurring_configs.id"
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")
    recurring_config: Optional["RecurringConfig"] = Relationship()
    reminders: List["Reminder"] = Relationship(back_populates="task")
```

### Tag

```python
class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship()
    tasks: List["Task"] = Relationship(back_populates="tags", link_model="TaskTag")
```

### TaskTag

```python
class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

### RecurringConfig

```python
class RecurringConfig(SQLModel, table=True):
    __tablename__ = "recurring_configs"

    id: Optional[int] = Field(default=None, primary_key=True)
    frequency: str = Field(max_length=20)  # daily, weekly, monthly
    next_occurrence: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Reminder

```python
class Reminder(SQLModel, table=True):
    __tablename__ = "reminders"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)
    remind_at: datetime = Field(index=True)
    sent: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    task: "Task" = Relationship(back_populates="reminders")
```

---

## Alembic Migration

```python
"""Add Phase V advanced features tables

Revision ID: 011_advanced_features
Revises: previous_revision
Create Date: 2026-01-26
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Extend tasks table
    op.add_column('tasks', sa.Column('priority', sa.String(10), server_default='medium'))
    op.add_column('tasks', sa.Column('due_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('is_recurring', sa.Boolean(), server_default='false'))
    op.add_column('tasks', sa.Column('recurring_config_id', sa.Integer(), nullable=True))

    # Create indexes for new columns
    op.create_index('idx_tasks_priority', 'tasks', ['priority'])
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])
    op.create_index('idx_tasks_user_priority', 'tasks', ['user_id', 'priority'])
    op.create_index('idx_tasks_user_due_date', 'tasks', ['user_id', 'due_date'])

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_tags_user_id', 'tags', ['user_id'])
    op.create_unique_constraint('uq_tags_user_name', 'tags', ['user_id', 'name'])

    # Create task_tags table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    )
    op.create_index('idx_task_tags_tag_id', 'task_tags', ['tag_id'])

    # Create recurring_configs table
    op.create_table(
        'recurring_configs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('frequency', sa.String(20), nullable=False),
        sa.Column('next_occurrence', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Add foreign key for recurring_config_id
    op.create_foreign_key(
        'fk_tasks_recurring_config',
        'tasks', 'recurring_configs',
        ['recurring_config_id'], ['id']
    )

    # Create reminders table
    op.create_table(
        'reminders',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('task_id', sa.Integer(), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('remind_at', sa.DateTime(), nullable=False),
        sa.Column('sent', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_reminders_task_id', 'reminders', ['task_id'])
    op.create_index('idx_reminders_remind_at', 'reminders', ['remind_at'])
    op.create_index('idx_reminders_pending', 'reminders', ['sent', 'remind_at'])


def downgrade():
    op.drop_table('reminders')
    op.drop_constraint('fk_tasks_recurring_config', 'tasks', type_='foreignkey')
    op.drop_table('recurring_configs')
    op.drop_table('task_tags')
    op.drop_table('tags')
    op.drop_index('idx_tasks_user_due_date', 'tasks')
    op.drop_index('idx_tasks_user_priority', 'tasks')
    op.drop_index('idx_tasks_due_date', 'tasks')
    op.drop_index('idx_tasks_priority', 'tasks')
    op.drop_column('tasks', 'recurring_config_id')
    op.drop_column('tasks', 'is_recurring')
    op.drop_column('tasks', 'due_date')
    op.drop_column('tasks', 'priority')
```

---

## Event Schemas

### TaskEvent

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class TaskEvent(BaseModel):
    event_type: str  # created, updated, completed, deleted
    task_id: int
    task_data: Dict[str, Any]
    user_id: str
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### ReminderEvent

```python
class ReminderEvent(BaseModel):
    task_id: int
    title: str
    due_at: datetime
    remind_at: datetime
    user_id: str
```

---

## State Transitions

### Task Completion (with Recurring)

```
                    ┌─────────────┐
                    │   Pending   │
                    │ (completed  │
                    │   = false)  │
                    └──────┬──────┘
                           │
                    Mark Complete
                           │
                           ▼
              ┌────────────────────────┐
              │     is_recurring?      │
              └───────────┬────────────┘
                    │           │
                   YES          NO
                    │           │
                    ▼           ▼
        ┌───────────────┐  ┌─────────────┐
        │ Create next   │  │  Completed  │
        │ occurrence    │  │ (completed  │
        │ (new task)    │  │  = true)    │
        └───────┬───────┘  └─────────────┘
                │
                ▼
        ┌───────────────┐
        │ Mark current  │
        │ as completed  │
        └───────────────┘
```

### Reminder Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Created   │────▶│   Pending   │────▶│    Sent     │
│ (sent=false)│     │ (remind_at  │     │ (sent=true) │
└─────────────┘     │   reached)  │     └─────────────┘
                    └─────────────┘
                           │
                    Publish to Kafka
                    (reminders topic)
```
