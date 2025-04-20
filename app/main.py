from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database import engine, get_db
from .config import settings
from .models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get('/')
def root():
    return {"message": "Welcome to CLEM Application System!"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to make a simple query to test the connection
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
