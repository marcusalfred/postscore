from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, Security
from fastapi.security.api_key import APIKeyHeader
#from utils.auth import verify_api_key
from sqlalchemy import func
from models import Player, PlayerRequest, PlayerRequestPatch, PlayerResponse
from db import SessionLocal
from pydantic import BaseModel


api_key_header = APIKeyHeader(name="Authorization")
playerrouter = APIRouter(dependencies=[Depends(verify_api_key)])
#Playerrouter = APIRouter()

@playerrouter.get("/players", tags=["Players"])
async def get_all_players(
    fields: str = Query(None, description="Comma-separated list of fields to display"),
    name: str = None,
    email: str = None):

    db = SessionLocal()
    #query = db.query(Player)

    if name:
        query = db.query(Player).filter(func.lower(Player.name).ilike(f"%{name.lower()}%"))
    if email:
        query = db.query(Player).filter(func.lower(Player.email).ilike(f"%{email.lower()}%"))
    records = db.query(Player).all()
    db.close()

    if fields:
        fields_list = fields.split(",")
        # Filter record fields based on user's specified fields
        records = [{field: getattr(record, field) for field in fields_list} for record in records]
    return {"players": records}

@playerrouter.get("/players/{player_id}", tags=["Players"])
async def get_a_player(player_id: int):
    db = SessionLocal()
    record = db.query(Player).filter(Player.id == player_id).first()
    db.close()
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@playerrouter.post("/players", tags=["Players"], response_model=PlayerResponse)
async def add_player(data: PlayerRequest):
    db = SessionLocal()
    new_record = Player(name=data.name, email=data.email)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    db.close()
    return {"id": new_record.id, "name": new_record.name, "email": new_record.email}

@playerrouter.patch("/players/{player_id}", tags=["Players"], response_model=PlayerResponse)
async def update_player(player_id: int, data: PlayerRequestPatch):
    db = SessionLocal()
    record = db.query(Player).filter(Player.id == player_id).first()

    if not record:
        db.close()
        return {"message": "Record not found"}
    if data.name:
        record.name = data.name
    if data.email:
        record.email = data.email

    db.commit()
    updated_record = db.query(Player).filter(Player.id == player_id).first()
    db.close()
    return {"id": updated_record.id, "name": updated_record.name, "email": updated_record.email}


@playerrouter.delete("/players/{player_id}", tags=["Players"])
async def delete_player(player_id: int):
        db = SessionLocal()
        record = db.query(Player).filter(Player.id == player_id).first()

        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")

        db.delete(record)
        db.commit()
        db.close()

        return {"message": "Record deleted successfully"}






