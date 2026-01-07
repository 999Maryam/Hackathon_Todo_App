# SKILL: api-endpoint-generator

## 1. Purpose
Generate complete, production-ready FastAPI REST endpoints with JWT authentication, user isolation, Pydantic validation, and async database access.

## 2. Input Parameters
- `ResourceName`: Name of the entity (e.g., Task, Project).
- `ResourceSchema`: Fields and types for the resource.
- `RequiresAuth`: Boolean, whether endpoint requires JWT (default: True).
- `UserIsolation`: Boolean, whether users can only access their own data.

## 3. Code Template

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api import deps
from app.models.models import {{ResourceName}}
from app.schemas.{{ResourceName | lower}} import {{ResourceName}}Create, {{ResourceName}}Update, {{ResourceName}}Response
from app.auth.jwt import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model={{ResourceName}}Response, status_code=status.HTTP_201_CREATED)
async def create_{{ResourceName | lower}}(
    *,
    db: AsyncSession = Depends(deps.get_db),
    obj_in: {{ResourceName}}Create,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new {{ResourceName}}.
    """
    db_obj = {{ResourceName}}(**obj_in.dict(), owner_id=current_user.id)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[{{ResourceName}}Response])
async def read_{{ResourceName | lower}}s(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve {{ResourceName}}s.
    """
    query = select({{ResourceName}}).where({{ResourceName}}.owner_id == current_user.id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{id}", response_model={{ResourceName}}Response)
async def read_{{ResourceName | lower}}(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get {{ResourceName}} by ID.
    """
    query = select({{ResourceName}}).where({{ResourceName}}.id == id, {{ResourceName}}.owner_id == current_user.id)
    result = await db.execute(query)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="{{ResourceName}} not found")
    return db_obj

@router.put("/{id}", response_model={{ResourceName}}Response)
async def update_{{ResourceName | lower}}(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    obj_in: {{ResourceName}}Update,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a {{ResourceName}}.
    """
    query = select({{ResourceName}}).where({{ResourceName}}.id == id, {{ResourceName}}.owner_id == current_user.id)
    result = await db.execute(query)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="{{ResourceName}} not found")

    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

@router.delete("/{id}", response_model={{ResourceName}}Response)
async def delete_{{ResourceName | lower}}(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a {{ResourceName}}.
    """
    query = select({{ResourceName}}).where({{ResourceName}}.id == id, {{ResourceName}}.owner_id == current_user.id)
    result = await db.execute(query)
    db_obj = result.scalar_one_or_none()
    if not db_obj:
        raise HTTPException(status_code=404, detail="{{ResourceName}} not found")

    await db.delete(db_obj)
    await db.commit()
    return db_obj
```

## 4. Output
A Python file containing FastAPI route handlers with full type hinting, dependency injection, and security logic.

## 5. Usage Example
Input: `ResourceName="Todo"`, `UserIsolation=True`
Output: A set of CRUD endpoints for 'Todo' items where each user only sees their own tasks.

## 6. Quality Standards
- Strict type hinting (Python 3.10+).
- Async/await for all I/O.
- Detailed docstrings with endpoint descriptions.
- Consistent error handling via standard FastAPI exceptions.
- Mandatory authentication via `get_current_user` dependency.
