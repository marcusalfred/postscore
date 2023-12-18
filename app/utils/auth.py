from typing import List
from fastapi import FastAPI, HTTPException, Header, Depends
from db import SessionLocal
from pydantic import BaseModel
from models import Player
from uuid import UUID

# Define a function to verify the API key
async def verify_api_key(key: UUID = Header(None)):
    db = SessionLocal()
    try:
        print(f"Received PID: {key}")
        player = db.query(Player).filter(Player.pid == key).first()
        print(f"SQL Query: {db.query(Player).filter(Player.pid == key)}")
        if not player:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return player
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()