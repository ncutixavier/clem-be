from sqlalchemy import Column, Integer, String, Boolean, Enum
import enum
from ..database import Base


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    COMPANY_ADMIN = "company_admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    company_id = Column(Integer, nullable=True)  # For company-specific users
