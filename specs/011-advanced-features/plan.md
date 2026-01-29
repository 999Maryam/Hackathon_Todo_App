# Implementation Plan: Phase V Part A - Advanced Features

**Branch**: `011-advanced-features` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/011-advanced-features/spec.md`

---

## Summary

Implement advanced task management features including priorities, tags, due dates, search, filter, sort, recurring tasks, and reminders. All task operations will publish events to Kafka topics for downstream processing, enabling event-driven architecture for Phase V.

**Technical Approach**: Extend existing FastAPI backend with new database tables (tags, task_tags, reminders, recurring_configs), update Task model with priority/due_date fields, add Kafka producer for event publishing, and extend MCP tools to support new task attributes. Frontend will be updated with new UI components for all features.

---

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript 5.0+ (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, aiokafka (Kafka client), Next.js 16+, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (existing), Kafka/Redpanda (new)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Linux server (Docker/Kubernetes), Web browsers
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <500ms response for filtered/sorted queries, <1s for search, events published within 100ms
**Constraints**: Must maintain backward compatibility with Phase IV, no breaking changes to existing API
**Scale/Scope**: 1000+ tasks per user, 3 Kafka topics, 5 new database tables

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. SDD Workflow** | PASS | Following /specify → /plan → /tasks → /implement |
| **II. Progressive Evolution** | PASS | Builds on Phase IV containers, maintains backward compatibility |
| **III. Reusable Intelligence** | PASS | Kafka event producer will be reusable across services |
| **IV. Security First** | PASS | All new endpoints require JWT, user_id filtering enforced |
| **V. Stateless & Resilient** | PASS | All state in Neon PostgreSQL, Kafka for events |
| **VI. Cloud-Native** | PASS | Kafka integration ready for Dapr in Part B |
| **VII. AI-Native Focus** | PASS | MCP tools extended for new task attributes |
| **VIII. Maintainability** | PASS | Task ID + spec references in all new code |

**Gate Result**: ALL PASS - Proceed to Phase 0

---

## Project Structure

### Documentation (this feature)

```text
specs/011-advanced-features/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI specs)
│   ├── tasks-api.yaml
│   ├── tags-api.yaml
│   └── events-schema.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── task.py           # Extended with priority, due_date, is_recurring
│   │   ├── tag.py            # NEW: Tag model
│   │   ├── task_tag.py       # NEW: Many-to-many relationship
│   │   ├── reminder.py       # NEW: Reminder model
│   │   └── recurring_config.py # NEW: Recurring task config
│   ├── schemas/
│   │   ├── task.py           # Extended schemas
│   │   ├── tag.py            # NEW: Tag schemas
│   │   └── events.py         # NEW: Kafka event schemas
│   ├── services/
│   │   ├── task_service.py   # Extended with new features
│   │   ├── tag_service.py    # NEW: Tag CRUD operations
│   │   ├── reminder_service.py # NEW: Reminder management
│   │   └── kafka_producer.py # NEW: Event publishing
│   ├── tools/
│   │   └── task_tools.py     # Extended MCP tools
│   └── api/
│       ├── routes.py         # Extended with search/filter/sort
│       └── tags.py           # NEW: Tag endpoints
└── tests/
    ├── test_tags.py          # NEW
    ├── test_reminders.py     # NEW
    ├── test_recurring.py     # NEW
    └── test_kafka.py         # NEW

frontend/
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── TaskItem.tsx      # Extended with priority/due date
│   │   │   ├── TaskModal.tsx     # Extended with new fields
│   │   │   ├── SearchBar.tsx     # NEW: Search component
│   │   │   ├── FilterPanel.tsx   # NEW: Filter controls
│   │   │   ├── SortDropdown.tsx  # NEW: Sort options
│   │   │   ├── TagPicker.tsx     # NEW: Tag selection
│   │   │   ├── PriorityBadge.tsx # NEW: Priority indicator
│   │   │   └── DueDatePicker.tsx # NEW: Date picker
│   │   └── tags/
│   │       ├── TagManager.tsx    # NEW: Tag CRUD UI
│   │       └── TagBadge.tsx      # NEW: Tag display
│   ├── hooks/
│   │   ├── useTasks.ts           # Extended with filter/sort
│   │   └── useTags.ts            # NEW: Tag operations
│   └── lib/
│       └── types.ts              # Extended task types
└── tests/
    └── tasks-advanced.test.tsx   # NEW
```

**Structure Decision**: Extending existing web application structure (Option 2) with new models, services, and components for advanced features.

---

## Complexity Tracking

> No constitution violations requiring justification.

---

## Architecture Overview

### Data Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │───▶│   FastAPI   │───▶│  PostgreSQL │    │   Kafka     │
│  (Next.js)  │◀───│  (Backend)  │◀───│   (Neon)    │    │ (Redpanda)  │
└─────────────┘    └──────┬──────┘    └─────────────┘    └──────▲──────┘
                          │                                      │
                          └──────────────────────────────────────┘
                                    Event Publishing
```

### Kafka Event Flow

```
Task Operation (Create/Update/Complete/Delete)
         │
         ▼
   TaskService
         │
    ┌────┴────┐
    │         │
    ▼         ▼
 Database   KafkaProducer
 (Commit)        │
                 ▼
          ┌──────────────┐
          │ task-events  │ ───▶ Recurring Task Service (Part B)
          │   topic      │ ───▶ Audit Service (Part B)
          └──────────────┘

          ┌──────────────┐
          │  reminders   │ ───▶ Notification Service (Part B)
          │   topic      │
          └──────────────┘
```

---

## Implementation Phases

### Phase 1: Database Schema Extensions
- Extend Task model with priority, due_date, is_recurring, recurring_config_id
- Create Tag, TaskTag, Reminder, RecurringConfig models
- Generate Alembic migration

### Phase 2: Tag Management
- Tag CRUD service and API endpoints
- TaskTag association logic
- Frontend TagManager and TagPicker components

### Phase 3: Priority & Due Dates
- Update TaskService with priority/due_date handling
- Frontend PriorityBadge and DueDatePicker components
- Update TaskItem and TaskModal

### Phase 4: Search, Filter, Sort
- Backend query builder with filters
- SearchBar, FilterPanel, SortDropdown components
- Update useTasks hook with filter/sort state

### Phase 5: Recurring Tasks
- RecurringConfig model and service
- Automatic next occurrence creation on completion
- Frontend recurring task UI

### Phase 6: Reminders
- Reminder model and service
- Frontend reminder picker
- Reminder scheduling logic

### Phase 7: Kafka Event Publishing
- KafkaProducer service with aiokafka
- Event schemas (TaskEvent, ReminderEvent)
- Integration with all task operations
- Graceful fallback when Kafka unavailable

### Phase 8: MCP Tool Extensions
- Update add_task with priority, due_date, tags
- Update list_tasks with filter/sort support
- Add new tools: add_tag, list_tags, set_reminder

---

## Key Design Decisions

### D1: Kafka Client Choice
**Decision**: Use `aiokafka` for async Kafka producer
**Rationale**: Native async support matches FastAPI's async handlers
**Alternatives Rejected**: kafka-python (sync only), confluent-kafka (more complex)

### D2: Event Publishing Strategy
**Decision**: Fire-and-forget with local retry queue
**Rationale**: Task operations shouldn't block on Kafka availability
**Implementation**: Async publish, queue failed events for retry

### D3: Tag Storage
**Decision**: Separate tags table with many-to-many relationship
**Rationale**: Supports tag reuse, counting, and efficient queries
**Alternatives Rejected**: JSON array in task (harder to query/index)

### D4: Search Implementation
**Decision**: PostgreSQL ILIKE for simple search, full-text search for scaling
**Rationale**: ILIKE sufficient for <1000 tasks, upgrade path available
**Alternatives Rejected**: Elasticsearch (overkill for MVP)

### D5: Filter Query Building
**Decision**: Dynamic SQLModel query builder
**Rationale**: Type-safe, composable filters
**Implementation**: Chain .where() clauses based on filter params

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Kafka unavailability | Local queue with exponential backoff retry |
| Complex filter combinations | Query builder with clear composition rules |
| Migration data loss | Alembic migration with ADD COLUMN (non-destructive) |
| Performance degradation | Database indexes on priority, due_date, user_id |

---

## Testing Strategy

### Backend Tests
- Unit tests for each new service (tag, reminder, recurring, kafka)
- Integration tests for API endpoints with filter/sort combinations
- Mock Kafka producer for unit tests

### Frontend Tests
- Component tests for new UI elements
- Integration tests for filter/sort interactions
- E2E tests for complete workflows

### Event Tests
- Verify event schema compliance
- Test Kafka unavailability handling
- Test event ordering and delivery

---

## Dependencies

### New Python Packages
```
aiokafka>=0.8.0        # Async Kafka client
python-dateutil>=2.8   # Date calculations for recurring tasks
```

### New Frontend Packages
```
date-fns               # Date formatting and manipulation
@radix-ui/react-select # Dropdown components
```

---

## Next Steps

1. **Phase 0**: Generate research.md (resolve any remaining unknowns)
2. **Phase 1**: Generate data-model.md with entity definitions
3. **Phase 1**: Generate API contracts in /contracts/
4. **Phase 1**: Generate quickstart.md
5. **Phase 2**: Run /sp.tasks to generate implementation tasks

---

## Appendix: Constitution Compliance Matrix

| Requirement | Spec Section | Implementation |
|-------------|--------------|----------------|
| FR-001 (Priorities) | US-1 | Task.priority field, PriorityBadge component |
| FR-007 (Tags) | US-3 | Tag model, TagService, TagPicker component |
| FR-011 (Search) | US-4 | SearchBar component, backend ILIKE query |
| FR-014-018 (Filters) | US-5 | FilterPanel component, query builder |
| FR-019-021 (Sort) | US-6 | SortDropdown component, ORDER BY clauses |
| FR-022-025 (Recurring) | US-7 | RecurringConfig model, completion handler |
| FR-026-028 (Reminders) | US-8 | Reminder model, scheduler service |
| FR-029-032 (Events) | US-9 | KafkaProducer, event schemas |
