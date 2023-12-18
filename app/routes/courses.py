from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, Security
from fastapi.security.api_key import APIKeyHeader
from utils.auth import verify_api_key
from sqlalchemy import func
from typing import List
from models import Course, CourseRequest, TeeBoxCreate, CourseCreate, CourseRequestPatch, CourseResponse, TeeBox, TeeBoxResponse, TeeBoxRequest, TeeBoxPatchRequest
from db import SessionLocal
from pydantic import BaseModel
import datetime

api_key_header = APIKeyHeader(name='Authorization')
courserouter = APIRouter()

@courserouter.get('/courses', tags=['Courses'])
async def get_all_courses(name: str = None):

    db = SessionLocal()
    query = db.query(Course)

    if name:
        query = query.filter(func.lower(Course.name).ilike(f'%{name.lower()}%'))
    records = query.all()
    record_count = len(records)
    db.close()

    courses =  [{
            'id': record.id,
            'name': record.name,
            'address': record.address,
            'city': record.city,
            'state': record.state,
            'zip': record.zip,
            'website': record.website,
            'par': record.par
        } for record in records]

    return {'courses': courses, 'count': record_count}

@courserouter.get('/courses/{course_id}', tags=['Courses'])
async def get_course(course_id: int):
    db = SessionLocal()
    record = db.query(Course).filter(Course.id == course_id).first()
    db.close()
    if record is None:
        raise HTTPException(status_code=404, detail='course not found')
    tees = db.query(TeeBox).filter(TeeBox.course_id == course_id).all()
    par_values = {f'hole{idx}_par': getattr(record, f'hole{idx}_par') for idx in range(1, 19)}
    handicap_values = {f'hole{idx}_handicap': getattr(record, f'hole{idx}_handicap') for idx in range(1, 19)}

    course_data = {
        'id': record.id,
        'name': record.name,
        'address': record.address,
        'city': record.city,
        'state': record.state,
        'zip': record.zip,
        'website': record.website,
        'par': record.par,
        'scorecard': [],
        'teeBoxes': []
    }

    # Prepare hole data first
    for hole_number in range(1, 19):  # Assuming 18 holes
        hole_data = {
            'hole': hole_number,
            'par': par_values[f'hole{hole_number}_par'],
            'handicap': handicap_values[f'hole{hole_number}_handicap'],
            'tees': []
        }
        for tee in tees:
            tee_yards = getattr(tee, f'hole{hole_number}_yards')
            tee_info = {
                'id': tee.id,
                'color': tee.name,  # Add color or another field
                'yards': tee_yards
            }
            hole_data['tees'].append(tee_info)

        course_data['scorecard'].append(hole_data)

    # Prepare teeBoxes data
    for tee in tees:
        tee_info = {
            'id': tee.id,
            'tee': tee.name,
            'slope': tee.slope,
            'handicap': tee.rating,
            'yardage': tee.yardage,
            'hex': tee.hex
            # Add other tee-related fields
        }
        course_data['teeBoxes'].append(tee_info)

    db.close()
    return [course_data]

@courserouter.patch('/courses/{course_id}', tags=['Courses'], response_model=CourseResponse, dependencies=[Depends(verify_api_key)])
async def update_course(course_id: int, data: CourseRequestPatch):
    db = SessionLocal()
    record = db.query(Course).filter(Course.id == course_id).first()

    if not record:
        db.close()
        return {'message': 'Record not found'}
    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    updated_record = db.query(Course).filter(Course.id == course_id).first()
    db.close()
    return {'id': updated_record.id,
        'name': updated_record.name,
        'address': updated_record.address,
        'city': updated_record.city,
        'state': updated_record.state,
        'zip': updated_record.zip,
        'website': updated_record.website,
        'par': updated_record.par,
        'hole1_par': updated_record.hole1_par,
        'hole2_par': updated_record.hole2_par,
        'hole3_par': updated_record.hole3_par,
        'hole4_par': updated_record.hole4_par,
        'hole5_par': updated_record.hole5_par,
        'hole6_par': updated_record.hole6_par,
        'hole7_par': updated_record.hole7_par,
        'hole8_par': updated_record.hole8_par,
        'hole9_par': updated_record.hole9_par,
        'hole10_par': updated_record.hole10_par,
        'hole11_par': updated_record.hole11_par,
        'hole12_par': updated_record.hole12_par,
        'hole13_par': updated_record.hole13_par,
        'hole14_par': updated_record.hole14_par,
        'hole15_par': updated_record.hole15_par,
        'hole16_par': updated_record.hole16_par,
        'hole17_par': updated_record.hole17_par,
        'hole18_par': updated_record.hole18_par,
        'hole1_handicap': updated_record.hole1_handicap,
        'hole2_handicap': updated_record.hole2_handicap,
        'hole3_handicap': updated_record.hole3_handicap,
        'hole4_handicap': updated_record.hole4_handicap,
        'hole5_handicap': updated_record.hole5_handicap,
        'hole6_handicap': updated_record.hole6_handicap,
        'hole7_handicap': updated_record.hole7_handicap,
        'hole8_handicap': updated_record.hole8_handicap,
        'hole9_handicap': updated_record.hole9_handicap,
        'hole10_handicap': updated_record.hole10_handicap,
        'hole11_handicap': updated_record.hole11_handicap,
        'hole12_handicap': updated_record.hole12_handicap,
        'hole13_handicap': updated_record.hole13_handicap,
        'hole14_handicap': updated_record.hole14_handicap,
        'hole15_handicap': updated_record.hole15_handicap,
        'hole16_handicap': updated_record.hole16_handicap,
        'hole17_handicap': updated_record.hole17_handicap,
        'hole18_handicap': updated_record.hole18_handicap}



@courserouter.post('/teeboxes', tags=['Courses'], response_model=TeeBoxResponse, dependencies=[Depends(verify_api_key)])
async def add_teebox(teebox: TeeBoxRequest):
    db = SessionLocal()
    new_record = TeeBox(**teebox.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()

    return {
        'id': new_record.id,
        'name': new_record.name,
        'course_id': new_record.course_id,
        'rating': new_record.rating,
        'slope': new_record.slope,
        'yardage': new_record.yardage,
        'hex': new_record.hex,
        'hole1_yards': new_record.hole1_yards,
        'hole2_yards': new_record.hole2_yards,
        'hole3_yards': new_record.hole3_yards,
        'hole4_yards': new_record.hole4_yards,
        'hole5_yards': new_record.hole5_yards,
        'hole6_yards': new_record.hole6_yards,
        'hole7_yards': new_record.hole7_yards,
        'hole8_yards': new_record.hole8_yards,
        'hole9_yards': new_record.hole9_yards,
        'hole10_yards': new_record.hole10_yards,
        'hole11_yards': new_record.hole11_yards,
        'hole12_yards': new_record.hole12_yards,
        'hole13_yards': new_record.hole13_yards,
        'hole14_yards': new_record.hole14_yards,
        'hole15_yards': new_record.hole15_yards,
        'hole16_yards': new_record.hole16_yards,
        'hole17_yards': new_record.hole17_yards,
        'hole18_yards': new_record.hole18_yards
    }


@courserouter.patch('/teeboxes/{tee_box_id}', tags=['Courses'], response_model=TeeBoxResponse, dependencies=[Depends(verify_api_key)])
async def update_teebox(tee_box_id: int, data: TeeBoxPatchRequest):
    db = SessionLocal()
    record = db.query(TeeBox).filter(TeeBox.id == tee_box_id).first()

    if not record:
        db.close()
        return {'message': 'Record not found'}
    for field, value in data.dict(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    updated_record = db.query(TeeBox).filter(TeeBox.id == tee_box_id).first()
    db.close()
    return {
        'id': updated_record.id,
        'name': updated_record.name,
        'course_id': updated_record.course_id,
        'rating': updated_record.rating,
        'slope': updated_record.slope,
        'yardage': updated_record.yardage,
        'hex': updated_record.hex,
        'hole1_yards': updated_record.hole1_yards,
        'hole2_yards': updated_record.hole2_yards,
        'hole3_yards': updated_record.hole3_yards,
        'hole4_yards': updated_record.hole4_yards,
        'hole5_yards': updated_record.hole5_yards,
        'hole6_yards': updated_record.hole6_yards,
        'hole7_yards': updated_record.hole7_yards,
        'hole8_yards': updated_record.hole8_yards,
        'hole9_yards': updated_record.hole9_yards,
        'hole10_yards': updated_record.hole10_yards,
        'hole11_yards': updated_record.hole11_yards,
        'hole12_yards': updated_record.hole12_yards,
        'hole13_yards': updated_record.hole13_yards,
        'hole14_yards': updated_record.hole14_yards,
        'hole15_yards': updated_record.hole15_yards,
        'hole16_yards': updated_record.hole16_yards,
        'hole17_yards': updated_record.hole17_yards,
        'hole18_yards': updated_record.hole18_yards
    }

@courserouter.delete('/teeboxes/{tee_box_id}', tags=['Courses'], dependencies=[Depends(verify_api_key)])
async def delete_teebox(tee_box_id: int):
    db = SessionLocal()
    teebox = db.query(TeeBox).filter(TeeBox.id == tee_box_id).first()

    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    db.delete(teebox)
    db.commit()
    db.close()

    return {'message': 'tee deleted successfully'}

@courserouter.post('/courses', tags=['Courses'], dependencies=[Depends(verify_api_key)])
async def create_course_and_tees(course_data: CourseCreate):
    db = SessionLocal()

    # Create Course instance
    course = Course(**course_data.dict(exclude={'tees'}))  # Exclude tees from course data

    db.add(course)
    db.commit()
    db.refresh(course)

    # Create TeeBox instances
    if course_data.tees:
        for tee_data in course_data.tees:
            tee = TeeBox(**tee_data, course_id=course.id)  # Assuming course_id is the foreign key
            db.add(tee)

        db.commit()
    db.close()

    return {'message': 'Course and Tees created successfully'}

@courserouter.delete('/courses/{course_id}', tags=['Courses'], dependencies=[Depends(verify_api_key)])
async def delete_course(course_id: int):
    db = SessionLocal()
    course = db.query(Course).filter(Course.id == course_id).first()

    if course is None:
        raise HTTPException(status_code=404, detail='Course not found')

    db.delete(course)
    db.commit()
    db.close()

    return {'message': 'Course and associated tees deleted successfully'}

