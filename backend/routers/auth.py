from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import uuid
from datetime import timedelta
from database import engine
from models import User
from auth.jwt_utils import create_access_token, decode_and_validate_jwt
from auth.dependencies import get_current_user
from config.settings import settings
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create the auth router
router = APIRouter(prefix="/auth", tags=["auth"])


# Pydantic models for request/response
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    user_email: str

class UserResponse(BaseModel):
    id: str
    email: str

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    Register a new user
    """
    async with AsyncSession(engine) as session:
        # Check if user already exists
        existing_user_statement = select(User).where(User.email == user_data.email)
        existing_user_result = await session.exec(existing_user_statement)
        existing_user = existing_user_result.first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = pwd_context.hash(user_data.password)

        # Create new user
        user = User(
            email=user_data.email,
            password_hash=hashed_password
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserResponse(id=str(user.id), email=user.email)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    """
    Authenticate user and return JWT token
    """
    async with AsyncSession(engine) as session:
        # Find user by email
        user_statement = select(User).where(User.email == login_data.email)
        user_result = await session.exec(user_statement)
        user = user_result.first()

        if not user or not pwd_context.verify(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Create access token
        token_data = {
            "sub": str(user.id),  # Subject (user ID)
            "user_id": str(user.id),
            "email": user.email
        }

        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(hours=24)  # Token valid for 24 hours
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=str(user.id),
            user_email=user.email
        )


@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token removal is sufficient)
    """
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user_id: str = Depends(get_current_user)):
    """
    Get current user's information
    """
    # Get user from database using the validated user ID
    async with AsyncSession(engine) as session:
        # Use select to get the user by ID
        user_statement = select(User).where(User.id == UUID(current_user_id))
        user_result = await session.exec(user_statement)
        user = user_result.first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return UserResponse(id=str(user.id), email=user.email)