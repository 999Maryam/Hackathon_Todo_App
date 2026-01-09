from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session
from ..database import get_session
from ..auth.jwt_handler import get_user_from_token
from ..models.user import User


async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    """Dependency to get current user from JWT token"""
    authorization = request.headers.get("Authorization")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = authorization.split(" ")[1]
    return get_user_from_token(token, session)


def get_db_session() -> Session:
    """Get database session dependency"""
    with get_session() as session:
        yield session