import uuid
from sqlalchemy.orm import Session
from app.models.user import User

def generate_token() -> str:
    return str(uuid.uuid4())

def get_user_by_token(db: Session, token: str) -> User:
    return db.query(User).filter(User.token == token).first()
