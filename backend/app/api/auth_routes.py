"""Authentication API endpoints for user registration and login."""

import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
import jwt
import bcrypt
from uuid import UUID, uuid4

from app.database import get_session
from app.config import settings
from app.models import User, UserCreate, UserPublic
from app.models.schemas import ErrorResponse

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class UserRegistrationRequest(BaseModel):
    """Request schema for user registration."""

    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    password: str = Field(..., min_length=8, description="User's password")


class UserLoginRequest(BaseModel):
    """Request schema for user login."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints."""

    user: UserPublic
    access_token: str
    token_type: str = "bearer"


@auth_router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        409: {"model": ErrorResponse, "description": "Conflict - User already exists"},
    },
)
def register(
    request: UserRegistrationRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Register a new user.

    Creates a new user account and returns an authentication token.

    Args:
        request: Registration data (email, name, password)
        session: Database session

    Returns:
        AuthResponse with user data and access token

    Raises:
        400 Bad Request: If validation fails
        409 Conflict: If user with email already exists
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == request.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    password_hash = bcrypt.hashpw(
        request.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Create new user
    db_user = User(
        email=request.email,
        name=request.name,
        password_hash=password_hash
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    logger.info(f"Created new user: {db_user.email}")

    # Create JWT token
    token_payload = {
        "user_id": db_user.id,
        "email": db_user.email,
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
    }
    access_token = jwt.encode(
        token_payload,
        settings.better_auth_secret,
        algorithm="HS256"
    )

    return AuthResponse(
        user=db_user,
        access_token=access_token
    )


@auth_router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
def login(
    request: UserLoginRequest,
    session: Session = Depends(get_session),
) -> AuthResponse:
    """Authenticate a user and return an access token.

    Args:
        request: Login data (email, password)
        session: Database session

    Returns:
        AuthResponse with user data and access token

    Raises:
        400 Bad Request: If validation fails
        401 Unauthorized: If credentials are invalid
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == request.email)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not bcrypt.checkpw(request.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    token_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
    }
    access_token = jwt.encode(
        token_payload,
        settings.better_auth_secret,
        algorithm="HS256"
    )

    logger.info(f"User logged in: {user.email}")

    return AuthResponse(
        user=user,
        access_token=access_token
    )


# HTTP Bearer security scheme
security = HTTPBearer()


class MeResponse(BaseModel):
    """Response schema for current user endpoint."""

    id: str
    email: str
    name: str
    expiresAt: str | None = None


@auth_router.get(
    "/me",
    response_model=MeResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
def get_current_user(
    credentials: HTTPBearer = Depends(security),
    session: Session = Depends(get_session),
) -> MeResponse:
    """Get the current authenticated user.

    Args:
        credentials: Bearer token from Authorization header
        session: Database session

    Returns:
        Current user information

    Raises:
        401 Unauthorized: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        exp = payload.get("exp")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    # Get user from database
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Convert expiration timestamp to ISO string
    expires_at = None
    if exp:
        expires_at = datetime.utcfromtimestamp(exp).isoformat() + "Z"

    return MeResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        expiresAt=expires_at
    )