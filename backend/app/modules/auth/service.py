from sqlalchemy.orm import Session
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import UserCreate, LoginRequest, ChangePasswordRequest, UserUpdateProfile, Token
from app.modules.auth.utils import verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta
from app.core.config import settings

class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    def register_user(self, db: Session, user_in: UserCreate):
        existing = self.repo.get_user_by_email(db, user_in.email)
        if existing:
            raise HTTPException(status_code=400, detail='Email already registered')
        return self.repo.create_user(db, user_in)

    def login(self, db: Session, login_data: LoginRequest) -> Token:
        user = self.repo.get_user_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        if not user.is_active:
            raise HTTPException(status_code=400, detail='Inactive user')
            
        self.repo.update_last_login(db, user)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.id, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type='bearer', user=user)

    def change_password(self, db: Session, user, pwd_data: ChangePasswordRequest):
        if not verify_password(pwd_data.current_password, user.password_hash):
            raise HTTPException(status_code=400, detail='Invalid current password')
        self.repo.update_password(db, user, pwd_data.new_password)

    def update_profile(self, db: Session, user, update_data: UserUpdateProfile):
        if update_data.name:
            self.repo.update_profile(db, user, update_data.name)
        return user