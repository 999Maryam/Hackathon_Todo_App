"""Recurring task service for managing task recurrence patterns.

Phase V US7: Handles recurring task configuration and next occurrence calculation.
"""

from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from app.models.recurring_config import RecurringConfig
from app.models.enums import RecurringFrequency


# Valid frequency values
VALID_FREQUENCIES = {f.value for f in RecurringFrequency}


class RecurringService:
    """Service for recurring task configuration and scheduling.

    Handles:
    - Creating recurring configurations
    - Calculating next occurrence dates
    - Managing recurrence lifecycle
    """

    @staticmethod
    def validate_frequency(frequency: str) -> str:
        """Validate and normalize frequency value.

        Args:
            frequency: Frequency string to validate.

        Returns:
            Normalized frequency value (lowercase).

        Raises:
            ValueError: If frequency is not valid.
        """
        normalized = frequency.lower() if frequency else None
        if normalized not in VALID_FREQUENCIES:
            raise ValueError(
                f"Invalid frequency: {frequency}. Must be one of: {', '.join(VALID_FREQUENCIES)}"
            )
        return normalized

    @staticmethod
    def calculate_next_occurrence(
        current_date: datetime,
        frequency: str,
    ) -> datetime:
        """Calculate the next occurrence date based on frequency.

        T083: Uses python-dateutil for reliable date calculations.

        Args:
            current_date: The current/base date to calculate from.
            frequency: Recurrence frequency (daily, weekly, monthly).

        Returns:
            Next occurrence datetime.

        Raises:
            ValueError: If frequency is invalid.
        """
        frequency = RecurringService.validate_frequency(frequency)

        if frequency == RecurringFrequency.DAILY.value:
            return current_date + relativedelta(days=1)
        elif frequency == RecurringFrequency.WEEKLY.value:
            return current_date + relativedelta(weeks=1)
        elif frequency == RecurringFrequency.MONTHLY.value:
            return current_date + relativedelta(months=1)
        else:
            # Should not reach here due to validation
            raise ValueError(f"Unsupported frequency: {frequency}")

    @staticmethod
    def create_recurring_config(
        session: Session,
        frequency: str,
        start_date: Optional[datetime] = None,
    ) -> RecurringConfig:
        """Create a new recurring configuration.

        T084: Creates RecurringConfig record with calculated next_occurrence.

        Args:
            session: Database session.
            frequency: Recurrence frequency (daily, weekly, monthly).
            start_date: Initial date to calculate from (defaults to now).

        Returns:
            Created RecurringConfig object.

        Raises:
            ValueError: If frequency is invalid.
        """
        # Validate frequency
        validated_frequency = RecurringService.validate_frequency(frequency)

        # Calculate first occurrence from start_date or now
        base_date = start_date or datetime.utcnow()
        next_occurrence = RecurringService.calculate_next_occurrence(
            base_date, validated_frequency
        )

        # Create config
        config = RecurringConfig(
            frequency=validated_frequency,
            next_occurrence=next_occurrence,
        )

        session.add(config)
        session.commit()
        session.refresh(config)

        return config

    @staticmethod
    def update_next_occurrence(
        session: Session,
        config_id: int,
    ) -> RecurringConfig:
        """Update the next occurrence after a task is completed.

        Args:
            session: Database session.
            config_id: RecurringConfig ID to update.

        Returns:
            Updated RecurringConfig object.

        Raises:
            ValueError: If config not found.
        """
        config = session.get(RecurringConfig, config_id)
        if not config:
            raise ValueError(f"RecurringConfig not found: {config_id}")

        # Calculate new next occurrence from current next_occurrence
        config.next_occurrence = RecurringService.calculate_next_occurrence(
            config.next_occurrence, config.frequency
        )

        session.add(config)
        session.commit()
        session.refresh(config)

        return config

    @staticmethod
    def get_recurring_config(
        session: Session,
        config_id: int,
    ) -> Optional[RecurringConfig]:
        """Get a recurring configuration by ID.

        Args:
            session: Database session.
            config_id: RecurringConfig ID.

        Returns:
            RecurringConfig object or None if not found.
        """
        return session.get(RecurringConfig, config_id)

    @staticmethod
    def delete_recurring_config(
        session: Session,
        config_id: int,
    ) -> bool:
        """Delete a recurring configuration.

        T088: Supports cascade delete when task is deleted.

        Args:
            session: Database session.
            config_id: RecurringConfig ID to delete.

        Returns:
            True if deleted, False if not found.
        """
        config = session.get(RecurringConfig, config_id)
        if not config:
            return False

        session.delete(config)
        session.commit()
        return True
