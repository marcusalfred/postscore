'''
DB connection and session maker
'''

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import Depends

# Load variables from .env into the environment
load_dotenv('../.env')
db_url = os.getenv('DB_URL')


if db_url is None:
    db_url = os.environ.get('DATABASE_URL')
    #raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
