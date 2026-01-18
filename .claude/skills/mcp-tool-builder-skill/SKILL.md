---
name: mcp-tool-builder-skill
description: Generate complete MCP tool implementations with FastAPI/MCP SDK style, user ownership validation, and SQLModel queries.
version: 1.0.0
---

# MCP Tool Builder Skill

This skill generates one complete MCP tool implementation when given a tool name and spec.

## Input Requirements

- **Tool name**: The function/tool identifier
- **Parameters**: Input parameters with types and descriptions
- **Return format**: Expected response structure

## Output Specifications

Generates a complete Python function including:
- Full function code using FastAPI/MCP SDK style
- `user_id` check for authentication
- SQLModel query with ownership filter
- Proper return dict structure
- Docstring with Phase III spec reference
- Inline comments explaining logic

## Instructions

1. **Function Signature**
   - Use async def for all tool handlers
   - Accept typed parameters matching input spec
   - Include db session dependency injection
   - Add user_id parameter for ownership validation

2. **User Ownership Validation**
   - Always verify user_id is present
   - Filter all queries by user_id for multi-tenancy
   - Return 401/403 errors for unauthorized access
   - Never expose data from other users

3. **SQLModel Query Pattern**
   - Use existing db session from Phase II
   - Apply ownership filter: `.where(Model.user_id == user_id)`
   - Handle not found cases with proper errors
   - Use `.first()` or `.all()` as appropriate

4. **Return Format**
   - Return structured dict matching spec
   - Include success/error status
   - Provide meaningful error messages
   - Match MCP tool response conventions

5. **Documentation**
   - Add docstring with tool description
   - Include parameter documentation
   - Reference Phase III spec section
   - Add inline comments for complex logic

## Template Structure

```python
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from typing import Optional
from app.db import get_session
from app.models import YourModel

async def tool_name(
    param1: str,
    param2: Optional[int] = None,
    user_id: str = None,
    db: Session = Depends(get_session)
) -> dict:
    """
    Brief description of what this tool does.

    Args:
        param1: Description of param1
        param2: Description of param2 (optional)
        user_id: Authenticated user ID for ownership validation
        db: Database session (injected)

    Returns:
        dict: Response with status and data

    Reference: Phase III Spec - Section X.X
    """
    # Validate user authentication
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Query with ownership filter
    statement = select(YourModel).where(
        YourModel.user_id == user_id,
        YourModel.param1 == param1
    )
    result = db.exec(statement).first()

    # Handle not found
    if not result:
        return {"success": False, "error": "Resource not found"}

    # Return structured response
    return {
        "success": True,
        "data": result.model_dump()
    }
```

## Best Practices

- Always validate user_id before any database operation
- Use SQLModel's type-safe query builder
- Return consistent response structures
- Log tool invocations without sensitive data
- Handle edge cases (empty results, invalid params)
- Follow existing Phase II db session patterns
