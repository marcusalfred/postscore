'''
Player endpoints
'''

from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from db.models import Player
from schemas.pydantic_models import PlayerRequest, PlayerRequestPatch
from db.database import SessionLocal, get_db
from uuid import UUID
from crud.players import get_players, get_player_by_id, create_player, update_player, delete_player

playerrouter = APIRouter()

@playerrouter.get('/players', tags=['Players'])
async def get_all_players(name: str = None, db: SessionLocal = Depends(get_db)):
    player_recs = get_players(db, name)
    return {'players': player_recs}

@playerrouter.get('/players/{player_id}', tags=['Players'])
async def get_a_player(player_id: UUID, db: SessionLocal = Depends(get_db)):
    player_rec = get_player_by_id(db, player_id)
    if player_rec is None:
        raise HTTPException(status_code=404, detail='player_rec not found')
    return player_rec

@playerrouter.post('/players', tags=['Players'])
async def add_player(data: PlayerRequest, db: SessionLocal = Depends(get_db)):
    new_player = create_player(db, data)
    print(f"New player created: {new_player}")
    return new_player

@playerrouter.patch('/players/{player_id}', tags=['Players'])
async def mod_player(player_id: UUID, data: PlayerRequestPatch, db: SessionLocal = Depends(get_db)):
    player_rec = update_player(db, player_id, data)
    if player_rec is None:
        raise HTTPException(status_code=404, detail='player_rec not found')
    return player_rec

@playerrouter.delete('/players/{player_id}', tags=['Players'])
async def del_player(player_id: UUID, db: SessionLocal = Depends(get_db)):
    player_rec = delete_player(db, player_id)
    if player_rec is None:
        raise HTTPException(status_code=404, detail='player_rec not found')
    return {'message': f"{player_id} deleted successfully"}
