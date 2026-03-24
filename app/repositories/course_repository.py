"""
Course repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from db.models import Course, TeeBox, TeeBoxHole
from schemas.pydantic_models import CourseRequest, CourseRequestPatch, CourseResponse
from repositories.base import BaseRepository
from core.errors import ResourceNotFoundException, DatabaseException


class CourseRepository(BaseRepository[Course, CourseRequest, CourseRequestPatch]):
    """
    Repository for Course operations.
    """
    
    def __init__(self):
        super().__init__(Course)
    
    def get_by_name(self, db: Session, name: str) -> List[Course]:
        """
        Get courses by name (partial match, case-insensitive).
        
        Args:
            db: Database session
            name: Course name to search for
            
        Returns:
            List[Course]: List of matching courses
        """
        return db.execute(select(self.model).where(self.model.name.ilike(f'%{name}%'))).scalars().all()

    def get_all(self, db: Session, name: Optional[str] = None) -> List[Course]:
        """
        Get all courses, optionally filtered by name.

        Args:
            db: Database session
            name: Optional name filter

        Returns:
            List[Course]: List of courses
        """
        if name:
            return self.get_by_name(db, name)
        return db.execute(select(self.model)).scalars().all()
    
    def get_all_with_tees(self, db: Session, name: Optional[str] = None) -> List[CourseResponse]:
        """
        Get all courses with their tee boxes and holes eagerly loaded.

        Args:
            db: Database session
            name: Optional name filter

        Returns:
            List[CourseResponse]: List of courses with tees and holes
        """
        stmt = select(self.model).options(
            selectinload(Course.tees).selectinload(TeeBox.hole)
        )
        if name:
            stmt = stmt.where(self.model.name.ilike(f'%{name}%'))
        courses = db.execute(stmt).scalars().all()

        response = []
        for course in courses:
            tees = [
                {
                    "tee_id": tee_box.id,
                    "tee": tee_box.name,
                    "rating": tee_box.rating,
                    "slope": tee_box.slope,
                    "holes": [
                        {"number": hole.hole_number, "par": hole.par, "yards": hole.yardage, "handicap": hole.handicap}
                        for hole in tee_box.hole
                    ]
                }
                for tee_box in course.tees
            ]
            response.append(CourseResponse(
                id=course.id,
                name=course.name,
                address=course.address,
                city=course.city,
                state=course.state,
                zip=course.zip,
                website=course.website,
                tees=tees
            ))
        return response

    def get_with_tees(self, db: Session, course_id: str) -> CourseResponse:
        """
        Get a course with its tee boxes and holes.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            CourseResponse: Course data with tees
            
        Raises:
            ResourceNotFoundException: If the course is not found
        """
        course = db.execute(
            select(Course)
            .where(Course.id == course_id)
            .options(selectinload(Course.tees).selectinload(TeeBox.hole))
        ).scalar_one_or_none()

        if course is None:
            raise ResourceNotFoundException("Course", course_id)

        tees = []
        for tee_box in course.tees:
            tee_box_data = {
                "tee_id": tee_box.id,
                "tee": tee_box.name,
                "rating": tee_box.rating,
                "slope": tee_box.slope,
                "holes": [
                    {"number": hole.hole_number, "par": hole.par, "yards": hole.yardage, "handicap": hole.handicap}
                    for hole in tee_box.hole
                ]
            }
            tees.append(tee_box_data)
        
        # Create response data
        response_data = {
            "id": course.id,
            "name": course.name,
            "address": course.address,
            "city": course.city,
            "state": course.state,
            "zip": course.zip,
            "website": course.website,
            "tees": tees
        }
        
        return CourseResponse(**response_data)
    
    def create_tee_boxes(self, db: Session, course_id: str, tee_box_data: List[Dict[str, Any]]) -> None:
        """
        Create tee boxes and holes for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            tee_box_data: List of tee box data dictionaries
            
        Raises:
            ResourceNotFoundException: If the course is not found
            DatabaseException: If there's an error creating the tee boxes
        """
        # Verify the course exists
        course = self.get(db, course_id)
        if course is None:
            raise ResourceNotFoundException("Course", course_id)
        
        try:
            for item in tee_box_data:
                # Extract data from JSON payload
                tee_box_name = item["tee_box_name"]
                rating = item["rating"]
                slope = item["slope"]
                yardage = item["yardage"]
                hole_data = item["holes"]
                
                # Insert data into tee_boxes table
                tee_box = TeeBox(
                    course_id=course_id, 
                    name=tee_box_name, 
                    rating=rating, 
                    slope=slope, 
                    yardage=yardage
                )
                db.add(tee_box)
                db.flush()  # assigns tee_box.id without committing

                # Insert data into tee_box_holes table
                for hole in hole_data:
                    hole_number = hole["hole_number"]
                    par = hole["par"]
                    yardage = hole["yardage"]
                    handicap = hole["handicap"]

                    tee_box_hole = TeeBoxHole(
                        tee_box_id=tee_box.id,
                        hole_number=hole_number,
                        par=par,
                        yardage=yardage,
                        handicap=handicap
                    )
                    db.add(tee_box_hole)
            db.commit()

        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error creating tee boxes: {str(e)}")
    
    def get_tee_box_detail(self, db: Session, tee_box_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a tee box, including hole IDs.
        
        Args:
            db: Database session
            tee_box_id: Tee box ID
            
        Returns:
            Dict[str, Any]: Tee box data with hole details including IDs
            
        Raises:
            ResourceNotFoundException: If the tee box is not found
        """
        # Query the tee box
        tee_box = db.execute(select(TeeBox).where(TeeBox.id == tee_box_id)).scalar_one_or_none()

        if tee_box is None:
            raise ResourceNotFoundException("TeeBox", tee_box_id)

        # Query all tee box holes
        tee_box_holes = db.execute(select(TeeBoxHole).where(TeeBoxHole.tee_box_id == tee_box_id)).scalars().all()
        
        # Create response data
        response_data = {
            "id": tee_box.id,
            "name": tee_box.name,
            "course_id": tee_box.course_id,
            "rating": tee_box.rating,
            "slope": tee_box.slope,
            "yardage": tee_box.yardage,
            "hex": tee_box.hex,
            "holes": [
                {
                    "id": hole.id,
                    "number": hole.hole_number,
                    "par": hole.par,
                    "yards": hole.yardage,
                    "handicap": hole.handicap
                } 
                for hole in tee_box_holes
            ]
        }
        
        return response_data
    
    def get_all_tee_boxes_for_course(self, db: Session, course_id: str) -> List[Dict[str, Any]]:
        """
        Get all tee boxes with detailed information for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List[Dict[str, Any]]: List of tee box data with hole details including IDs
            
        Raises:
            ResourceNotFoundException: If the course is not found
        """
        # Verify the course exists
        course = self.get(db, course_id)
        if course is None:
            raise ResourceNotFoundException("Course", course_id)
        
        # Query all tee boxes with holes eagerly loaded to avoid N+1
        tee_boxes = db.execute(
            select(TeeBox).where(TeeBox.course_id == course_id).options(selectinload(TeeBox.hole))
        ).scalars().all()

        # Create response data
        response_data = []
        for tee_box in tee_boxes:
            tee_box_holes = tee_box.hole
            tee_box_data = {
                "id": tee_box.id,
                "name": tee_box.name,
                "course_id": tee_box.course_id,
                "rating": tee_box.rating,
                "slope": tee_box.slope,
                "yardage": tee_box.yardage,
                "hex": tee_box.hex,
                "holes": [
                    {
                        "id": hole.id,
                        "number": hole.hole_number,
                        "par": hole.par,
                        "yards": hole.yardage,
                        "handicap": hole.handicap
                    } 
                    for hole in tee_box_holes
                ]
            }
            response_data.append(tee_box_data)
        
        return response_data
    
    def get_tee_box_hole(self, db: Session, tee_box_hole_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a tee box hole.
        
        Args:
            db: Database session
            tee_box_hole_id: Tee box hole ID
            
        Returns:
            Dict[str, Any]: Tee box hole data
            
        Raises:
            ResourceNotFoundException: If the tee box hole is not found
        """
        # Query the tee box hole
        tee_box_hole = db.execute(select(TeeBoxHole).where(TeeBoxHole.id == tee_box_hole_id)).scalar_one_or_none()

        if tee_box_hole is None:
            raise ResourceNotFoundException("TeeBoxHole", tee_box_hole_id)

        # Query the tee box to include additional context
        tee_box = db.execute(select(TeeBox).where(TeeBox.id == tee_box_hole.tee_box_id)).scalar_one_or_none()
        
        # Create response data
        response_data = {
            "id": tee_box_hole.id,
            "tee_box_id": tee_box_hole.tee_box_id,
            "number": tee_box_hole.hole_number,
            "par": tee_box_hole.par,
            "yards": tee_box_hole.yardage,
            "handicap": tee_box_hole.handicap,
            "tee_box_name": tee_box.name if tee_box else None,
            "course_id": tee_box.course_id if tee_box else None
        }
        
        return response_data


# Create a singleton instance
course_repository = CourseRepository() 