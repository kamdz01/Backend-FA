# app/db/__init__.py
"""
Initialization file for the db module.
Imports the database session and base model for convenient access.
"""
from .session import SessionLocal, get_db
from .base import Base
