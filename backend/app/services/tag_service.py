"""Tag service with business logic for tag management.

Phase V US3: Tag management service with CRUD operations and task association.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session
from sqlmodel import select, func

from app.models.tag import Tag
from app.models.task_tag import TaskTag
from app.schemas.tag import TagCreate, TagUpdate, TagWithCount
from app.utils.errors import NotFoundException, BadRequestException


class TagService:
    """Service for tag business logic and database operations.

    Phase V US3: Provides CRUD operations for tags with task count support.
    """

    @staticmethod
    def get_tag(session: Session, user_id: str, tag_id: int) -> Tag:
        """Get a single tag by ID with ownership validation.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            tag_id: Tag ID to retrieve.

        Returns:
            Tag object if found and owned by user.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
        """
        tag = session.get(Tag, tag_id)
        if not tag or tag.user_id != user_id:
            raise NotFoundException("Tag not found")
        return tag

    @staticmethod
    def get_tag_with_count(session: Session, user_id: str, tag_id: int) -> TagWithCount:
        """Get a tag with its associated task count.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            tag_id: Tag ID to retrieve.

        Returns:
            TagWithCount with task count included.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
        """
        tag = TagService.get_tag(session, user_id, tag_id)

        # Count associated tasks
        count_statement = select(func.count(TaskTag.task_id)).where(
            TaskTag.tag_id == tag_id
        )
        task_count = session.exec(count_statement).first() or 0

        return TagWithCount(
            id=tag.id,
            user_id=tag.user_id,
            name=tag.name,
            created_at=tag.created_at,
            task_count=task_count,
        )

    @staticmethod
    def get_user_tags(session: Session, user_id: str) -> List[TagWithCount]:
        """Get all tags for a user with task counts.

        Args:
            session: Database session.
            user_id: User ID to get tags for.

        Returns:
            List of TagWithCount objects for the user.
        """
        # Get all tags for user
        statement = select(Tag).where(Tag.user_id == user_id).order_by(Tag.name)
        tags = session.exec(statement).all()

        # Get task counts for each tag
        result = []
        for tag in tags:
            count_statement = select(func.count(TaskTag.task_id)).where(
                TaskTag.tag_id == tag.id
            )
            task_count = session.exec(count_statement).first() or 0
            result.append(
                TagWithCount(
                    id=tag.id,
                    user_id=tag.user_id,
                    name=tag.name,
                    created_at=tag.created_at,
                    task_count=task_count,
                )
            )

        return result

    @staticmethod
    def create_tag(session: Session, user_id: str, tag_create: TagCreate) -> Tag:
        """Create a new tag for a user.

        Args:
            session: Database session.
            user_id: Tag owner (from JWT).
            tag_create: Tag creation data.

        Returns:
            Created Tag object.

        Raises:
            BadRequestException: If tag name already exists for user.
        """
        # Check for duplicate name
        existing = session.exec(
            select(Tag).where(Tag.user_id == user_id, Tag.name == tag_create.name)
        ).first()
        if existing:
            raise BadRequestException(f"Tag '{tag_create.name}' already exists")

        tag = Tag(
            user_id=user_id,
            name=tag_create.name.strip(),
        )
        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag

    @staticmethod
    def update_tag(
        session: Session,
        user_id: str,
        tag_id: int,
        tag_update: TagUpdate,
    ) -> Tag:
        """Update an existing tag.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            tag_id: Tag ID to update.
            tag_update: Partial tag update data.

        Returns:
            Updated Tag object.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
            BadRequestException: If new name already exists for user.
        """
        tag = TagService.get_tag(session, user_id, tag_id)

        if tag_update.name is not None:
            # Check for duplicate name (excluding current tag)
            existing = session.exec(
                select(Tag).where(
                    Tag.user_id == user_id,
                    Tag.name == tag_update.name,
                    Tag.id != tag_id,
                )
            ).first()
            if existing:
                raise BadRequestException(f"Tag '{tag_update.name}' already exists")

            tag.name = tag_update.name.strip()

        session.add(tag)
        session.commit()
        session.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(session: Session, user_id: str, tag_id: int) -> None:
        """Delete a tag permanently.

        Note: TaskTag associations are deleted via CASCADE.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            tag_id: Tag ID to delete.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
        """
        tag = TagService.get_tag(session, user_id, tag_id)
        session.delete(tag)
        session.commit()

    @staticmethod
    def add_tag_to_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        tag_id: int,
    ) -> None:
        """Add a tag to a task.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to add tag to.
            tag_id: Tag ID to add.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
            BadRequestException: If tag is already assigned to task.
        """
        # Validate tag ownership
        TagService.get_tag(session, user_id, tag_id)

        # Check if association already exists
        existing = session.exec(
            select(TaskTag).where(
                TaskTag.task_id == task_id,
                TaskTag.tag_id == tag_id,
            )
        ).first()
        if existing:
            raise BadRequestException("Tag is already assigned to this task")

        task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
        session.add(task_tag)
        session.commit()

    @staticmethod
    def remove_tag_from_task(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        tag_id: int,
    ) -> None:
        """Remove a tag from a task.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to remove tag from.
            tag_id: Tag ID to remove.

        Raises:
            NotFoundException: If tag doesn't exist or doesn't belong to user.
            NotFoundException: If tag is not assigned to task.
        """
        # Validate tag ownership
        TagService.get_tag(session, user_id, tag_id)

        # Find and delete association
        task_tag = session.exec(
            select(TaskTag).where(
                TaskTag.task_id == task_id,
                TaskTag.tag_id == tag_id,
            )
        ).first()
        if not task_tag:
            raise NotFoundException("Tag is not assigned to this task")

        session.delete(task_tag)
        session.commit()

    @staticmethod
    def get_task_tags(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
    ) -> List[Tag]:
        """Get all tags for a specific task.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to get tags for.

        Returns:
            List of Tag objects assigned to the task.
        """
        statement = (
            select(Tag)
            .join(TaskTag, TaskTag.tag_id == Tag.id)
            .where(TaskTag.task_id == task_id, Tag.user_id == user_id)
            .order_by(Tag.name)
        )
        return list(session.exec(statement).all())

    @staticmethod
    def set_task_tags(
        session: Session,
        user_id: str,
        task_id: uuid.UUID,
        tag_ids: List[int],
    ) -> List[Tag]:
        """Replace all tags on a task with a new set of tags.

        Args:
            session: Database session.
            user_id: Authenticated user ID.
            task_id: Task ID to update tags for.
            tag_ids: List of tag IDs to assign.

        Returns:
            List of Tag objects now assigned to the task.

        Raises:
            NotFoundException: If any tag doesn't exist or doesn't belong to user.
        """
        # Validate all tags belong to user
        for tag_id in tag_ids:
            TagService.get_tag(session, user_id, tag_id)

        # Remove existing associations
        existing = session.exec(
            select(TaskTag).where(TaskTag.task_id == task_id)
        ).all()
        for task_tag in existing:
            session.delete(task_tag)

        # Add new associations
        for tag_id in tag_ids:
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            session.add(task_tag)

        session.commit()

        # Return updated tags
        return TagService.get_task_tags(session, user_id, task_id)
