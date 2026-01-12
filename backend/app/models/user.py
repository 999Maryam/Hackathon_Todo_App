"""User data model for authentication."""

from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr, field_validator
import re


class UserBase(SQLModel):
    """Base fields for a user."""

    email: str = Field(unique=True, index=True)
    name: str = Field(max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        # Basic email validation regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email address")
        return v


class User(UserBase, table=True):
    """User database model."""

    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)



class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(min_length=8)


class UserPublic(UserBase):
    """Public representation of a user (without sensitive data)."""

    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""

    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        # Basic email validation regex
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email address")
        return v