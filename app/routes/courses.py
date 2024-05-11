from fastapi import FastAPI, Depends, HTTPException, APIRouter
from typing import List
from db.models import Course, TeeBox, TeeBoxHole
from schemas.pydantic_models import CourseRequest, CourseRequestPatch, TeeBoxBase
from db.database import SessionLocal, get_db
from crud.courses import get_courses, get_a_course_and_tees, delete_a_course, RecordNotFoundException, create_tee_boxes_and_holes
from uuid import UUID

#api_key_header = APIKeyHeader(name='Authorization')
courserouter = APIRouter()
db = SessionLocal()

@courserouter.get('/courses', tags=['Courses'])
async def get_all_courses(name: str = None, db: SessionLocal = Depends(get_db)):
    courses = get_courses(db, name)
    return {"courses": courses, "count": len(courses)}

@courserouter.get('/courses/{course_id}', tags=['Courses'])
async def get_course(course_id: UUID, db: SessionLocal = Depends(get_db)):
    try:
        course_rec = get_a_course_and_tees(db, course_id)
    except RecordNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

    return(course_rec)

@courserouter.delete('/courses/{course_id}', tags=['Courses'])
async def delete_course(course_id: UUID, db: SessionLocal = Depends(get_db)):
    course = delete_a_course(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    return {'message': 'Course and associated tees deleted successfully'}

@courserouter.post("/courses/{course_id}/bulk_tees", tags=['Courses'],)
async def bulk_tees(course_id: UUID, data: List[dict], db: SessionLocal = Depends(get_db)):
    try:
        create_tee_boxes_and_holes(db, course_id, data)
        return {"message": "Data uploaded successfully"}

    except Exception as e:  # Handle any errors
        raise HTTPException(status_code=500, detail=str(e))

@courserouter.post("/courses/", tags=['Courses'])
def create_a_course(course_data: CourseRequest,  db: SessionLocal = Depends(get_db)):
    course = create_course(db, course_data)
    return course

@courserouter.patch("/courses/{course_id}", tags=['Courses'])
def update_course(course_id: UUID, course_data: CourseRequestPatch, db: SessionLocal = Depends(get_db)):
    course_rec = update_a_course(db, course_id, data)
    if course_rec is None:
        raise HTTPException(status_code=404, detail='course not found')
    return course_rec
