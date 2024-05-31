from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, Security
from fastapi.security.api_key import APIKeyHeader
#from utils.auth import verify_api_key
from sqlalchemy import func
from ..models import Round, RoundHole, RoundRequest, RoundResponse, RoundHoleRequest, RoundHoleResponse, RoundHolePatchRequest
from ..database import SessionLocal
from pydantic import BaseModel
import datetime

api_key_header = APIKeyHeader(name="Authorization")
roundrouter = APIRouter(dependencies=[Depends(verify_api_key)])
#roundrouter = APIRouter()

@roundrouter.post("/rounds", tags=["Rounds"], response_model=RoundResponse)
async def add_round(data: RoundRequest):
    db = SessionLocal()
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
        "id": new_record.id,
        "course_id": new_record.course_id,
        "tee_box_id": new_record.tee_box_id,
        "player_id": new_record.player_id,
        "total_score": new_record.total_score,
        "holes": new_record.holes
        }

@roundrouter.post("/rounds/{round_id}/{hole_number}", tags=["Rounds"], response_model=RoundHoleResponse)
async def add_roundhole(round_id: int, hole_number: int, data: RoundHoleRequest):
    db = SessionLocal()
    new_record = RoundHole(
        round_id=data.round_id,
        score=data.score,
        hole_number=data.hole_number,
        gir=data.gir,
        fairway=data.fairway,
        putts=data.putts,
        penalties=data.penalties,
        sand=data.sand,
        water=data.water)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()
    return {
        "id": new_record.id,
        "round_id": new_record.round_id,
        "score": new_record.score,
        "hole_number": new_record.hole_number,
        "gir": new_record.gir,
        "fairway": new_record.fairway,
        "putts": new_record.putts,
        "penalties": new_record.penalties,
        "sand": new_record.sand,
        "water": new_record.water}

@roundrouter.get('/rounds', tags=["Rounds"])
async def get_all_rounds(player_id: int = None):
    db = SessionLocal()

    query = db.query(Round)
    if player_id:
        query = query.filter(Round.player_id == player_id)
    records = query.all()
    record_count = len(records)
    db.close()

    rounds =  [{
            "id": record.id,
            "course_id": record.course_id,
            "player_id": record.player_id,
            "tee_box_id": record.tee_box_id,
            "total_score": record.total_score,
            "holes": record.holes,
            "start": record.start_time,
            "end": record.end_time#,
           # "status": record.status
        } for record in records]

    return {"rounds": rounds, "count": record_count}

@roundrouter.get('/rounds/{round_id}', tags=["Rounds"])
async def get_round(round_id: int):
    db = SessionLocal()
    # Fetch the course along with its tees
    round = db.query(Round).filter(Round.id == round_id).first()

    if round:
        # Access associated tees through the relationship defined in the Course model
        round_holes = [{"hole": round_hole.hole_number, "score": round_hole.score, "putts": round_hole.putts} for round_hole in round.round_holes]

        db.close()

        score2 = sum(obj["score"] for obj in round_holes)

        return {"round": {"id": round.id, "score": round.total_score, "hole_count": len(round_holes), "round_holes": round_holes, "score2": score2}}

    db.close()
    return {"message": "Round not found"}


@roundrouter.delete("/rounds/{round_id}", tags=["Rounds"])
async def delete_round(round_id: int):
        db = SessionLocal()
        record = db.query(Round).filter(Round.id == round_id).first()

        if record is None:
            raise HTTPException(status_code=404, detail="Round not found")

        db.delete(record)
        db.commit()
        db.close()

        return {"message": "Round deleted successfully"}



@roundrouter.get('/rounds/{round_id}/{hole_number}', tags=["Rounds"])
async def get_roundhole(round_id: int, hole_number: int):
    db = SessionLocal()
    roundhole = db.query(RoundHole).filter(RoundHole.round_id == round_id, RoundHole.hole_number == hole_number).first()
    db.close()
    if roundhole is None:
            raise HTTPException(status_code=404, detail="RoundHole not found")
    return roundhole


@roundrouter.patch('/rounds/{round_id}/{hole_number}', tags=["Rounds"])
async def update_roundhole(round_id: int, hole_number: int, data: RoundHolePatchRequest):
    db = SessionLocal()
    try:
        record = db.query(RoundHole).filter(RoundHole.round_id == round_id, RoundHole.hole_number == hole_number).first()

        if not record:
            db.close()
            return {"message": "Record not found"}

        for field in data.dict(exclude_unset=True):
            setattr(record, field, getattr(data, field))

        db.commit()
        db.refresh(record)
        return record

    finally:
        db.close()

