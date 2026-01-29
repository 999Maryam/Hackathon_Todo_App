"""Reminder service for task reminder management.

Phase V US8: Handles reminder creation, validation, and auto-adjustment.
"""

from datetime import datetime, timedelta
from typing import Optional
import uuid

from sqlalchemy.orm import Session
from sqlmodel import select

from app.models.reminder import Reminder
from app.models.task import Task
from app.utils.errors import NotFoundException, BadRequestException


class ReminderService:
    """Service for task reminder management.

    Handles:
    - Creating and deleting reminders
    - Validating remind_at < due_date
    - Auto-adjusting reminders when due_date changes
    """

    @staticmethod
    def get_reminder_by_task(
        session: Session,
        task_id: uuid.UUID,
    ) -> Optional[Reminder]:
        """Get reminder for a specific task.

        Args:
            session: Database session.
            task_id: Task UUID.

        Returns:
            Reminder object or None if not found.
        """
        statement = select(Reminder).where(Reminder.task_id == task_id)
        return session.exec(statement).first()

    @staticmethod
    def set_reminder(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        remind_at: datetime,
    ) -> Reminder:
        """Set or update a reminder for a task.

        T094: Validates that remind_at < due_date.

        Args:
            session: Database session.
            user_id: Authenticated user ID (for task ownership check).
            task_id: Task UUID to set reminder for.
            remind_at: When to send the reminder (UTC).

        Returns:
            Created or updated Reminder object.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
            BadRequestException: If task has no due_date or remind_at >= due_date.
        """
        # Get and validate task ownership
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException("Task not found")

        # Validate task has a due date
        if not task.due_date:
            raise BadRequestException("Cannot set reminder for task without due date")

        # Validate remind_at is before due_date
        if remind_at >= task.due_date:
            raise BadRequestException("Reminder time must be before due date")

        # Check if reminder already exists
        existing = ReminderService.get_reminder_by_task(session, task_id)

        if existing:
            # Update existing reminder
            existing.remind_at = remind_at
            existing.sent = False  # Reset sent status
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing
        else:
            # Create new reminder
            reminder = Reminder(
                task_id=task_id,
                remind_at=remind_at,
                sent=False,
            )
            session.add(reminder)
            session.commit()
            session.refresh(reminder)
            return reminder

    @staticmethod
    def set_reminder_minutes_before(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        minutes_before: int,
    ) -> Reminder:
        """Set a reminder N minutes before the task's due date.

        Convenience method for common reminder patterns (1h, 1d, etc.).

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task UUID.
            minutes_before: Minutes before due_date to remind.

        Returns:
            Created or updated Reminder object.

        Raises:
            NotFoundException: If task doesn't exist.
            BadRequestException: If task has no due_date or minutes_before <= 0.
        """
        if minutes_before <= 0:
            raise BadRequestException("minutes_before must be positive")

        # Get task to calculate remind_at
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException("Task not found")

        if not task.due_date:
            raise BadRequestException("Cannot set reminder for task without due date")

        remind_at = task.due_date - timedelta(minutes=minutes_before)

        # Ensure remind_at is not in the past
        if remind_at <= datetime.utcnow():
            raise BadRequestException("Reminder time would be in the past")

        return ReminderService.set_reminder(session, user_id, task_id, remind_at)

    @staticmethod
    def delete_reminder(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> bool:
        """Delete a reminder for a task.

        T095: Removes the reminder from the task.

        Args:
            session: Database session.
            user_id: Authenticated user ID (for task ownership check).
            task_id: Task UUID.

        Returns:
            True if deleted, False if not found.

        Raises:
            NotFoundException: If task doesn't exist or doesn't belong to user.
        """
        # Verify task ownership
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            raise NotFoundException("Task not found")

        reminder = ReminderService.get_reminder_by_task(session, task_id)
        if not reminder:
            return False

        session.delete(reminder)
        session.commit()
        return True

    @staticmethod
    def adjust_reminder_for_due_date_change(
        session: Session,
        task_id: uuid.UUID,
        old_due_date: datetime,
        new_due_date: datetime,
    ) -> Optional[Reminder]:
        """Adjust reminder proportionally when due_date changes.

        T096: Maintains the same relative time before due_date.

        Example: If reminder was 1 hour before old due_date,
        it will be adjusted to 1 hour before new due_date.

        Args:
            session: Database session.
            task_id: Task UUID.
            old_due_date: Previous due_date.
            new_due_date: New due_date.

        Returns:
            Updated Reminder or None if no reminder exists.
        """
        reminder = ReminderService.get_reminder_by_task(session, task_id)
        if not reminder:
            return None

        # Calculate the time delta between old remind_at and old due_date
        time_before = old_due_date - reminder.remind_at

        # Apply same delta to new due_date
        new_remind_at = new_due_date - time_before

        # Ensure new remind_at is not in the past
        if new_remind_at <= datetime.utcnow():
            # Set to a minimum of now + 5 minutes if would be in past
            new_remind_at = datetime.utcnow() + timedelta(minutes=5)

        # Ensure remind_at is still before due_date
        if new_remind_at >= new_due_date:
            # Delete reminder if it would be after or at due_date
            session.delete(reminder)
            session.commit()
            return None

        reminder.remind_at = new_remind_at
        reminder.sent = False  # Reset sent status
        session.add(reminder)
        session.commit()
        session.refresh(reminder)

        return reminder

    @staticmethod
    def get_pending_reminders(
        session: Session,
        before: Optional[datetime] = None,
    ) -> list[Reminder]:
        """Get all unsent reminders that are due.

        Used by the reminder worker to find reminders to send.

        Args:
            session: Database session.
            before: Get reminders due before this time (default: now).

        Returns:
            List of Reminder objects.
        """
        check_time = before or datetime.utcnow()
        statement = (
            select(Reminder)
            .where(Reminder.sent == False)
            .where(Reminder.remind_at <= check_time)
            .order_by(Reminder.remind_at.asc())
        )
        return session.exec(statement).all()

    @staticmethod
    def mark_reminder_sent(
        session: Session,
        reminder_id: int,
    ) -> Reminder:
        """Mark a reminder as sent.

        Args:
            session: Database session.
            reminder_id: Reminder ID.

        Returns:
            Updated Reminder object.

        Raises:
            NotFoundException: If reminder not found.
        """
        reminder = session.get(Reminder, reminder_id)
        if not reminder:
            raise NotFoundException("Reminder not found")

        reminder.sent = True
        session.add(reminder)
        session.commit()
        session.refresh(reminder)

        return reminder

    @staticmethod
    def process_due_reminders(
        session: Session,
    ) -> int:
        """Process all due reminders and publish events.

        T105: Finds reminders that are due, publishes events to Kafka,
        and marks them as sent.

        This method should be called by a background worker or scheduled task.

        Args:
            session: Database session.

        Returns:
            Number of reminders processed.
        """
        from app.models.task import Task
        from app.services.event_publisher import EventPublisher

        # Get all pending reminders that are due
        due_reminders = ReminderService.get_pending_reminders(session)

        processed_count = 0

        for reminder in due_reminders:
            try:
                # Get the associated task
                task = session.get(Task, reminder.task_id)
                if not task:
                    # Task was deleted, mark reminder as sent to clean up
                    ReminderService.mark_reminder_sent(session, reminder.id)
                    continue

                # T105: Publish reminder event to Kafka
                EventPublisher.publish_reminder_due(
                    task_id=str(task.id),
                    task_title=task.title,
                    due_at=task.due_date,
                    remind_at=reminder.remind_at,
                    user_id=task.user_id,
                )

                # Mark reminder as sent
                ReminderService.mark_reminder_sent(session, reminder.id)
                processed_count += 1

            except Exception as e:
                # Log error but continue processing other reminders
                import logging
                logging.getLogger(__name__).error(
                    f"Failed to process reminder {reminder.id}: {e}"
                )

        return processed_count
