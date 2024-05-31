from .models import Course, TeeBox, TeeBoxHole, Player
from .database import SessionLocal
from sqlalchemy import func
from typing import List
from uuid import UUID
from .pydantic_models import CourseRequest, CourseRequestPatch, CourseResponse, PlayerRequest, PlayerRequestPatch, PlayerResponse
import logging



logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class RecordNotFoundException(Exception):
    pass

def get_courses(db: SessionLocal, name: str = None):

    if name:
        query = db.query(Course).filter(func.lower(Course.name).ilike(f'%{name.lower()}%'))
    else:  # If name is not provided, fetch all courses
        query = db.query(Course)
    course_recs = query.all()
    return course_recs

def get_a_course (db: SessionLocal, course_id: UUID):
    course = db.query(Course).filter(Course.id == course_id).first()
    return course

def get_a_course_and_tees(db: SessionLocal, course_id: UUID):
    """
    Retrieves a single course by ID.

    Args:
        db: Database session object.
        course_id: ID of the course to retrieve.

    Returns:
        Course model instance if found, otherwise None.
    """
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise RecordNotFoundException("Course not found")

    tees = []
    tee_boxes = db.query(TeeBox).filter(TeeBox.course_id == course_id).all()
    for tee_box in tee_boxes:
        tee_box_holes = db.query(TeeBoxHole).filter(TeeBoxHole.tee_box_id == tee_box.id).all()
        tee_box_data = {
            "tee_id": tee_box.id,
            "tee": tee_box.name,
            "rating": tee_box.rating,
            "slope": tee_box.slope,
            "holes": [{"number": hole.hole_number, "par": hole.par, "yards": hole.yardage, "handicap": hole.handicap} for hole in tee_box_holes]
        }
        tees.append(tee_box_data)

    response_data = {
        "id": course.id,
        "name": course.name,
        "location": f"{course.city}, {course.state}",
        "website": course.website,
        "tees": tees
    }
    return CourseResponse(**response_data)

def delete_a_course(db: SessionLocal, course_id: UUID):
    course = db.query(Course).filter(Course.id == course_id).first()
    db.delete(course)
    db.commit()

    return {'message': 'Course and associated tees deleted successfully'}

def create_tee_boxes_and_holes(db: SessionLocal, course_id: UUID, tee_box_data: List[dict]):
    """
    Creates tee boxes and their associated holes based on provided data.
    """
    for item in tee_box_data:
            # Extract data from JSON payload
            tee_box_name = item["tee_box_name"]
            rating = item["rating"]
            slope = item["slope"]
            yardage = item["yardage"]
            hole_data = item["holes"]  # Assuming holes data is a list of dicts

            # Insert data into tee_boxes table
            tee_box = TeeBox(course_id=course_id, name=tee_box_name, rating=rating, slope=slope, yardage=yardage)
            db.add(tee_box)
            db.commit()

            # Insert data into tee_box_holes table
            for hole in hole_data:
                hole_number = hole["hole_number"]
                par = hole["par"]
                yardage = hole["yardage"]
                handicap = hole["handicap"]

                tee_box_hole = TeeBoxHole(tee_box_id=tee_box.id, hole_number=hole_number, par=par, yardage=yardage, handicap=handicap)
                db.add(tee_box_hole)
                db.commit()

def create_course(db: SessionLocal, course_data: CourseRequest):
    new_course = Course(**course_data.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

def update_a_course(db: SessionLocal, course_id: UUID, course_data: CourseRequestPatch):
    course = db.query(Course).filter(Course.id == course_id).first()
    for attr, value in course_data.dict(exclude_unset=True).items():
        if hasattr(course, attr):
            setattr(course, attr, value)
    db.commit()
    db.refresh(course)

    return course


def get_players(db: SessionLocal, name: str = None):
    if name:
        query = db.query(Player).filter(func.lower(Player.name).ilike(f'%{name.lower()}%'))
        player_recs = query.all()
    else:
        player_recs = db.query(Player).all()
    return player_recs

def get_player_by_id(db: SessionLocal, player_id: UUID):
    player_rec = db.query(Player).filter(Player.id == player_id).first()
    return player_rec

def create_player(db: SessionLocal, player_data: PlayerRequest):
    new_player = Player(**player_data.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

def update_player(db: SessionLocal, player_id: UUID, data: PlayerRequestPatch):
    player_rec = db.query(Player).filter(Player.id == player_id).first()
    for attr, value in data.dict(exclude_unset=True).items():
        if hasattr(player_rec, attr):
            setattr(player_rec, attr, value)
    db.commit()
    db.refresh(player_rec)
    return player_rec

def delete_player(db: SessionLocal, player_id: UUID):
    player_rec = db.query(Player).filter(Player.id == player_id).first()
    db.delete(player_rec)
    db.commit()
    db.close()
    return {'message': 'player_rec deleted successfully'}