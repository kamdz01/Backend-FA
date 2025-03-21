# app/services/auth_service.py
import uuid
from sqlalchemy.orm import Session
from app.models.user import User

def generate_token() -> str:
    """
    Generates a random token using UUID4.
    """
    return str(uuid.uuid4())

def get_user_by_token(db: Session, token: str) -> User:
    """
    Retrieves a user based on the provided token.
    """
    return db.query(User).filter(User.token == token).first()
