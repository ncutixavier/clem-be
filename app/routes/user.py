from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core import auth_dependencies
from ..crud import user as user_crud
from ..schemas.user import UserCreate, UserResponse
from ..models.user import User, UserRole

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def read_users(
    db: Session = Depends(auth_dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth_dependencies.check_super_admin),
) -> Any:
    """
    Retrieve users. Only super admin can access this endpoint.
    """
    users = user_crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserResponse)
async def create_user(
    *,
    db: Session = Depends(auth_dependencies.get_db),
    user_in: UserCreate,
    current_user: User = Depends(auth_dependencies.check_super_admin),
) -> Any:
    """
    Create new user. Only super admin can create users.
    """
    user = user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = user_crud.create_user(db, user_in)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: Session = Depends(auth_dependencies.get_db),
    current_user: User = Depends(auth_dependencies.get_current_active_user),
) -> Any:
    """
    Get user by ID.
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # Check if user has permission to view this user
    if current_user.role != UserRole.SUPER_ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: Session = Depends(auth_dependencies.get_db),
    user_id: int,
    user_in: UserCreate,
    current_user: User = Depends(auth_dependencies.get_current_active_user),
) -> Any:
    """
    Update user.
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    # Check if user has permission to update this user
    if current_user.role != UserRole.SUPER_ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    user = user_crud.update_user(db, db_user=user, user_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    *,
    db: Session = Depends(auth_dependencies.get_db),
    user_id: int,
    current_user: User = Depends(auth_dependencies.check_super_admin),
) -> Any:
    """
    Delete user. Only super admin can delete users.
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user = user_crud.delete_user(db, user)
    return user
