from sqlalchemy.orm import Session

from app.auth.hashing import verify_password
from app.database.models import User
from app.services.user_service import get_user_by_username


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
