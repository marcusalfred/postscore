"""
API endpoints for course management.
"""
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Body, Path, Query, status
from sqlalchemy.orm import Session

from core.security import get_current_active_user, get_current_superuser
from db.database import get_db
from db.models import Course, Player
from repositories.course_repository import course_repository
from schemas.pydantic_models import (
    CourseRequest, CourseRequestPatch, CourseResponse, 
    TeeBoxDetailResponse, TeeBoxHoleDetailResponse
)
from core.errors import ResourceNotFoundException

router = APIRouter()


@router.get(
    "/",
    response_model=List[CourseResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all courses",
    description="Retrieve all golf courses, with optional filtering by name.",
    tags=["Courses"]
)
async def get_courses(
    name: Optional[str] = Query(None, description="Filter courses by name (partial match)"),
    db: Session = Depends(get_db)
) -> List[CourseResponse]:
    """
    Get all courses, optionally filtered by name.
    
    Args:
        name: Optional filter for course name (partial match)
        db: Database session
        
    Returns:
        List[CourseResponse]: List of courses
    """
    return course_repository.get_all_with_tees(db, name=name)


@router.get(
    "/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a specific course",
    description="Retrieve a specific golf course by ID, including tee boxes and holes.",
    tags=["Courses"]
)
async def get_course(
    course_id: str = Path(..., description="The ID of the course to retrieve"),
    db: Session = Depends(get_db)
) -> CourseResponse:
    """
    Get a specific course by ID.
    
    Args:
        course_id: Course ID
        db: Database session
        
    Returns:
        CourseResponse: Course details with tee boxes
        
    Raises:
        ResourceNotFoundException: If the course is not found
    """
    return course_repository.get_with_tees(db, course_id)


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course",
    description="Create a new golf course.",
    tags=["Courses"]
)
async def create_course(
    course_data: CourseRequest = Body(
        ...,
        example={
            "name": "Augusta National Golf Club",
            "address": "2604 Washington Rd",
            "city": "Augusta",
            "state": "GA",
            "zip": "30904",
            "website": "https://www.augusta.com"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> CourseResponse:
    """
    Create a new course.
    
    Args:
        course_data: Course data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        CourseResponse: Created course
    """
    # Create the course
    course = course_repository.create(db, obj_in=course_data)
    
    # Return the course with empty tees
    return CourseResponse(
        id=course.id,
        name=course.name,
        address=course.address,
        city=course.city,
        state=course.state,
        zip=course.zip,
        website=course.website,
        tees=[]
    )


@router.patch(
    "/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a course",
    description="Update an existing golf course.",
    tags=["Courses"]
)
async def update_course(
    course_id: str = Path(..., description="The ID of the course to update"),
    course_data: CourseRequestPatch = Body(
        ...,
        example={
            "website": "https://www.augusta.com",
            "name": "Augusta National Golf Club (Updated)"
        }
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> CourseResponse:
    """
    Update a course.
    
    Args:
        course_id: Course ID
        course_data: Course data to update
        db: Database session
        current_user: Authenticated user
        
    Returns:
        CourseResponse: Updated course
        
    Raises:
        ResourceNotFoundException: If the course is not found
    """
    # Get the course
    course = course_repository.get_or_404(db, course_id)
    
    # Update the course
    course = course_repository.update(db, db_obj=course, obj_in=course_data)
    
    # Return the updated course with tees
    return course_repository.get_with_tees(db, course_id)


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a course",
    description="Delete a golf course and all associated tee boxes and holes.",
    tags=["Courses"]
)
async def delete_course(
    course_id: str = Path(..., description="The ID of the course to delete"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_superuser)
) -> None:
    """
    Delete a course.
    
    Args:
        course_id: Course ID
        db: Database session
        current_user: Authenticated superuser
        
    Raises:
        ResourceNotFoundException: If the course is not found
    """
    course_repository.remove(db, id=course_id)


@router.post(
    "/{course_id}/bulk_tees",
    status_code=status.HTTP_200_OK,
    summary="Add tee boxes to a course",
    description="Add multiple tee boxes with holes to an existing course.",
    tags=["Courses"]
)
async def add_tee_boxes(
    course_id: str = Path(..., description="The ID of the course to add tee boxes to"),
    tee_box_data: List[dict] = Body(
        ...,
        example=[
            {
                "tee_box_name": "Championship",
                "rating": 74.2,
                "slope": 140,
                "yardage": 7475,
                "holes": [
                    {"hole_number": 1, "par": 4, "yardage": 445, "handicap": 4},
                    {"hole_number": 2, "par": 5, "yardage": 575, "handicap": 8}
                    # Additional holes would be included
                ]
            }
        ]
    ),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> dict:
    """
    Add tee boxes to a course.
    
    Args:
        course_id: Course ID
        tee_box_data: List of tee box data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        dict: Success message
        
    Raises:
        ResourceNotFoundException: If the course is not found
        DatabaseException: If there's an error creating the tee boxes
    """
    course_repository.create_tee_boxes(db, course_id, tee_box_data)
    return {"message": "Tee boxes added successfully"}


@router.get(
    "/tee-boxes/{tee_box_id}",
    response_model=TeeBoxDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get detailed tee box information",
    description="Retrieve detailed information for a tee box, including hole IDs.",
    tags=["Courses"]
)
async def get_tee_box_detail(
    tee_box_id: str = Path(..., description="The ID of the tee box to retrieve"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> TeeBoxDetailResponse:
    """
    Get detailed information for a tee box, including hole IDs.
    
    Args:
        tee_box_id: Tee box ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        TeeBoxDetailResponse: Tee box details with hole IDs
        
    Raises:
        ResourceNotFoundException: If the tee box is not found
    """
    tee_box_detail = course_repository.get_tee_box_detail(db, tee_box_id)
    return TeeBoxDetailResponse(**tee_box_detail)


@router.get(
    "/{course_id}/tee-boxes",
    response_model=List[TeeBoxDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all tee boxes for a course with details",
    description="Retrieve all tee boxes for a course with detailed information, including hole IDs.",
    tags=["Courses"]
)
async def get_course_tee_boxes(
    course_id: str = Path(..., description="The ID of the course"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> List[TeeBoxDetailResponse]:
    """
    Get all tee boxes for a course with detailed information.
    
    Args:
        course_id: Course ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[TeeBoxDetailResponse]: List of tee box details with hole IDs
        
    Raises:
        ResourceNotFoundException: If the course is not found
    """
    tee_boxes = course_repository.get_all_tee_boxes_for_course(db, course_id)
    return [TeeBoxDetailResponse(**tee_box) for tee_box in tee_boxes]


@router.get(
    "/tee-box-holes/{tee_box_hole_id}",
    response_model=TeeBoxHoleDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get tee box hole details",
    description="Retrieve detailed information for a specific tee box hole.",
    tags=["Courses"]
)
async def get_tee_box_hole(
    tee_box_hole_id: str = Path(..., description="The ID of the tee box hole to retrieve"),
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_active_user)
) -> TeeBoxHoleDetailResponse:
    """
    Get detailed information for a tee box hole.
    
    Args:
        tee_box_hole_id: Tee box hole ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        TeeBoxHoleDetailResponse: Tee box hole details
        
    Raises:
        ResourceNotFoundException: If the tee box hole is not found
    """
    tee_box_hole = course_repository.get_tee_box_hole(db, tee_box_hole_id)
    return TeeBoxHoleDetailResponse(**tee_box_hole) 