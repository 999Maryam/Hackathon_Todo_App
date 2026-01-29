"""Task service with business logic.

Phase V: Extended with priority, due_date, filtering, sorting, and search support.
"""

from datetime import datetime
from typing import List, Optional
import uuid

from sqlalchemy import case
from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.task import Task
from app.models.schemas import TaskCreate, TaskUpdate
from app.models.enums import Priority
from app.utils.errors import NotFoundException


# Valid priority values
VALID_PRIORITIES = {p.value for p in Priority}

# T075: Priority sort mapping (high=1, medium=2, low=3 for ordering)
PRIORITY_SORT_ORDER = {
    "high": 1,
    "medium": 2,
    "low": 3,
}


class TaskService:
    """Service for task business logic and database operations.

    Phase V: Extended with priority, due_date, search, filter, and sort support.
    """

    @staticmethod
    def validate_priority(priority: str) -> str:
        """Validate and normalize priority value.

        Args:
            priority: Priority string to validate.

        Returns:
            Normalized priority value (lowercase).

        Raises:
            ValueError: If priority is not valid.
        """
        normalized = priority.lower() if priority else "medium"
        if normalized not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority: {priority}. Must be one of: {', '.join(VALID_PRIORITIES)}")
        return normalized

    @staticmethod
    def get_all_tasks(
        session: Session,
        user_id: str,
        # Phase V: Filter parameters
        search: Optional[str] = None,
        priority: Optional[List[str]] = None,
        completed: Optional[bool] = None,
        due_from: Optional[datetime] = None,
        due_to: Optional[datetime] = None,
        tag_ids: Optional[List[int]] = None,
        # Phase V: Sort parameters
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
    ) -> List[Task]:
        """Get all tasks for a specific user with optional filtering and sorting.

        Args:
            session: Database session.
            user_id: User ID to filter tasks by.
            search: Search term for title/description (ILIKE).
            priority: List of priority values to filter by.
            completed: Filter by completion status (None = all).
            due_from: Filter tasks due after this date.
            due_to: Filter tasks due before this date.
            tag_ids: Filter tasks with any of these tags.
            sort_by: Sort field (due_date, priority, created_at, title).
            sort_order: Sort order (asc, desc).

        Returns:
            List of Task objects for the user.
        """
        statement = select(Task).where(Task.user_id == user_id)

        # Phase V: Search filter (US4)
        if search:
            search_term = f"%{search}%"
            statement = statement.where(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )

        # Phase V: Priority filter (US5)
        if priority:
            statement = statement.where(Task.priority.in_(priority))

        # Phase V: Completion status filter (US5)
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Phase V: Due date range filter (US5)
        if due_from:
            statement = statement.where(Task.due_date >= due_from)
        if due_to:
            statement = statement.where(Task.due_date <= due_to)

        # Phase V: Tag filter (US5) - filter tasks that have any of the specified tags
        if tag_ids:
            from app.models.task_tag import TaskTag
            # Subquery to find task IDs that have any of the specified tags
            statement = statement.where(
                Task.id.in_(
                    select(TaskTag.task_id).where(TaskTag.tag_id.in_(tag_ids))
                )
            )

        # Phase V: Sorting (US6)
        if sort_by:
            # T075: Special handling for priority sort (high=1, medium=2, low=3)
            if sort_by == "priority":
                priority_order = case(
                    (Task.priority == "high", PRIORITY_SORT_ORDER["high"]),
                    (Task.priority == "medium", PRIORITY_SORT_ORDER["medium"]),
                    (Task.priority == "low", PRIORITY_SORT_ORDER["low"]),
                    else_=PRIORITY_SORT_ORDER["medium"],  # Default for null/unknown
                )
                if sort_order == "desc":
                    # desc means low priority first (3, 2, 1)
                    statement = statement.order_by(priority_order.desc())
                else:
                    # asc means high priority first (1, 2, 3)
                    statement = statement.order_by(priority_order.asc())
            else:
                # Standard column sorting with null handling
                order_column = getattr(Task, sort_by, Task.created_at)
                if sort_order == "desc":
                    statement = statement.order_by(order_column.desc().nulls_last())
                else:
                    statement = statement.order_by(order_column.asc().nulls_last())
        else:
            # Default: newest first
            statement = statement.order_by(Task.created_at.desc())

        return session.exec(statement).all()

    @staticmethod
    def get_task(session: Session, user_id: str, task_id: uuid.UUID) -> Task:
        """Get a single task by ID with ownership validation.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to retrieve.

        Returns:
            Task object if found and owned by user.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException("Task not found")
        return task

    @staticmethod
    def create_task(
        session: Session,
        user_id: str,
        task_create: TaskCreate,
    ) -> Task:
        """Create a new task for a user.

        Phase V: Extended with priority, due_date, and recurring support.
        T085: Handles is_recurring and recurring_frequency to create RecurringConfig.

        Args:
            session: Database session.
            user_id: Task owner (from JWT).
            task_create: Task creation data.

        Returns:
            Created Task object.

        Raises:
            ValueError: If priority or recurring_frequency is invalid.
        """
        from app.services.recurring_service import RecurringService

        # Phase V: Validate and normalize priority (US1)
        priority = TaskService.validate_priority(
            task_create.priority if task_create.priority else "medium"
        )

        # T085: Handle recurring task configuration (US7)
        recurring_config_id = None
        is_recurring = task_create.is_recurring or False

        if is_recurring:
            # Validate that frequency is provided for recurring tasks
            if not task_create.recurring_frequency:
                raise ValueError("recurring_frequency is required when is_recurring=true")

            # Create recurring configuration
            start_date = task_create.due_date or datetime.utcnow()
            config = RecurringService.create_recurring_config(
                session,
                frequency=task_create.recurring_frequency,
                start_date=start_date,
            )
            recurring_config_id = config.id

        task = Task(
            user_id=user_id,
            title=task_create.title,
            description=task_create.description,
            # Phase V: Advanced features
            priority=priority,
            due_date=task_create.due_date,
            is_recurring=is_recurring,
            recurring_config_id=recurring_config_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        # T101: Publish task_created event to Kafka
        from app.services.event_publisher import EventPublisher
        EventPublisher.publish_task_created(task)

        return task

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        task_update: TaskUpdate,
    ) -> Task:
        """Update an existing task with partial fields.

        Phase V: Extended with priority and due_date update support.
        T102: Publishes task_updated event to Kafka.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to update.
            task_update: Partial task update data.

        Returns:
            Updated Task object.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
            ValueError: If priority is invalid.
        """
        task = TaskService.get_task(session, user_id, task_id)

        # T102: Track changed fields for event
        changed_fields = []
        previous_values = {}

        # Update only provided fields and track changes
        if task_update.title is not None and task_update.title != task.title:
            previous_values["title"] = task.title
            task.title = task_update.title
            changed_fields.append("title")

        if task_update.description is not None and task_update.description != task.description:
            previous_values["description"] = task.description
            task.description = task_update.description
            changed_fields.append("description")

        # Phase V: Priority update (US1)
        if task_update.priority is not None:
            new_priority = TaskService.validate_priority(task_update.priority)
            if new_priority != task.priority:
                previous_values["priority"] = task.priority
                task.priority = new_priority
                changed_fields.append("priority")

        # Phase V: Due date update (US2)
        if task_update.due_date is not None and task_update.due_date != task.due_date:
            previous_values["due_date"] = task.due_date.isoformat() if task.due_date else None
            task.due_date = task_update.due_date
            changed_fields.append("due_date")

        # Phase V: Recurring update (US7)
        if task_update.is_recurring is not None and task_update.is_recurring != task.is_recurring:
            previous_values["is_recurring"] = task.is_recurring
            task.is_recurring = task_update.is_recurring
            changed_fields.append("is_recurring")

        # Update modified timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        # T102: Publish task_updated event to Kafka (only if something changed)
        if changed_fields:
            from app.services.event_publisher import EventPublisher
            EventPublisher.publish_task_updated(task, changed_fields, previous_values)

        return task

    @staticmethod
    def toggle_complete(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> Task:
        """Toggle task completion status.

        T086: For recurring tasks, completing triggers creation of next occurrence.
        T103: Publishes task_completed event to Kafka when completing.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to toggle.

        Returns:
            Task with toggled completion status.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        task = TaskService.get_task(session, user_id, task_id)
        was_completed = task.completed
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        # T103: Publish task_completed event to Kafka when completing
        if task.completed and not was_completed:
            from app.services.event_publisher import EventPublisher
            EventPublisher.publish_task_completed(task)

        # T086: Create next occurrence for recurring tasks when completed
        if task.completed and task.is_recurring and task.recurring_config_id:
            TaskService.create_next_occurrence(session, task)

        return task

    @staticmethod
    def create_next_occurrence(
        session: Session,
        completed_task: Task,
    ) -> Task:
        """Create the next occurrence of a recurring task.

        T087: Clones the completed task with a new due_date based on recurrence pattern.

        Args:
            session: Database session.
            completed_task: The completed recurring task.

        Returns:
            New Task object for the next occurrence.

        Raises:
            ValueError: If task is not recurring or has no config.
        """
        from app.services.recurring_service import RecurringService

        if not completed_task.is_recurring or not completed_task.recurring_config_id:
            raise ValueError("Task is not recurring or has no recurring configuration")

        # Get the recurring configuration
        config = RecurringService.get_recurring_config(
            session, completed_task.recurring_config_id
        )
        if not config:
            raise ValueError(f"RecurringConfig not found: {completed_task.recurring_config_id}")

        # Calculate next due date
        base_date = completed_task.due_date or datetime.utcnow()
        next_due_date = RecurringService.calculate_next_occurrence(
            base_date, config.frequency
        )

        # Update the config's next_occurrence
        config.next_occurrence = next_due_date
        session.add(config)

        # Create new task instance (clone with new due_date)
        new_task = Task(
            user_id=completed_task.user_id,
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            due_date=next_due_date,
            is_recurring=True,
            recurring_config_id=completed_task.recurring_config_id,
            completed=False,
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return new_task

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> None:
        """Delete a task permanently.

        T088: Cascade deletes recurring_config if this is the last task using it.
        T104: Publishes task_deleted event to Kafka.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to delete.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        from app.services.recurring_service import RecurringService

        task = TaskService.get_task(session, user_id, task_id)

        # T104: Capture task info before deletion for event
        task_id_str = str(task.id)
        task_title = task.title
        task_user_id = task.user_id

        # T088: Check if we need to delete the recurring config
        recurring_config_id = task.recurring_config_id

        # Delete the task first
        session.delete(task)
        session.commit()

        # T104: Publish task_deleted event to Kafka
        from app.services.event_publisher import EventPublisher
        EventPublisher.publish_task_deleted(task_id_str, task_user_id, task_title)

        # T088: If task had a recurring config, check if any other tasks use it
        if recurring_config_id:
            # Count remaining tasks with this config
            remaining_tasks = session.exec(
                select(Task).where(Task.recurring_config_id == recurring_config_id)
            ).all()

            # If no other tasks use this config, delete it
            if len(remaining_tasks) == 0:
                RecurringService.delete_recurring_config(session, recurring_config_id)
