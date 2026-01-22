from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserLogin(SQLModel):
    """Schema for login request body"""
    email: str
    password: str