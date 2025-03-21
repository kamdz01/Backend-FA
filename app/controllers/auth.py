from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.db.session import get_db
from app.services.auth_service import generate_token

router = APIRouter()

@router.post("/signup")
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_create.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email już zarejestrowany"
        )
    
    token = generate_token()
    new_user = User(email=user_create.email, password=user_create.password, token=token)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"token": token}

@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_login.email,
        User.password == user_login.password
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowe dane logowania"
        )
    
    token = generate_token()
    user.token = token
    db.commit()
    return {"token": token}
