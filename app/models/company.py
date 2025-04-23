from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    country = Column(String)
    city = Column(String)
    address = Column(String)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False)
    website = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    created_by_user = relationship(
        "User", foreign_keys=[created_by], backref="created_companies")
    updated_by_user = relationship(
        "User", foreign_keys=[updated_by], backref="updated_companies")
