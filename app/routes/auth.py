from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core import auth_dependencies
from ..core.auth_security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..schemas.user import Token, UserCreate, UserResponse, UserLogin
from ..models.user import User
from ..crud import user as user_crud

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(auth_dependencies.get_db),
    user_in: UserLogin = None
) -> Any:
    """
    Login with email and password to get access token.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role,
            "company_id": user.company_id
        },
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "token"
    }


@router.post("/register", response_model=UserResponse)
async def register(
    *,
    db: Session = Depends(auth_dependencies.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )

    user = user_crud.create_user(db, user_in)
    return user


@router.post("/logout")
async def logout(
    current_user: User = Depends(auth_dependencies.get_current_active_user),
) -> Any:
    """
    Logout current user.
    """
    # In a JWT-based authentication system, the client is responsible for removing the token
    # The server doesn't maintain any session state
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(auth_dependencies.get_current_active_user),
) -> Any:
    """
    Get current authenticated user.
    """
    return current_user
