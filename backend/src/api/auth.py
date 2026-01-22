from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ..database import get_session
from ..api.deps import get_current_user
from ..models.user import UserCreate, UserRead, UserLogin
from ..services.auth_service import authenticate_user, create_user, create_access_token_for_user

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    try:
        user = create_user(session, user_create)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login")
async def login(login_data: UserLogin, session: Session = Depends(get_session)):
    """Login user and return access token"""
    user = authenticate_user(session, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token_for_user(user)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


@router.post("/logout")
async def logout():
    """Logout user"""
    # In a stateless JWT system, logout is typically handled on the client side
    # by removing the token from client storage
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
async def get_current_user_profile(current_user = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user