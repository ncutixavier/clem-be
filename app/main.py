from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, user
from .database import engine, get_db, Base

from .config import settings
from .models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CLEM - Company Leave & Employee Management System",
    description="""
    CLEM (Company Leave & Employee Management System) is a comprehensive solution for managing:
    
    * Employee leaves and attendance
    * Company policies and settings
    * Role-based access control
    * Employee information and profiles
    
    ## Features
    * Authentication and Authorization
    * Leave Request Management
    * Employee Profile Management
    * Company Settings Management
    * Role-Based Access Control
    """,
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {
        "name": "CLEM",
        "full_name": "Company Leave & Employee Management System",
        "version": "1.0.0",
        "description": "A comprehensive solution for managing company leaves and employee data",
        "documentation": {
            "swagger": "/api/docs",
            "redoc": "/api/redoc"
        },
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "leaves": "/api/v1/leaves",
            "companies": "/api/v1/companies"
        }
    }


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to make a simple query to test the connection
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
