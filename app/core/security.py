"""
Security and authentication utilities.
This module handles security-related functionality including
password hashing, JWT token creation, and authentication.
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Player
from core.config import settings
from core.errors import AuthenticationException, AuthorizationException

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 setup for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: The plaintext password
        hashed_password: The hashed password
        
    Returns:
        bool: True if the password matches the hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing.
    
    Args:
        password: The plaintext password
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional expiration time override
        
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Player:
    """
    Get the current authenticated user from the JWT token.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        Player: The authenticated user
        
    Raises:
        AuthenticationException: If authentication fails
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AuthenticationException("Could not validate credentials")
    except jwt.JWTError:
        raise AuthenticationException("Could not validate credentials")
    
    user = db.execute(select(Player).where(Player.id == user_id)).scalar_one_or_none()
    if user is None:
        raise AuthenticationException("User not found")
    return user


def get_current_active_user(
    current_user: Player = Depends(get_current_user),
) -> Player:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Player: The authenticated user if active
        
    Raises:
        AuthenticationException: If user is inactive
    """
    if not current_user.is_active:
        raise AuthorizationException("Account is inactive")
    return current_user


def get_current_superuser(
    current_user: Player = Depends(get_current_active_user),
) -> Player:
    """
    Get the current superuser.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Player: The authenticated user if superuser
        
    Raises:
        AuthenticationException: If user is not a superuser
    """
    if not current_user.is_super:
        raise AuthorizationException("Insufficient permissions")
    return current_user 