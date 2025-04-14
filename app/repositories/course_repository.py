"""
Course repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import Course, TeeBox, TeeBoxHole
from schemas.pydantic_models import CourseCreate, CourseRequestPatch, CourseResponse
from repositories.base import BaseRepository
from core.errors import ResourceNotFoundException, DatabaseException


class CourseRepository(BaseRepository[Course, CourseCreate, CourseRequestPatch]):
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
        return db.query(self.model).filter(func.lower(self.model.name).ilike(f'%{name.lower()}%')).all()
    
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
        return db.query(self.model).all()
    
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
        course = self.get(db, course_id)
        
        if course is None:
            raise ResourceNotFoundException("Course", course_id)
        
        tees = []
        tee_boxes = db.query(TeeBox).filter(TeeBox.course_id == course_id).all()
        
        for tee_box in tee_boxes:
            tee_box_holes = db.query(TeeBoxHole).filter(TeeBoxHole.tee_box_id == tee_box.id).all()
            tee_box_data = {
                "tee_id": tee_box.id,
                "tee": tee_box.name,
                "rating": tee_box.rating,
                "slope": tee_box.slope,
                "holes": [
                    {"number": hole.hole_number, "par": hole.par, "yards": hole.yardage, "handicap": hole.handicap} 
                    for hole in tee_box_holes
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
                db.commit()
                db.refresh(tee_box)
                
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
        tee_box = db.query(TeeBox).filter(TeeBox.id == tee_box_id).first()
        
        if tee_box is None:
            raise ResourceNotFoundException("TeeBox", tee_box_id)
        
        # Query all tee box holes
        tee_box_holes = db.query(TeeBoxHole).filter(TeeBoxHole.tee_box_id == tee_box_id).all()
        
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
        
        # Query all tee boxes for the course
        tee_boxes = db.query(TeeBox).filter(TeeBox.course_id == course_id).all()
        
        # Create response data
        response_data = []
        for tee_box in tee_boxes:
            tee_box_holes = db.query(TeeBoxHole).filter(TeeBoxHole.tee_box_id == tee_box.id).all()
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
        tee_box_hole = db.query(TeeBoxHole).filter(TeeBoxHole.id == tee_box_hole_id).first()
        
        if tee_box_hole is None:
            raise ResourceNotFoundException("TeeBoxHole", tee_box_hole_id)
        
        # Query the tee box to include additional context
        tee_box = db.query(TeeBox).filter(TeeBox.id == tee_box_hole.tee_box_id).first()
        
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