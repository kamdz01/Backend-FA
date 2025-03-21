# app/main.py
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.controllers import router as api_router
import app.models  # Ensure models are imported so they are registered

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MVC FastAPI Application")

# Include the API router
app.include_router(api_router)