"""
Authentication endpoints for the V1 API.
This module provides endpoints for user authentication and registration.
"""

from datetime import timedelta
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from core.security import (
    verify_password,
    create_access_token,
    get_current_active_user,
    get_password_hash,
    get_current_superuser,
)
from db.database import get_db
from db.models import Player
from repositories.player_repository import player_repository
from schemas.pydantic_models import (
    Token,
    PlayerResponse,
    PlayerRequest,
    UserSignupRequest
)
from core.errors import ValidationException, AuthenticationException

router = APIRouter(tags=["Authentication"])

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login and get access token",
    description="OAuth2 compatible token login, get an access token for future requests.",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    OAuth2 compatible token login endpoint.
    
    Args:
        form_data: OAuth2 form with username and password
        db: Database session
        
    Returns:
        Token: Access token response
        
    Raises:
        AuthenticationException: If login fails
    """
    # Check if user exists
    user = player_repository.get_by_email(db, form_data.username)
    if not user:
        raise AuthenticationException("Incorrect email or password")
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise AuthenticationException("Incorrect email or password")
    
    # Check if user is active
    if not user.is_active:
        raise AuthenticationException("User account is disabled")
    
    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/signup",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Register a new player account with email and password.",
)
async def signup(
    player_data: UserSignupRequest = Body(...),
    db: Session = Depends(get_db)
) -> PlayerResponse:
    """
    Register a new player account.
    
    Args:
        player_data: User data for registration
        db: Database session
        
    Returns:
        PlayerResponse: Created player
        
    Raises:
        ValidationException: If email already exists or password is too short
    """
    # Check if email already exists
    existing_player = player_repository.get_by_email(db, player_data.email)
    if existing_player:
        raise ValidationException("Email already registered")
    
    # Validate password
    if not player_data.password or len(player_data.password) < 8:
        raise ValidationException("Password must be at least 8 characters long")
    
    # Convert to dictionary and handle password
    obj_in_data = player_data.dict(exclude_unset=True)
    obj_in_data["hashed_password"] = get_password_hash(player_data.password)
    del obj_in_data["password"]
    
    # Set default values
    obj_in_data["is_active"] = True
    obj_in_data["is_super"] = False
    
    # Create the player
    player = player_repository.create(db, obj_in_data)
    
    return PlayerResponse.from_orm(player)


@router.get(
    "/me",
    response_model=PlayerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get information about the currently logged in user.",
)
async def read_users_me(
    current_user: Player = Depends(get_current_active_user)
) -> PlayerResponse:
    """
    Get the current authenticated user.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        PlayerResponse: User information
    """
    return PlayerResponse.from_orm(current_user) 