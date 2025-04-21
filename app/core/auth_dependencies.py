from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..core.auth_security import verify_token
from ..models.user import User, UserRole
from ..schemas.user import TokenData

# Replace OAuth2PasswordBearer with APIKeyHeader
api_key_header = APIKeyHeader(name="Authorization")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(api_key_header)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    user = db.query(User).filter(User.email == token_data.email).first()

    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def check_super_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def check_company_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.COMPANY_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def check_manager(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.role not in [UserRole.SUPER_ADMIN, UserRole.COMPANY_ADMIN, UserRole.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
