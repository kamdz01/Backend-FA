# app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Pydantic model for creating a new user.
    """
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Pydantic model for user login.
    """
    email: EmailStr
    password: str
