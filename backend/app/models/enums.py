"""Enum definitions for the Todo App."""

from enum import Enum


class Priority(str, Enum):
    """Task priority levels.

    Values: high, medium, low
    Used in Task.priority field.
    """
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurringFrequency(str, Enum):
    """Recurring task frequency options.

    Values: daily, weekly, monthly
    Used in RecurringConfig.frequency field.
    """
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
