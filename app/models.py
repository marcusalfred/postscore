from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .database import SessionLocal
from datetime import datetime
from pydantic import BaseModel, Field, validator
import datetime
from typing import List, Optional

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    zip = Column(Integer)
    ghin_number = Column(Integer)
    handicap = Column(Integer)
    pid = Column(UUID(as_uuid=True))
    rounds = relationship("Round", back_populates="player", cascade="all, delete")

class PlayerRequest(BaseModel):
    name: str
    email: str

class PlayerRequestPatch(BaseModel):
    name: str = None
    email: str = None

class PlayerResponse(BaseModel):
    id: int
    name: str
    email: str

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    website = Column(String(50))
    par = Column(Integer)
    hole1_par = Column(Integer)
    hole2_par = Column(Integer)
    hole3_par = Column(Integer)
    hole4_par = Column(Integer)
    hole5_par = Column(Integer)
    hole6_par = Column(Integer)
    hole7_par = Column(Integer)
    hole8_par = Column(Integer)
    hole9_par = Column(Integer)
    hole10_par = Column(Integer)
    hole11_par = Column(Integer)
    hole12_par = Column(Integer)
    hole13_par = Column(Integer)
    hole14_par = Column(Integer)
    hole15_par = Column(Integer)
    hole16_par = Column(Integer)
    hole17_par = Column(Integer)
    hole18_par = Column(Integer)
    hole1_handicap = Column(Integer)
    hole2_handicap = Column(Integer)
    hole3_handicap = Column(Integer)
    hole4_handicap = Column(Integer)
    hole5_handicap = Column(Integer)
    hole6_handicap = Column(Integer)
    hole7_handicap = Column(Integer)
    hole8_handicap = Column(Integer)
    hole9_handicap = Column(Integer)
    hole10_handicap = Column(Integer)
    hole11_handicap = Column(Integer)
    hole12_handicap = Column(Integer)
    hole13_handicap = Column(Integer)
    hole14_handicap = Column(Integer)
    hole15_handicap = Column(Integer)
    hole16_handicap = Column(Integer)
    hole17_handicap = Column(Integer)
    hole18_handicap = Column(Integer)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    tees = relationship("TeeBox", back_populates="course", cascade="all, delete")
    rounds = relationship("Round", back_populates="course")


class CourseRequest(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip: int
    website: str
    par: int
    hole1_par: int
    hole2_par: int
    hole3_par: int
    hole4_par: int
    hole5_par: int
    hole6_par: int
    hole7_par: int
    hole8_par: int
    hole9_par: int
    hole10_par: int
    hole11_par: int
    hole12_par: int
    hole13_par: int
    hole14_par: int
    hole15_par: int
    hole16_par: int
    hole17_par: int
    hole18_par: int
    hole1_handicap: int
    hole2_handicap: int
    hole3_handicap: int
    hole4_handicap: int
    hole5_handicap: int
    hole6_handicap: int
    hole7_handicap: int
    hole8_handicap: int
    hole9_handicap: int
    hole10_handicap: int
    hole11_handicap: int
    hole12_handicap: int
    hole13_handicap: int
    hole14_handicap: int
    hole15_handicap: int
    hole16_handicap: int
    hole17_handicap: int
    hole18_handicap: int

class CourseCreate(CourseRequest):
    tees: Optional[List[dict]] = Field(None, description="List of tee details, if available")

class CourseRequestPatch(BaseModel):
    name: str = None
    address: str = None
    city: str = None
    state: str = None
    zip: int = None
    website: str = None
    par: int = None
    hole1_par: int = None
    hole2_par: int = None
    hole3_par: int = None
    hole4_par: int = None
    hole5_par: int = None
    hole6_par: int = None
    hole7_par: int = None
    hole8_par: int = None
    hole9_par: int = None
    hole10_par: int = None
    hole11_par: int = None
    hole12_par: int = None
    hole13_par: int = None
    hole14_par: int = None
    hole15_par: int = None
    hole16_par: int = None
    hole17_par: int = None
    hole18_par: int = None
    hole1_handicap: int = None
    hole2_handicap: int = None
    hole3_handicap: int = None
    hole4_handicap: int = None
    hole5_handicap: int = None
    hole6_handicap: int = None
    hole7_handicap: int = None
    hole8_handicap: int = None
    hole9_handicap: int = None
    hole10_handicap: int = None
    hole11_handicap: int = None
    hole12_handicap: int = None
    hole13_handicap: int = None
    hole14_handicap: int = None
    hole15_handicap: int = None
    hole16_handicap: int = None
    hole17_handicap: int = None
    hole18_handicap: int = None

class CourseResponse(BaseModel):
    id: int
    name: str = None
    address: str = None
    city: str = None
    state: str = None
    zip: int = None
    website: str = None
    par: int = None
    hole1_par: int = None
    hole2_par: int = None
    hole3_par: int = None
    hole4_par: int = None
    hole5_par: int = None
    hole6_par: int = None
    hole7_par: int = None
    hole8_par: int = None
    hole9_par: int = None
    hole10_par: int = None
    hole11_par: int = None
    hole12_par: int = None
    hole13_par: int = None
    hole14_par: int = None
    hole15_par: int = None
    hole16_par: int = None
    hole17_par: int = None
    hole18_par: int = None
    hole1_handicap: int = None
    hole2_handicap: int = None
    hole3_handicap: int = None
    hole4_handicap: int = None
    hole5_handicap: int = None
    hole6_handicap: int = None
    hole7_handicap: int = None
    hole8_handicap: int = None
    hole9_handicap: int = None
    hole10_handicap: int = None
    hole11_handicap: int = None
    hole12_handicap: int = None
    hole13_handicap: int = None
    hole14_handicap: int = None
    hole15_handicap: int = None
    hole16_handicap: int = None
    hole17_handicap: int = None
    hole18_handicap: int = None

class TeeBox(Base):
    __tablename__ = 'tee_boxes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    rating = Column(Float)
    slope = Column(Integer)
    yardage = Column(Integer)
    hex = Column(String(50))
    hole1_yards = Column(Integer)
    hole2_yards = Column(Integer)
    hole3_yards = Column(Integer)
    hole4_yards = Column(Integer)
    hole5_yards = Column(Integer)
    hole6_yards = Column(Integer)
    hole7_yards = Column(Integer)
    hole8_yards = Column(Integer)
    hole9_yards = Column(Integer)
    hole10_yards = Column(Integer)
    hole11_yards = Column(Integer)
    hole12_yards = Column(Integer)
    hole13_yards = Column(Integer)
    hole14_yards = Column(Integer)
    hole15_yards = Column(Integer)
    hole16_yards = Column(Integer)
    hole17_yards = Column(Integer)
    hole18_yards = Column(Integer)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    course = relationship("Course", back_populates="tees")
    rounds = relationship("Round", back_populates="tees")

class TeeBoxRequest(BaseModel):
    name: str
    course_id: int
    rating: float = None
    slope: int = None
    yardage: int = None
    hex: str = None
    hole1_yards: int = None
    hole2_yards: int = None
    hole3_yards: int = None
    hole4_yards: int = None
    hole5_yards: int = None
    hole6_yards: int = None
    hole7_yards: int = None
    hole8_yards: int = None
    hole9_yards: int = None
    hole10_yards: int = None
    hole11_yards: int = None
    hole12_yards: int = None
    hole13_yards: int = None
    hole14_yards: int = None
    hole15_yards: int = None
    hole16_yards: int = None
    hole17_yards: int = None
    hole18_yards: int = None

class TeeBoxCreate(TeeBoxRequest):
    pass

class TeeBoxResponse(BaseModel):
    id: int
    name: str
    course_id: int
    rating: float = None
    slope: int = None
    yardage: int = None
    hex: str = None
    hole1_yards: int = None
    hole2_yards: int = None
    hole3_yards: int = None
    hole4_yards: int = None
    hole5_yards: int = None
    hole6_yards: int = None
    hole7_yards: int = None
    hole8_yards: int = None
    hole9_yards: int = None
    hole10_yards: int = None
    hole11_yards: int = None
    hole12_yards: int = None
    hole13_yards: int = None
    hole14_yards: int = None
    hole15_yards: int = None
    hole16_yards: int = None
    hole17_yards: int = None
    hole18_yards: int = None


class Round(Base):
    __tablename__ = 'rounds'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    tee_box_id = Column(Integer, ForeignKey("tee_boxes.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    total_score = Column(Integer,  nullable=True)
    holes = Column(Integer,  nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    course = relationship("Course", back_populates="rounds")
    tees = relationship("TeeBox", back_populates="rounds")
    player = relationship("Player", back_populates="rounds")
    round_holes = relationship("RoundHole", back_populates="rounds", cascade="all, delete")

class RoundRequest(BaseModel):
    course_id: int
    tee_box_id: int
    player_id: int
    total_score: int
    holes: int

class RoundResponse(BaseModel):
    id: int
    course_id: int
    tee_box_id: int
    player_id: int
    total_score: int
    holes: int


class RoundHole(Base):
    __tablename__ = 'round_holes'
    id = Column(Integer, primary_key=True)
    round_id = Column(Integer, ForeignKey("rounds.id"), nullable=False)
    score = Column(Integer)
    hole_number = Column(Integer)
    gir = Column(Boolean, nullable=True)
    fairway = Column(String, nullable=True)
    putts = Column(Integer, nullable=True)
    penalties = Column(Integer, nullable=True)
    sand = Column(Boolean, nullable=True)
    water = Column(Boolean, nullable=True)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    rounds = relationship("Round", back_populates="round_holes")

def check_unique_name(session, round_id, hole_number):
    item = (
        session.query(RoundHole)
        .filter(RoundHole.round_id == round_id, RoundHole.hole_number == hole_number)
        .first()
        )
    return item


class RoundHoleRequest(BaseModel):
    round_id: int = None
    hole_number: int = None
    score: int = None
    gir: bool = None
    fairway: str = None
    putts: int = None
    penalties: int = None
    sand: bool = None
    water: bool = None

    @validator("hole_number")
    def validate_unique_number(cls, value, values, **kwargs):
        round_id = values.get("round_id")
        if round_id and value:
            session = SessionLocal()
            item = check_unique_name(session, round_id, value)
            session.close()
            if item:
                    raise ValueError("hole_number must be unique within the round")
        return value

class RoundHolePatchRequest(BaseModel):
    score: int = None
    gir: bool = None
    fairway: str = None
    putts: int = None
    penalties: int = None
    sand: bool = None
    water: bool = None

class RoundHoleResponse(BaseModel):
    id: int
    round_id: int
    hole_number: int
    score: int
    gir: bool = None
    fairway: str = None
    putts: int = None
    penalties: int = None
    sand: bool = None
    water: bool = None
