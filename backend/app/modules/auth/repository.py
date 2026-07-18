from sqlalchemy.orm import Session
from app.modules.auth.models import User
from app.modules.auth.schemas import UserCreate
from app.modules.auth.utils import get_password_hash
from datetime import datetime
import uuid

class AuthRepository:
    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            id=str(uuid.uuid4()),
            uuid=str(uuid.uuid4()),
            name=user_in.name,
            email=user_in.email,
            password_hash=hashed_password,
            role='user',
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_last_login(self, db: Session, user: User) -> None:
        user.last_login = datetime.utcnow()
        db.commit()

    def update_password(self, db: Session, user: User, new_password: str) -> None:
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
    def update_profile(self, db: Session, user: User, name: str) -> None:
        user.name = name
        db.commit()