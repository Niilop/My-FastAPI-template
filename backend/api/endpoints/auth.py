# backend/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from models.schemas import UserCreate, UserLogin, Token, UserResponse
from services.auth_service import (
    create_user, authenticate_user, create_access_token, decode_token, get_user_by_email
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **email**: Must be a valid email address
    - **username**: Unique username
    - **password**: Password for the account
    """
    try:
        user = create_user(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    
    Returns an access token to use for authenticated requests.
    """
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = None, db: Session = Depends(get_db)):
    """
    Get the current authenticated user's information.
    
    Requires a valid JWT token in the Authorization header.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    token_data = decode_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = get_user_by_email(db, token_data["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
