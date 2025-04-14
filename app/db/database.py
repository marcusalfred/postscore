'''
DB connection and session maker
'''

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from fastapi import Depends

# Load variables from .env into the environment
load_dotenv()

# Create the Base class for declarative SQLAlchemy models
Base = declarative_base()

# Get database connection details from environment
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "postscore")

# Construct the database URL
if db_password:
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
else:
    db_url = f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"

if db_url is None:
    raise ValueError("Database connection parameters are not properly set")

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
