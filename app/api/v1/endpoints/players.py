"""
API endpoints for player management.
"""
import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Body, Header, Path, Query, status, HTTPException
from sqlalchemy.orm import Session

from core.config import settings
from core.security import get_current_active_user, get_current_superuser

logger = logging.getLogger(__name__)
from db.database import get_db
from db.models import Player
from repositories.player_repository import player_repository
from schemas.pydantic_models import (
    PlayerRequest,
    PlayerRequestPatch,
    PlayerResponse,
)
from core.errors import ResourceNotFoundException, ValidationException, AuthorizationException, DatabaseException

router = APIRouter()


@router.get(
    "/",
    response_model=List[PlayerResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all players",
    description="Retrieve all players, with optional filtering by name.",
    tags=["Players"]
)
async def get_players(
    name: Optional[str] = Query(None, description="Filter players by name (partial match)"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> List[PlayerResponse]:
    """
    Get all players, optionally filtered by name.
    
    Args:
        name: Optional filter for player name (partial match)
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[PlayerResponse]: List of players
    """
    players = player_repository.get_all(db, name=name)
    return [PlayerResponse.model_validate(player) for player in players]


@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific player",
    description="Retrieve a specific player by ID.",
    tags=["Players"]
)
async def get_player(
    player_id: str = Path(..., description="The ID of the player to retrieve"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> PlayerResponse:
    """
    Get a specific player by ID.
    
    Args:
        player_id: Player ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        PlayerResponse: Player details
        
    Raises:
        ResourceNotFoundException: If the player is not found
    """
    player = player_repository.get_or_404(db, player_id)
    return PlayerResponse.model_validate(player)


@router.post(
    "/",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new player",
    description="Create a new player.",
    tags=["Players"]
)
async def create_player(
    player_data: PlayerRequest = Body(
        ...,
        example={
            "name": "John Doe",
            "email": "john@example.com",
            "zip": "12345",
            "handicap": 15.2,
            "ghin_number": "1234567"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_superuser)
) -> PlayerResponse:
    """
    Create a new player (admin only).
    
    Args:
        player_data: Player data
        db: Database session
        current_user: Authenticated superuser
        
    Returns:
        PlayerResponse: Created player
        
    Raises:
        ValidationException: If a player with the same email already exists
        DatabaseException: If there's an error creating the player
    """
    # Check if a player with the same email already exists
    existing_player = player_repository.get_by_email(db, player_data.email)
    if existing_player:
        raise ValidationException(f"A player with email {player_data.email} already exists")
    
    # Create the player
    player = player_repository.create_with_password(db, player_data)
    return PlayerResponse.model_validate(player)


@router.patch(
    "/{player_id}",
    response_model=PlayerResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a player",
    description="Update an existing player.",
    tags=["Players"]
)
async def update_player(
    player_id: str = Path(..., description="The ID of the player to update"),
    player_data: PlayerRequestPatch = Body(
        ...,
        example={
            "handicap": 14.5,
            "zip": "90210"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> PlayerResponse:
    """
    Update a player.
    
    Args:
        player_id: Player ID
        player_data: Player data to update
        db: Database session
        current_user: Authenticated user (must be the player or an admin)
        
    Returns:
        PlayerResponse: Updated player
        
    Raises:
        ResourceNotFoundException: If the player is not found
        ValidationException: If trying to update another player without admin privileges
    """
    # Get the player
    player = player_repository.get_or_404(db, player_id)
    
    # Check if the user is updating their own profile or is an admin
    if player.id != current_user.id and not current_user.is_super:
        raise AuthorizationException("You can only update your own player profile")
    
    # If email is being updated, check if it's already in use
    if player_data.email and player_data.email != player.email:
        existing_player = player_repository.get_by_email(db, player_data.email)
        if existing_player:
            raise ValidationException(f"A player with email {player_data.email} already exists")
    
    # Update the player
    player = player_repository.update(db, db_obj=player, obj_in=player_data)
    return PlayerResponse.model_validate(player)


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a player",
    description="Delete a player account (admin only).",
    tags=["Players"]
)
async def delete_player(
    player_id: str = Path(..., description="The ID of the player to delete"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_superuser)
) -> None:
    """
    Delete a player (admin only).
    
    Args:
        player_id: Player ID
        db: Database session
        current_user: Authenticated superuser
        
    Raises:
        ResourceNotFoundException: If the player is not found
    """
    player_repository.remove(db, id=player_id)


@router.post(
    "/setup_super",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Setup Super User",
    description="Create a super user during initial setup. \nRequires a setup key that matches the SETUP_SECRET environment variable.\nThis endpoint should be disabled in production after initial setup.",
    tags=["Players"]
)
async def setup_super_user(
    setup_key: Optional[str] = Header(None, alias="x-setup-key", description="The setup key to verify"),
    player_data: PlayerRequest = Body(
        ...,
        example={
            "name": "Admin User",
            "email": "admin@example.com",
            "zip": "12345",
            "handicap": 5.0,
            "ghin_number": "1234567",
            "password": "securepassword"
        }
    ),
    db: Session = Depends(get_db)
) -> PlayerResponse:
    """
    Create a super user during initial setup.

    Args:
        setup_key: Secret key to verify authorization (passed as x-setup-key header)
        player_data: Player data
        db: Database session

    Returns:
        PlayerResponse: Created super user

    Raises:
        HTTPException: If the setup key is invalid or there's an error creating the user
    """
    # Disable endpoint if SETUP_SECRET is not configured
    if not settings.SETUP_SECRET:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Verify setup key
    if setup_key != settings.SETUP_SECRET:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid setup key")
    
    # Check if email already exists
    existing_player = player_repository.get_by_email(db, player_data.email)
    if existing_player:
        raise ValidationException(f"A player with email {player_data.email} already exists")
    
    try:
        # Create the player with super user rights
        obj_in_data = player_data.model_dump(exclude_unset=True)
        
        # Hash the password if provided
        if player_data.password:
            from core.security import get_password_hash
            obj_in_data["hashed_password"] = get_password_hash(player_data.password)
            del obj_in_data["password"]
        
        # Set super user flag
        obj_in_data["is_super"] = True
        obj_in_data["is_active"] = True
        
        # Create the player
        db_obj = Player(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        logger.info(f"New super user created: {db_obj.id}")
        return PlayerResponse.from_orm(db_obj)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 