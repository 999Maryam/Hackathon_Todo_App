"""FastAPI dependencies for authentication and request context."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt
from datetime import datetime, timedelta

from app.config import settings

security = HTTPBearer()


def current_user(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """Dependency to extract and verify JWT token from Authorization header.

    Args:
        credentials: HTTP Bearer credentials from FastAPI security.

    Returns:
        str: The user_id from the JWT token.

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
        )
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authentication token",
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def create_test_token(user_id: str, days: int = 7) -> str:
    """Create a test JWT token for development and testing.

    Args:
        user_id: The user ID to encode in the token.
        days: Token expiry in days.

    Returns:
        str: The encoded JWT token.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=days),
    }
    token = jwt.encode(
        payload,
        settings.better_auth_secret,
        algorithm="HS256",
    )
    return token
