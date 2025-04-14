"""
API endpoints for round management.
"""
from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, Body, Path, Query, status
from sqlalchemy.orm import Session

from core.security import get_current_active_user, get_current_superuser
from db.database import get_db
from db.models import Player, Round, RoundHole, Course, TeeBox, TeeBoxHole
from repositories.round_repository import round_repository
from schemas.pydantic_models import (
    RoundRequest, RoundPatchRequest, RoundResponse,
    RoundHoleRequest, RoundHolePatchRequest, RoundHoleResponse, RoundHoleDetailResponse,
    RoundStatsResponse
)
from core.errors import ResourceNotFoundException, ValidationException, DatabaseException

router = APIRouter()


@router.get(
    "/",
    response_model=List[RoundResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all rounds",
    description="Retrieve all rounds, with optional filtering by player or course.",
    tags=["Rounds"]
)
async def get_rounds(
    player_id: Optional[str] = Query(None, description="Filter rounds by player ID"),
    course_id: Optional[str] = Query(None, description="Filter rounds by course ID"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> List[RoundResponse]:
    """
    Get all rounds, optionally filtered by player or course.
    
    Args:
        player_id: Optional filter for player ID
        course_id: Optional filter for course ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[RoundResponse]: List of rounds
    """
    if player_id:
        rounds = round_repository.get_by_player(db, player_id)
    elif course_id:
        rounds = round_repository.get_by_course(db, course_id)
    else:
        rounds = round_repository.get_multi(db)
    
    return [RoundResponse.from_orm(round_obj) for round_obj in rounds]


@router.get(
    "/{round_id}",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get a specific round",
    description="Retrieve a specific round by ID, including its holes.",
    tags=["Rounds"]
)
async def get_round(
    round_id: str = Path(..., description="The ID of the round to retrieve"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Get a specific round by ID, including its holes.
    
    Args:
        round_id: Round ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Dict[str, Any]: Round details with holes
        
    Raises:
        ResourceNotFoundException: If the round is not found
    """
    return round_repository.get_round_with_holes(db, round_id)


@router.post(
    "/",
    response_model=RoundResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new round",
    description="Create a new round of golf.",
    tags=["Rounds"]
)
async def create_round(
    round_data: RoundRequest = Body(
        ...,
        example={
            "course_id": "01H0JMVKHWBH8QRE098XVGC9X4",
            "tee_box_id": "01H0JMVKHWBH8QRE098XVGC9X5",
            "player_id": "01H0JMVKHWBH8QRE098XVGC9X6",
            "holes": 18,
            "start_time": "2023-10-20T08:30:00Z"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> RoundResponse:
    """
    Create a new round.
    
    Args:
        round_data: Round data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        RoundResponse: Created round
        
    Raises:
        ValidationException: If user tries to create a round for another player
        DatabaseException: If there's an error creating the round
    """
    # Check if the user is creating a round for themselves or is an admin
    if round_data.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only create rounds for yourself")
    
    # Create the round
    round_obj = round_repository.create(db, obj_in=round_data)
    return RoundResponse.from_orm(round_obj)


@router.patch(
    "/{round_id}",
    response_model=RoundResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a round",
    description="Update an existing round.",
    tags=["Rounds"]
)
async def update_round(
    round_id: str = Path(..., description="The ID of the round to update"),
    round_data: RoundPatchRequest = Body(
        ...,
        example={
            "total_score": 72,
            "end_time": "2023-10-20T12:30:00Z"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> RoundResponse:
    """
    Update a round.
    
    Args:
        round_id: Round ID
        round_data: Round data to update
        db: Database session
        current_user: Authenticated user
        
    Returns:
        RoundResponse: Updated round
        
    Raises:
        ResourceNotFoundException: If the round is not found
        ValidationException: If user tries to update a round for another player
    """
    # Get the round
    round_obj = round_repository.get_or_404(db, round_id)
    
    # Check if the user is updating their own round or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only update your own rounds")
    
    # Update the round
    round_obj = round_repository.update(db, db_obj=round_obj, obj_in=round_data)
    return RoundResponse.from_orm(round_obj)


@router.delete(
    "/{round_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a round",
    description="Delete a round and all its holes.",
    tags=["Rounds"]
)
async def delete_round(
    round_id: str = Path(..., description="The ID of the round to delete"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> None:
    """
    Delete a round.
    
    Args:
        round_id: Round ID
        db: Database session
        current_user: Authenticated user
        
    Raises:
        ResourceNotFoundException: If the round is not found
        ValidationException: If user tries to delete a round for another player
    """
    # Get the round
    round_obj = round_repository.get_or_404(db, round_id)
    
    # Check if the user is deleting their own round or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only delete your own rounds")
    
    # Delete the round
    round_repository.remove(db, id=round_id)


@router.post(
    "/holes",
    response_model=RoundHoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a hole to a round",
    description="Record a score for a hole in a round.",
    tags=["Rounds"]
)
async def add_round_hole(
    hole_data: RoundHoleRequest = Body(
        ...,
        example={
            "round_id": "01H0JMVKHWBH8QRE098XVGC9X7",
            "tee_box_hole_id": "01H0JMVKHWBH8QRE098XVGC9X8",
            "score": 4,
            "gir": True,
            "fairway": "o",
            "putts": 2
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> RoundHoleResponse:
    """
    Add a hole to a round.
    
    Args:
        hole_data: Hole data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        RoundHoleResponse: Created hole
        
    Raises:
        ResourceNotFoundException: If the round is not found
        ValidationException: If user tries to add a hole to another player's round
        ValidationException: If a score for this hole already exists in the round
        DatabaseException: If there's an error creating the hole
    """
    # Get the round
    round_obj = round_repository.get_or_404(db, hole_data.round_id)
    
    # Check if the user is adding a hole to their own round or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only add holes to your own rounds")
    
    # Extract non-pydantic fields
    hole_dict = hole_data.dict(exclude={"round_id", "tee_box_hole_id"})
    
    # Add the hole
    round_hole = round_repository.add_round_hole(
        db, hole_data.round_id, hole_data.tee_box_hole_id, hole_dict
    )
    
    return RoundHoleResponse.from_orm(round_hole)


@router.patch(
    "/holes/{round_hole_id}",
    response_model=RoundHoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a round hole",
    description="Update a score for a hole in a round.",
    tags=["Rounds"]
)
async def update_round_hole(
    round_hole_id: str = Path(..., description="The ID of the round hole to update"),
    hole_data: RoundHolePatchRequest = Body(
        ...,
        example={
            "score": 5,
            "putts": 3
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> RoundHoleResponse:
    """
    Update a round hole.
    
    Args:
        round_hole_id: Round hole ID
        hole_data: Hole data to update
        db: Database session
        current_user: Authenticated user
        
    Returns:
        RoundHoleResponse: Updated hole
        
    Raises:
        ResourceNotFoundException: If the round hole is not found
        ValidationException: If user tries to update a hole for another player's round
        DatabaseException: If there's an error updating the hole
    """
    # Get the round hole
    round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
    if round_hole is None:
        raise ResourceNotFoundException("RoundHole", round_hole_id)
    
    # Get the round
    round_obj = round_repository.get_or_404(db, round_hole.round_id)
    
    # Check if the user is updating a hole for their own round or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only update holes for your own rounds")
    
    # Update the hole
    round_hole = round_repository.update_round_hole(
        db, round_hole_id, hole_data.dict(exclude_unset=True)
    )
    
    return RoundHoleResponse.from_orm(round_hole)


@router.delete(
    "/holes/{round_hole_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a round hole",
    description="Delete a hole score from a round.",
    tags=["Rounds"]
)
async def delete_round_hole(
    round_hole_id: str = Path(..., description="The ID of the round hole to delete"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> None:
    """
    Delete a round hole.
    
    Args:
        round_hole_id: Round hole ID
        db: Database session
        current_user: Authenticated user
        
    Raises:
        ResourceNotFoundException: If the round hole is not found
        ValidationException: If user tries to delete a hole for another player's round
        DatabaseException: If there's an error deleting the hole
    """
    # Get the round hole
    round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
    if round_hole is None:
        raise ResourceNotFoundException("RoundHole", round_hole_id)
    
    # Get the round
    round_obj = round_repository.get_or_404(db, round_hole.round_id)
    
    # Check if the user is deleting a hole for their own round or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only delete holes for your own rounds")
    
    # Delete the hole
    round_repository.delete_round_hole(db, round_hole_id)


@router.get(
    "/holes/{round_hole_id}",
    response_model=RoundHoleDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get round hole details",
    description="Retrieve detailed information for a specific round hole including context.",
    tags=["Rounds"]
)
async def get_round_hole(
    round_hole_id: str = Path(..., description="The ID of the round hole to retrieve"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> RoundHoleDetailResponse:
    """
    Get detailed information for a round hole.
    
    Args:
        round_hole_id: Round hole ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        RoundHoleDetailResponse: Round hole details with context
        
    Raises:
        ResourceNotFoundException: If the round hole is not found
        ValidationException: If user tries to access a hole for another player's round
    """
    # Get the round hole
    round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
    if round_hole is None:
        raise ResourceNotFoundException("RoundHole", round_hole_id)
    
    # Get the round
    round_obj = round_repository.get_or_404(db, round_hole.round_id)
    
    # Check if the user is accessing their own round hole or is an admin
    if round_obj.player_id != current_user.id and not current_user.is_super:
        raise ValidationException("You can only access holes for your own rounds")
    
    # Get the round hole details
    return round_repository.get_round_hole(db, round_hole_id) 