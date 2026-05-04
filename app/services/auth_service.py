from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

def register_user(db: Session, email: str, name: str, password: str) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Энэ имэйлээр аль хэдийн бүртгэгдсэн байна.")
    user = User(email=email, name=name, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Имэйл эсвэл нууц үг буруу байна.")
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": str(user.id), "email": user.email}, expires_delta=expires)
