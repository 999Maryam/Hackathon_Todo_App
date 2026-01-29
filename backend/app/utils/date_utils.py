"""Date utility functions for Phase V task features.

Provides helper functions for due date calculations and status checks.
"""

from datetime import datetime, timedelta
from typing import Optional


def is_overdue(due_date: Optional[datetime]) -> bool:
    """Check if a task is overdue.

    Args:
        due_date: Task due date (UTC timestamp).

    Returns:
        True if due_date has passed, False otherwise.
    """
    if not due_date:
        return False
    return datetime.utcnow() > due_date


def is_due_today(due_date: Optional[datetime]) -> bool:
    """Check if a task is due today.

    Args:
        due_date: Task due date (UTC timestamp).

    Returns:
        True if due_date is today, False otherwise.
    """
    if not due_date:
        return False
    today = datetime.utcnow().date()
    return due_date.date() == today


def is_due_soon(due_date: Optional[datetime], days: int = 3) -> bool:
    """Check if a task is due within the specified number of days.

    Args:
        due_date: Task due date (UTC timestamp).
        days: Number of days to consider "soon" (default: 3).

    Returns:
        True if due_date is within the specified days, False otherwise.
    """
    if not due_date:
        return False
    now = datetime.utcnow()
    soon_threshold = now + timedelta(days=days)
    return now < due_date <= soon_threshold


def get_due_status(due_date: Optional[datetime]) -> str:
    """Get the due status of a task.

    Args:
        due_date: Task due date (UTC timestamp).

    Returns:
        Status string: 'overdue', 'today', 'soon', 'upcoming', or 'none'.
    """
    if not due_date:
        return "none"

    if is_overdue(due_date):
        return "overdue"
    if is_due_today(due_date):
        return "today"
    if is_due_soon(due_date):
        return "soon"
    return "upcoming"


def calculate_reminder_time(
    due_date: datetime,
    minutes_before: int,
) -> datetime:
    """Calculate reminder time based on due date and offset.

    Args:
        due_date: Task due date (UTC timestamp).
        minutes_before: Minutes before due_date to send reminder.

    Returns:
        Reminder datetime (UTC).

    Raises:
        ValueError: If minutes_before is negative or reminder would be in the past.
    """
    if minutes_before < 0:
        raise ValueError("minutes_before must be non-negative")

    remind_at = due_date - timedelta(minutes=minutes_before)

    if remind_at < datetime.utcnow():
        raise ValueError("Reminder time would be in the past")

    return remind_at
