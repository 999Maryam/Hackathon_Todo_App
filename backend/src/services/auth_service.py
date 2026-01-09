from sqlmodel import Session, select
from ..models.user import User, UserCreate
from ..auth.jwt_handler import create_access_token
from passlib.context import CryptContext
from typing import Optional

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    user = session.exec(select(User).where(User.email == email)).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user
    user = User(
        email=user_create.email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def create_access_token_for_user(user: User) -> str:
    """Create access token for a user"""
    data = {"sub": user.id}
    return create_access_token(data=data)


def invalidate_token(token: str) -> bool:
    """In a stateless JWT system, token invalidation is typically handled differently.
    For this implementation, we're relying on client-side token removal and token expiration.
    In a production system, you might implement a token blacklist or short-lived tokens with refresh tokens."""
    # In a true stateless JWT system, we don't store tokens server-side
    # So this is a placeholder for future implementation if needed
    return True