from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.database.models import User
from app.schemas.user import UserCreate


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_create: UserCreate) -> User:
    password_hash = hash_password(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        password_hash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
