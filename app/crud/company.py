from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyUpdate
from fastapi import HTTPException


def get_company_by_email(db: Session, email: str) -> Optional[Company]:
    return db.query(Company).filter(Company.email == email).first()


def get_company(db: Session, company_id: int) -> Optional[Company]:
    return db.query(Company).options(
        joinedload(Company.created_by_user),
        joinedload(Company.updated_by_user)
    ).filter(Company.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
    return db.query(Company).options(
        joinedload(Company.created_by_user),
        joinedload(Company.updated_by_user)
    ).offset(skip).limit(limit).all()


def create_company(db: Session, company_in: CompanyCreate) -> Company:
    db_company = Company(**company_in.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return get_company(db, db_company.id)


def update_company(db: Session, company_id: int, company_in: CompanyUpdate) -> Company:
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    for field, value in company_in.model_dump().items():
        setattr(db_company, field, value)
    db.commit()
    db.refresh(db_company)
    return get_company(db, company_id)


def delete_company(db: Session, company_id: int) -> None:
    db_company = get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
