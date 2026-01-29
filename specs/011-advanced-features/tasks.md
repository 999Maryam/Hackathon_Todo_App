# Tasks: Phase V Part A - Advanced Features

**Input**: Design documents from `/specs/011-advanced-features/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/ (complete)

**Feature**: 011-advanced-features
**Date**: 2026-01-26
**Branch**: `011-advanced-features`

**MVP Scope (Core Deliverable)**  
Phase 1–4 (T001–T040): Priority + Due Dates features + foundational setup  
→ Enables first production-grade task management with visual indicators and due date handling

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Environment setup and new dependencies

- [x] T001 Add aiokafka>=0.8.0 and python-dateutil>=2.8 to backend/requirements.txt
- [x] T002 [P] Add date-fns to frontend package.json
- [x] T003 [P] Add @radix-ui/react-select to frontend package.json
- [x] T004 [P] Create Kafka environment variables in .env.example (KAFKA_BOOTSTRAP_SERVERS, REDPANDA_USERNAME, REDPANDA_PASSWORD)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database schema and Kafka infrastructure - MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

### Database Models

- [x] T005 Create Priority enum in backend/app/models/enums.py (high, medium, low)
- [x] T006 [P] Create Tag model in backend/app/models/tag.py (id, user_id, name, created_at)
- [x] T007 [P] Create TaskTag model in backend/app/models/task_tag.py (task_id, tag_id)
- [x] T008 [P] Create RecurringConfig model in backend/app/models/recurring_config.py (id, frequency, next_occurrence, created_at)
- [x] T009 [P] Create Reminder model in backend/app/models/reminder.py (id, task_id, remind_at, sent, created_at)
- [x] T010 Extend Task model in backend/app/models/task.py with priority, due_date, is_recurring, recurring_config_id fields
- [x] T011 Update backend/app/models/__init__.py to export all new models

### Database Migration

- [x] T012 Generate Alembic migration for Phase V schema changes (alembic revision --autogenerate -m "Add Phase V advanced features")
- [x] T013 Run migration and verify all tables/indexes created (alembic upgrade head)

### Pydantic Schemas

- [x] T014 [P] Create TagCreate, TagUpdate, Tag, TagWithCount, TagWithTasks schemas in backend/app/schemas/tag.py
- [x] T015 [P] Create ReminderCreate, Reminder schemas in backend/app/schemas/reminder.py
- [x] T016 [P] Create RecurringConfigCreate, RecurringConfig schemas in backend/app/schemas/recurring_config.py
- [x] T017 [P] Create TaskEvent, ReminderEvent, TaskUpdateEvent schemas in backend/app/schemas/events.py
- [x] T018 Extend TaskCreate, TaskUpdate, Task schemas in backend/app/schemas/task.py with priority, due_date, is_recurring, recurring_frequency, tag_ids, reminder fields

### Kafka Infrastructure

- [x] T019 Create KafkaProducer service in backend/app/services/kafka_producer.py with async publish, retry queue, and graceful fallback
- [x] T020 [P] Add Kafka configuration to backend/app/core/config.py (Settings class)
- [x] T021 Create startup/shutdown handlers for Kafka in backend/app/main.py

### Frontend Types

- [x] T022 Extend Task interface in frontend/src/lib/types.ts with priority, due_date, is_recurring, recurring_config, tags, reminder fields
- [x] T023 [P] Create Tag interface in frontend/src/lib/types.ts
- [x] T024 [P] Create Reminder interface in frontend/src/lib/types.ts
- [x] T025 [P] Create FilterParams and SortParams interfaces in frontend/src/lib/types.ts

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task Priority Management (Priority: P1) MVP

**Goal**: Users can assign priority levels (High, Medium, Low) to tasks

**Independent Test**: Create tasks with different priorities, verify visual indicators display correctly

### Backend Implementation

- [x] T026 [US1] Update TaskService.create_task() in backend/app/services/task_service.py to handle priority field with default 'medium'
- [x] T027 [US1] Update TaskService.update_task() in backend/app/services/task_service.py to allow priority updates
- [x] T028 [US1] Add priority validation in task service (must be high/medium/low)

### Frontend Implementation

- [x] T029 [P] [US1] Create PriorityBadge component in frontend/src/components/dashboard/PriorityBadge.tsx with color-coded indicators (red=high, yellow=medium, green=low)
- [x] T030 [P] [US1] Create PrioritySelect component in frontend/src/components/dashboard/PrioritySelect.tsx using @radix-ui/react-select
- [x] T031 [US1] Update TaskItem.tsx to display PriorityBadge for each task
- [x] T032 [US1] Update TaskModal.tsx (or task creation form) to include PrioritySelect field

**Checkpoint**: User Story 1 complete - users can set and view task priorities

---

## Phase 4: User Story 2 - Due Dates for Tasks (Priority: P1) MVP

**Goal**: Users can set due dates and see overdue/due-today/due-soon indicators

**Independent Test**: Create tasks with due dates, verify overdue tasks are highlighted

### Backend Implementation

- [x] T033 [US2] Update TaskService.create_task() to handle due_date field
- [x] T034 [US2] Update TaskService.update_task() to allow due_date updates
- [x] T035 [P] [US2] Create date utility functions in backend/app/utils/date_utils.py (is_overdue, is_due_today, is_due_soon)

### Frontend Implementation

- [x] T036 [P] [US2] Create DueDatePicker component in frontend/src/components/dashboard/DueDatePicker.tsx using date-fns
- [x] T037 [P] [US2] Create DueDateBadge component in frontend/src/components/dashboard/DueDateBadge.tsx with overdue/today/soon indicators
- [x] T038 [US2] Create date formatting utilities in frontend/src/lib/date-utils.ts (formatDueDate, isOverdue, isDueToday, isDueSoon)
- [x] T039 [US2] Update TaskItem.tsx to display DueDateBadge
- [x] T040 [US2] Update TaskModal.tsx to include DueDatePicker field

**Checkpoint**: User Story 2 complete - users can set due dates with visual indicators

---

## Phase 5: User Story 3 - Tag Management (Priority: P2)

**Goal**: Users can create, assign, and manage custom tags for task categorization

**Independent Test**: Create tags, assign to tasks, view tag counts

### Backend Implementation

- [x] T041 [US3] Create TagService in backend/app/services/tag_service.py with CRUD operations (create, get, list, update, delete)
- [x] T042 [US3] Add get_tag_with_count() method to TagService (returns tag with task count)
- [x] T043 [US3] Add get_user_tags() method to TagService (returns all tags for user with counts)
- [x] T044 [P] [US3] Create Tag API router in backend/app/api/tags.py with CRUD endpoints (/api/{user_id}/tags)
- [x] T045 [US3] Update TaskService to handle tag_ids on create/update (link tasks to tags)
- [x] T046 [US3] Add TaskService.add_tags_to_task() and remove_tags_from_task() methods
- [x] T047 [US3] Add POST/DELETE /api/{user_id}/tasks/{task_id}/tags endpoints in backend/app/api/routes.py

### Frontend Implementation

- [x] T048 [P] [US3] Create TagBadge component in frontend/src/components/tags/TagBadge.tsx
- [x] T049 [P] [US3] Create TagPicker component in frontend/src/components/dashboard/TagPicker.tsx (multi-select)
- [x] T050 [P] [US3] Create TagManager component in frontend/src/components/tags/TagManager.tsx (CRUD UI)
- [x] T051 [US3] Create useTags hook in frontend/src/hooks/useTags.ts (fetch, create, delete tags)
- [x] T052 [US3] Update TaskItem.tsx to display task tags using TagBadge
- [x] T053 [US3] Update TaskModal.tsx to include TagPicker field

**Checkpoint**: User Story 3 complete - full tag management functionality

---

## Phase 6: User Story 4 - Search Tasks (Priority: P2)

**Goal**: Users can search tasks by title and description

**Independent Test**: Create multiple tasks, search by keyword, verify matching results

### Backend Implementation

- [x] T054 [US4] Add search parameter to list_tasks() in backend/app/services/task_service.py
- [x] T055 [US4] Implement PostgreSQL ILIKE search on title and description fields
- [x] T056 [US4] Update GET /api/{user_id}/tasks endpoint to accept ?search= query parameter

### Frontend Implementation

- [x] T057 [P] [US4] Create SearchBar component in frontend/src/components/dashboard/SearchBar.tsx with debounced input
- [x] T058 [US4] Update useTasks hook to accept search parameter
- [x] T059 [US4] Integrate SearchBar into task list page (dashboard)
- [x] T060 [US4] Add "no results found" message when search returns empty

**Checkpoint**: User Story 4 complete - search functionality working

---

## Phase 7: User Story 5 - Filter Tasks (Priority: P2)

**Goal**: Users can filter tasks by priority, tags, status, and due date range

**Independent Test**: Apply various filter combinations, verify correct results

### Backend Implementation

- [x] T061 [US5] Add filter parameters to list_tasks() signature (priority, tags, completed, due_from, due_to)
- [x] T062 [US5] Implement dynamic query builder in TaskService with composable WHERE clauses
- [x] T063 [US5] Update GET /api/{user_id}/tasks endpoint to accept filter query parameters
- [x] T064 [US5] Add filter parameter validation (priority must be valid, dates must be ISO format)

### Frontend Implementation

- [x] T065 [P] [US5] Create FilterPanel component in frontend/src/components/dashboard/FilterPanel.tsx
- [x] T066 [US5] Add priority filter (checkboxes for high/medium/low) in FilterPanel
- [x] T067 [US5] Add tag filter (multi-select from user's tags) in FilterPanel
- [x] T068 [US5] Add status filter (pending/completed/all) in FilterPanel
- [x] T069 [US5] Add due date range filter (from/to date pickers) in FilterPanel
- [x] T070 [US5] Update useTasks hook to accept filter parameters
- [x] T071 [US5] Add "Clear all filters" button in FilterPanel
- [x] T072 [US5] Integrate FilterPanel into task list page

**Checkpoint**: User Story 5 complete - filtering functionality working

---

## Phase 8: User Story 6 - Sort Tasks (Priority: P2)

**Goal**: Users can sort tasks by due date, priority, creation date, or title

**Independent Test**: Apply different sort options, verify correct ordering

### Backend Implementation

- [x] T073 [US6] Add sort parameters to list_tasks() signature (sort_by, sort_order)
- [x] T074 [US6] Implement ORDER BY clause builder with null handling (nulls last for due_date)
- [x] T075 [US6] Add priority sort mapping (high=1, medium=2, low=3 for ordering)
- [x] T076 [US6] Update GET /api/{user_id}/tasks endpoint to accept sort_by and sort_order parameters

### Frontend Implementation

- [x] T077 [P] [US6] Create SortDropdown component in frontend/src/components/dashboard/SortDropdown.tsx
- [x] T078 [US6] Add sort options: Due Date, Priority, Created Date, Title (A-Z)
- [x] T079 [US6] Add ascending/descending toggle button in SortDropdown
- [x] T080 [US6] Update useTasks hook to accept sort parameters
- [x] T081 [US6] Integrate SortDropdown into task list page

**Checkpoint**: User Story 6 complete - sorting functionality working ✓

---

## Phase 9: User Story 7 - Recurring Tasks (Priority: P3)

**Goal**: Users can create tasks that repeat on a schedule (daily, weekly, monthly)

**Independent Test**: Create recurring task, complete it, verify new instance created

### Backend Implementation

- [x] T082 [US7] Create RecurringService in backend/app/services/recurring_service.py
- [x] T083 [US7] Add calculate_next_occurrence() method using python-dateutil (daily/weekly/monthly)
- [x] T084 [US7] Add create_recurring_config() method to create RecurringConfig record
- [x] T085 [US7] Update TaskService.create_task() to handle is_recurring and recurring_frequency
- [x] T086 [US7] Update TaskService.complete_task() to trigger next occurrence creation for recurring tasks
- [x] T087 [US7] Add create_next_occurrence() method that clones task with new due_date
- [x] T088 [US7] Add delete cascade logic: deleting recurring task removes recurring_config

### Frontend Implementation

- [x] T089 [P] [US7] Create RecurringSelect component in frontend/src/components/dashboard/RecurringSelect.tsx (Daily/Weekly/Monthly/None)
- [x] T090 [P] [US7] Create RecurringBadge component in frontend/src/components/dashboard/RecurringBadge.tsx showing recurrence pattern
- [x] T091 [US7] Update TaskModal.tsx to include recurring toggle and frequency selector
- [x] T092 [US7] Update TaskItem.tsx to display RecurringBadge for recurring tasks

**Checkpoint**: User Story 7 complete - recurring tasks functional ✓

---

## Phase 10: User Story 8 - Task Reminders (Priority: P3)

**Goal**: Users can set reminders for tasks with due dates

**Independent Test**: Set reminder, verify reminder event published at scheduled time

### Backend Implementation

- [x] T093 [US8] Create ReminderService in backend/app/services/reminder_service.py
- [x] T094 [US8] Add set_reminder() method (validates remind_at < due_date)
- [x] T095 [US8] Add delete_reminder() method
- [x] T096 [US8] Add auto-update logic: when due_date changes, adjust remind_at proportionally
- [x] T097 [US8] Add POST/DELETE /api/{user_id}/tasks/{task_id}/reminder endpoints in backend/app/api/routes.py

### Frontend Implementation

- [x] T098 [P] [US8] Create ReminderPicker component in frontend/src/components/dashboard/ReminderPicker.tsx (1h before, 1d before, custom)
- [x] T099 [US8] Update TaskModal.tsx to include ReminderPicker (only when due_date is set)
- [x] T100 [US8] Display reminder indicator on TaskItem when reminder is set

**Checkpoint**: User Story 8 complete - reminder scheduling functional ✓

---

## Phase 11: User Story 9 - Event Publishing (Kafka) (Priority: P3)

**Goal**: All task operations publish events to Kafka for downstream processing

**Independent Test**: Perform task operations, verify events appear in Kafka topics

### Backend Implementation

- [x] T101 [US9] Integrate KafkaProducer.publish() into TaskService.create_task() (task_created event)
- [x] T102 [US9] Integrate KafkaProducer.publish() into TaskService.update_task() (task_updated event)
- [x] T103 [US9] Integrate KafkaProducer.publish() into TaskService.complete_task() (task_completed event)
- [x] T104 [US9] Integrate KafkaProducer.publish() into TaskService.delete_task() (task_deleted event)
- [x] T105 [US9] Create reminder event publisher: when reminder time reached, publish to reminders topic
- [x] T106 [US9] Add local retry queue for failed Kafka publishes with exponential backoff
- [x] T107 [US9] Add event logging for audit trail (log all published events)

### Event Schema Validation

- [x] T108 [P] [US9] Create event serialization tests to verify TaskEvent schema compliance
- [x] T109 [P] [US9] Create event serialization tests to verify ReminderEvent schema compliance

**Checkpoint**: User Story 9 complete - event publishing operational ✓

---

## Phase 12: MCP Tool Extensions

**Purpose**: Extend MCP tools to support new task attributes

- [x] T110 Update add_task MCP tool in backend/app/tools/task_tools.py with priority, due_date, tag_ids parameters
- [x] T111 Update list_tasks MCP tool with search, filter (priority, tags, completed, due_from, due_to), sort parameters
- [x] T112 [P] Create add_tag MCP tool in backend/app/tools/task_tools.py
- [x] T113 [P] Create list_tags MCP tool in backend/app/tools/task_tools.py
- [x] T114 [P] Create set_reminder MCP tool in backend/app/tools/task_tools.py

**Checkpoint**: MCP tools extended with Phase V features ✓

---

## Phase 13: Polish & Integration

**Purpose**: Final integration, documentation, and testing

- [x] T115 [P] Update quickstart.md with testing commands for each feature
- [x] T116 [P] Add API documentation for new endpoints in README or API docs
- [x] T117 Run full integration test: create task with priority, due_date, tags, set reminder, complete recurring task
- [x] T118 Verify Kafka events published for complete workflow
- [x] T119 [P] Update frontend README with new component documentation
- [x] T120 Code cleanup: remove any unused imports, add type hints where missing
- [x] T121 Verify all new features work with OpenRouter-powered AI agent (natural language commands)

**Note**: T117, T118, T120, T121 require manual verification with running application.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-11)**: All depend on Foundational phase completion
  - US1 (Priority) + US2 (Due Dates): Can run in parallel after Foundational
  - US3 (Tags): Can run in parallel after Foundational
  - US4 (Search) + US5 (Filter) + US6 (Sort): Can run in parallel after Foundational
  - US7 (Recurring): Can run after US2 (needs due_date support)
  - US8 (Reminders): Can run after US2 (needs due_date support)
  - US9 (Events): Can run after Foundational (needs KafkaProducer)
- **MCP Tools (Phase 12)**: Depends on all user stories for full support
- **Polish (Phase 13)**: Final phase

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|-----------|-------------------|
| US1 (Priority) | Foundational | US2, US3, US4, US5, US6, US9 |
| US2 (Due Dates) | Foundational | US1, US3, US4, US5, US6, US9 |
| US3 (Tags) | Foundational | US1, US2, US4, US5, US6, US9 |
| US4 (Search) | Foundational | US1, US2, US3, US5, US6, US9 |
| US5 (Filter) | Foundational | US1, US2, US3, US4, US6, US9 |
| US6 (Sort) | Foundational | US1, US2, US3, US4, US5, US9 |
| US7 (Recurring) | US2 (due_date) | US8, US9 |
| US8 (Reminders) | US2 (due_date) | US7, US9 |
| US9 (Events) | Foundational | US1-US8 (integrates with all) |

### Parallel Opportunities

Within each phase, tasks marked [P] can run in parallel:
- Phase 1: T002, T003, T004 can run in parallel
- Phase 2: T006, T007, T008, T009 can run in parallel (models)
- Phase 2: T014, T015, T016, T017 can run in parallel (schemas)
- Each user story has parallel-safe tasks marked

---

## Implementation Strategy

### MVP First (Priority P1 Stories)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: US1 - Priority Management
4. Complete Phase 4: US2 - Due Dates
5. **STOP and VALIDATE**: Test P1 features independently
6. Deploy/demo if ready (MVP with priorities and due dates)

### Incremental Delivery (Add P2 Stories)

7. Complete Phase 5: US3 - Tags
8. Complete Phase 6: US4 - Search
9. Complete Phase 7: US5 - Filter
10. Complete Phase 8: US6 - Sort
11. **CHECKPOINT**: Full intermediate features working

### Advanced Features (P3 Stories)

12. Complete Phase 9: US7 - Recurring Tasks
13. Complete Phase 10: US8 - Reminders
14. Complete Phase 11: US9 - Kafka Events
15. Complete Phase 12: MCP Tools
16. Complete Phase 13: Polish

---

## Task Count Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Phase 1: Setup | 4 | 3 |
| Phase 2: Foundational | 21 | 11 |
| Phase 3: US1 Priority | 7 | 2 |
| Phase 4: US2 Due Dates | 8 | 3 |
| Phase 5: US3 Tags | 13 | 4 |
| Phase 6: US4 Search | 7 | 1 |
| Phase 7: US5 Filter | 12 | 1 |
| Phase 8: US6 Sort | 9 | 1 |
| Phase 9: US7 Recurring | 11 | 2 |
| Phase 10: US8 Reminders | 8 | 1 |
| Phase 11: US9 Events | 9 | 2 |
| Phase 12: MCP Tools | 5 | 3 |
| Phase 13: Polish | 6 | 3 |
| **TOTAL** | **120** | **37** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Kafka unavailability should not block task operations (graceful fallback)
- Use OPENROUTER_API_KEY in backend secret (todo-secrets) – no hard-coding