# app/main.py
from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.controllers import router as api_router
import app.models  # Import modeli, aby zostały zarejestrowane

# Tworzenie tabel w bazie danych (jeśli nie istnieją)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MVC FastAPI Application")

# Rejestracja routera API
app.include_router(api_router)
