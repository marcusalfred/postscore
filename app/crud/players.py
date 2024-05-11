'''
Player CRUD
'''

from db.models import Player
from db.database import SessionLocal
from sqlalchemy import func
from typing import List
from uuid import UUID
from schemas.pydantic_models import PlayerRequest, PlayerRequestPatch, PlayerResponse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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