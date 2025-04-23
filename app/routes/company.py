from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import company as company_crud
from app.schemas import company as company_schemas
from app.models.user import User
from app.core import auth_dependencies

router = APIRouter(prefix="/api/v1/companies", tags=["companies"])


@router.post("/", response_model=company_schemas.CompanyResponse)
async def create_company(
    company: company_schemas.CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_dependencies.check_super_admin)
):
    db_company = company_crud.get_company_by_email(db, email=company.email)
    if db_company:
        raise HTTPException(status_code=400, detail="Email already registered")
    company.created_by = current_user.id
    company.updated_by = current_user.id
    return company_crud.create_company(db, company)


@router.get("/", response_model=list[company_schemas.CompanyResponse])
async def get_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_dependencies.check_super_admin)
):
    return company_crud.get_companies(db, skip, limit)


@router.get("/{company_id}", response_model=company_schemas.CompanyResponse)
async def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_dependencies.check_super_admin)
):
    db_company = company_crud.get_company(db, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company


@router.put("/{company_id}", response_model=company_schemas.CompanyResponse)
async def update_company(
    company_id: int,
    company: company_schemas.CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_dependencies.check_super_admin)
):
    company.updated_by = current_user.id
    company.updated_at = datetime.utcnow()
    return company_crud.update_company(db, company_id, company)


@router.delete("/{company_id}", response_model=company_schemas.CompanyResponse)
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_dependencies.check_super_admin)
):
    company = company_crud.get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    company.is_active = False
    company.updated_by = current_user.id
    company.updated_at = datetime.utcnow()
    return company_crud.update_company(db, company_id, company)
