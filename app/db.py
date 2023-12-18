'''
DB connection and session maker
'''

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

db_url = os.environ.get('DB_URL')

engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
