# SKILL: database-model-generator

## 1. Purpose
Generate production-ready database models using SQLModel (SQLAlchemy + Pydantic) with relationships, indexes, validation, and schema definitions.

## 2. Input Parameters
- `ModelName`: Class name for the model (e.g., User, Task).
- `Fields`: Dictionary of field names and types.
- `Relationships`: List of related models and relationship types (e.g., "many-to-one with User").

## 3. Code Template

```python
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select

# --- Base Schemas ---

class {{ModelName}}Base(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)

# --- Table Model ---

class {{ModelName}}({{ModelName}}Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner_id: int = Field(foreign_key="user.id", index=True)
    owner: "User" = Relationship(back_populates="{{ModelName | lower}}s")

# --- API Schemas ---

class {{ModelName}}Create({{ModelName}}Base):
    pass

class {{ModelName}}Update(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class {{ModelName}}Response({{ModelName}}Base):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
```

## 4. Output
A Python file with SQLModel definitions containing Table models, Create schemas, Update schemas, and Response schemas.

## 5. Usage Example
Input: `ModelName="Task"`, `Fields={"title": "str", "is_completed": "bool"}`, `Relationships=["User"]`
Output: A Task model with a foreign key to User and corresponding Pydantic schemas for API interactions.

## 6. Quality Standards
- Use `Field` for all DB-specific constraints (index, foreign_key).
- Inherit from `Base` to share logic between DB models and API schemas.
- Automatic UTC timestamps for `created_at` and `updated_at`.
- Strict type hints and Pydantic validation (min_length, etc.).
