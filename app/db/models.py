'''
Models
'''

from typing import List, Optional
import datetime
from db.database import SessionLocal
from sqlalchemy import UniqueConstraint, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Player(Base, TimestampMixin):
    __tablename__ = 'players'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    name = Column(String)
    email = Column(String)
    zip = Column(Integer)
    ghin_number = Column(Integer)
    handicap = Column(Float)
    rounds = relationship('Round', back_populates='player', cascade='all, delete')

class Course(Base, TimestampMixin):
    __tablename__ = 'courses'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    name = Column(String(50), unique=True, nullable=False)
    address = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(String(50))
    website = Column(String(50))
    tees = relationship('TeeBox', back_populates='course', cascade='all, delete')
    rounds = relationship('Round', back_populates='course')

class TeeBox(Base, TimestampMixin):
    __tablename__ = 'tee_boxes'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    name = Column(String(50), unique=True, nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    rating = Column(Float)
    slope = Column(Integer)
    yardage = Column(Integer)
    hex = Column(String(50))
    course = relationship('Course', back_populates='tees')
    rounds = relationship('Round', back_populates='tees')
    hole = relationship('TeeBoxHole', back_populates='tees')

class TeeBoxHole(Base, TimestampMixin):
    __tablename__ = 'tee_box_holes'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    tee_box_id = Column(UUID(as_uuid=True), ForeignKey('tee_boxes.id'), nullable=False)
    hole_number = Column(Integer)
    par = Column(Integer)
    yardage = Column(Integer)
    handicap = Column(Integer)
    tees = relationship('TeeBox', back_populates='hole')
    round_holes = relationship('RoundHole', back_populates='hole', cascade='all, delete')


class Round(Base, TimestampMixin):
    __tablename__ = 'rounds'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    course_id = Column(UUID(as_uuid=True), ForeignKey('courses.id'), nullable=False)
    tee_box_id = Column(UUID(as_uuid=True), ForeignKey('tee_boxes.id'), nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey('players.id'), nullable=False)
    total_score = Column(Integer,  nullable=True)
    holes = Column(Integer,  nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    course = relationship('Course', back_populates='rounds')
    tees = relationship('TeeBox', back_populates='rounds')
    player = relationship('Player', back_populates='rounds')
    round_holes = relationship('RoundHole', back_populates='rounds', cascade='all, delete')

class RoundHole(Base, TimestampMixin):
    __tablename__ = 'round_holes'
    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=False, server_default=text('gen_random_uuid()'))
    round_id = Column(UUID(as_uuid=True), ForeignKey('rounds.id'), nullable=False)
    tee_box_hole_id = Column(UUID(as_uuid=True), ForeignKey('tee_box_holes.id'), nullable=False)
    score = Column(Integer)
    gir = Column(Boolean, nullable=True)
    fairway = Column(String, nullable=True)
    putts = Column(Integer, nullable=True)
    penalties = Column(Integer, nullable=True)
    sand = Column(Boolean, nullable=True)
    water = Column(Boolean, nullable=True)
    rounds = relationship('Round', back_populates='round_holes')
    hole = relationship('TeeBoxHole', back_populates='round_holes')

    # Unique constraint on round_id and tee_box_hole_id
    __table_args__ = (
        UniqueConstraint('round_id', 'tee_box_hole_id', name='unique_round_hole_per_round'),
    )



