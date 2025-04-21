from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from ..models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.EMPLOYEE
    company_id: Optional[int] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    company_id: Optional[int] = None
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "token"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
    company_id: Optional[int] = None


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
