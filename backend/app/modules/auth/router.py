from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.modules.auth.schemas import UserCreate, UserResponse, Token, LoginRequest, ChangePasswordRequest, UserUpdateProfile
from app.modules.auth.service import AuthService
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User
from app.shared.responses import SuccessResponse

router = APIRouter(prefix='/auth', tags=['auth'])
auth_service = AuthService()

@router.post('/register', response_model=SuccessResponse[UserResponse])
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = auth_service.register_user(db, user_in)
    return {'success': True, 'message': 'User registered successfully', 'data': user}

@router.post('/login', response_model=SuccessResponse[Token])
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    token = auth_service.login(db, login_data)
    return {'success': True, 'message': 'Login successful', 'data': token}

@router.post('/logout', response_model=SuccessResponse[None])
def logout(current_user: User = Depends(get_current_active_user)):
    # Frontend handles token removal. We just return success.
    return {'success': True, 'message': 'Logout successful', 'data': None}

@router.get('/me', response_model=SuccessResponse[UserResponse])
def get_me(current_user: User = Depends(get_current_active_user)):
    return {'success': True, 'message': 'Profile retrieved', 'data': current_user}

@router.put('/change-password', response_model=SuccessResponse[None])
def change_password(pwd_data: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    auth_service.change_password(db, current_user, pwd_data)
    return {'success': True, 'message': 'Password updated successfully', 'data': None}

@router.put('/update-profile', response_model=SuccessResponse[UserResponse])
def update_profile(update_data: UserUpdateProfile, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    updated = auth_service.update_profile(db, current_user, update_data)
    return {'success': True, 'message': 'Profile updated', 'data': updated}