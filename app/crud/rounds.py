from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, Security
from fastapi.security.api_key import APIKeyHeader
from utils.auth import verify_api_key
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from db.models import Round, RoundHole, TeeBoxHole
from schemas.pydantic_models import RoundRequest, RoundPatchRequest, RoundResponse, RoundHoleRequest, RoundHoleResponse, RoundHolePatchRequest
from db.database import SessionLocal
from pydantic import BaseModel
from uuid import UUID
import datetime

#api_key_header = APIKeyHeader(name='Authorization')
#roundrouter = APIRouter(dependencies=[Depends(verify_api_key)])
roundrouter = APIRouter()
db = SessionLocal()

@roundrouter.post('/rounds', tags=['Rounds'], response_model=RoundResponse)
async def add_round(data: RoundRequest):
    new_record = Round(
        course_id=data.course_id,
        tee_box_id=data.tee_box_id,
        player_id=data.player_id,
        total_score=data.total_score,
        holes=data.holes)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()
    return {
        'id': new_record.id,
        'course_id': new_record.course_id,
        'tee_box_id': new_record.tee_box_id,
        'player_id': new_record.player_id,
        'total_score': new_record.total_score,
        'holes': new_record.holes
        }


@roundrouter.post('/rounds/{round_id}/hole/{hole_number}', tags=['Rounds'], response_model=RoundHoleResponse)
async def add_roundhole(round_id: UUID, hole_number: int, data: RoundHoleRequest):
   # Find the teebox id associated with the round
    round_row = db.query(Round).filter(Round.id == round_id).first()
    if not round_row:
        raise HTTPException(status_code=404, detail="Round not found")
    tee_box_id = round_row.tee_box_id

    # Find the corresponding tee_box_hole_id using the hole_number and teebox_id
    tee_box_hole = db.query(TeeBoxHole).filter(TeeBoxHole.tee_box_id == tee_box_id, TeeBoxHole.hole_number == hole_number).first()
    if not tee_box_hole:
        raise HTTPException(status_code=404, detail="TeeBoxHole not found")

    # Check if a RoundHole record with the same round_id and tee_box_hole_id already exists
    existing_record = db.query(RoundHole).filter(RoundHole.round_id == round_id, RoundHole.tee_box_hole_id == tee_box_hole.id).first()
    if existing_record:
        raise HTTPException(status_code=400, detail="RoundHole record already exists")

    try:

        new_record = RoundHole(
            round_id=data.round_id,
            tee_box_hole_id=tee_box_hole.id,
            score=data.score,
            gir=data.gir,
            fairway=data.fairway,
            putts=data.putts#,
            #penalties=data.penalties,
            #sand=data.sand,
            #water=data.water
            )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        round_row.total_score = db.query(func.sum(RoundHole.score)).filter(RoundHole.round_id == round_id).scalar() or 0
        round_row.holes = db.query(func.count(RoundHole.id)).filter(RoundHole.round_id == round_id).scalar() or 0
        db.commit()

        # Refresh the Round record to reflect the changes made in the database
        db.refresh(round_row)


        return {
            'id': new_record.id,
            'round_id': new_record.round_id,
            'tee_box_hole_id': new_record.tee_box_hole_id,
            'score': new_record.score,
            'hole_number': tee_box_hole.hole_number,
            'gir': new_record.gir,
            'fairway': new_record.fairway,
            'putts': new_record.putts#,
            #'penalties': new_record.penalties,
            #'sand': new_record.sand,
            #'water': new_record.water
        }
    except IntegrityError as e:
        # Handle the integrity error (e.g., log the error, inform the user, etc.)
        # For example:
        raise HTTPException(status_code=400, detail="Duplicate RoundHole record")
    finally:
        db.close()


@roundrouter.get('/rounds', tags=['Rounds'])
async def get_all_rounds(player_id: UUID = None):

    query = db.query(Round)
    if player_id:
        query = query.filter(Round.player_id == player_id)
    records = query.all()
    record_count = len(records)
    db.close()

    rounds =  [{
            'id': record.id,
            'course_id': record.course_id,
            'player_id': record.player_id,
            'tee_box_id': record.tee_box_id,
            'total_score': record.total_score,
            'holes': record.holes,
            'start': record.start_time,
            'end': record.end_time#,
           # 'status': record.status
        } for record in records]

    return {'rounds': rounds, 'count': record_count}



@roundrouter.get('/rounds/{round_id}', tags=['Rounds'])
async def get_round(round_id: UUID):
    round = db.query(Round).filter(Round.id == round_id).options(joinedload(Round.round_holes).joinedload(RoundHole.hole)).first()

    if round:
        round_holes_data = []
        agg_score = 0

        for round_hole in round.round_holes:
            tee_box_hole_id = round_hole.tee_box_hole_id
            hole_number = round_hole.hole.hole_number
            round_holes_data.append({
                'id': round_hole.id,
                'tee_box_hole_id': tee_box_hole_id,
                'hole_number': hole_number,
                'score': round_hole.score,
                'putts': round_hole.putts
            })
            agg_score += round_hole.score

        return {
            'round': {
                'id': round.id,
                'score': round.total_score,
                'round_holes': round_holes_data,
                'hole_count': len(round.round_holes)
            }
        }

    return {'message': 'Round not found'}

@roundrouter.delete('/rounds/{round_id}', tags=['Rounds'], response_model=RoundResponse)
async def delete_round(round_id: UUID):
    record = db.query(Round).filter(Round.id == round_id).first()

    if record is None:
        raise HTTPException(status_code=404, detail='Round not found')

    db.delete(record)
    db.commit()
    db.close()

    return {'message': 'Round deleted successfully'}

@roundrouter.patch('/roundhole/{roundhole_id}', tags=['Rounds'])
async def update_roundhole(roundhole_id: UUID, data: RoundHolePatchRequest):
    try:
        record = db.query(RoundHole).filter(RoundHole.id == roundhole_id).first()

        if not record:
            db.close()
            return {'message': 'Record not found'}

        for field in data.dict(exclude_unset=True):
            setattr(record, field, getattr(data, field))

        db.commit()
        db.refresh(record)
        return record

    finally:
        db.close()


@roundrouter.patch('/rounds/{round_id}', tags=['Rounds'], response_model=RoundResponse)
async def update_round(round_id: UUID, data: RoundPatchRequest):
    try:
        record = db.query(Round).filter(Round.round_id == round_id).first()

        if not record:
            db.close()
            return {'message': 'Record not found'}

        for field in data.dict(exclude_unset=True):
            setattr(record, field, getattr(data, field))

        db.commit()
        db.refresh(record)
        return record

    finally:
        db.close()
