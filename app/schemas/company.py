from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.schemas.user import UserResponse
class CompanyBase(BaseModel):
    name: str
    country: str
    city: str
    address: str
    email: EmailStr
    website: str
    phone_number: str
    logo: str
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: datetime

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class CompanyResponse(BaseModel):
    id: int
    name: str
    country: str
    city: str
    address: str
    email: EmailStr
    website: str
    phone_number: str
    logo: str
    is_active: bool = Field(default=True)
    created_by_user: UserResponse
    updated_by_user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
