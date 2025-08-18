from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.schemas import AdminUserCreate, AdminUserLogin, Token, AdminUserResponse
from app.models.models import AdminUser
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=AdminUserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: AdminUserCreate, db: Session = Depends(get_db)):
    """
    Create a new admin user account.
    
    - **email**: Must be a valid email address and unique
    - **password**: Will be securely hashed before storage
    """
    # Check if user already exists
    db_user = db.query(AdminUser).filter(AdminUser.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = AdminUser(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
def login(user_credentials: AdminUserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    - **email**: Registered admin email
    - **password**: User password
    
    Returns a JWT token valid for 30 minutes by default.
    """
    # Find user by email
    user = db.query(AdminUser).filter(AdminUser.email == user_credentials.email).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}