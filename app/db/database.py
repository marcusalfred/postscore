'''
DB connection and session maker
'''

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import Depends

# Load variables from .env into the environment
load_dotenv()

db_url = "postgresql://golf_api:t!ger_w00ds@postgres:5432/golf_api"


if db_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
