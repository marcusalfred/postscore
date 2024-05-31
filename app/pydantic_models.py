from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, validator, UUID4, typing
from datetime import date, datetime, time, timedelta


class PlayerRequest(BaseModel):
    name: str
    email: str
    zip: int
    handicap: float
    ghin_number: int

class PlayerCreate(BaseModel):
    username: str
    password: str

class PlayerRequestPatch(BaseModel):
    name: Optional[str]
    email: Optional[str]
    zip: Optional[int]
    handicap: Optional[float]
    ghin_number: Optional[int]

class PlayerResponse(BaseModel):
    id: UUID4
    name: str
    email: str
    zip: int
    handicap: float
    ghin_number: int
    created_at: datetime = Field(exclude=True)  # Exclude created_at field
    updated_at: datetime = Field(exclude=True)  # Exclude updated_at field

class TeeBoxHoleBase(BaseModel):
    number: int
    par: int
    yards: int
    handicap: int

class TeeBoxBase(BaseModel):
    tee_id: UUID4
    tee: str
    rating: float
    slope: int
    holes: List[TeeBoxHoleBase]


class CourseRequest(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip: int
    website: str

class CourseCreate(CourseRequest):
    tees: Optional[List[dict]] = Field(None, description='List of tee details, if available')

class CourseRequestPatch(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[int]
    website: Optional[str]

class CourseRequest(BaseModel):
    name: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    website: Optional[str]

class CourseResponse(BaseModel):
    id: UUID4
    name: str
    location: str
    website: str
    tees: List[TeeBoxBase]

class TeeBoxRequest(BaseModel):
    name: str
    course_id: UUID4
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class TeeBoxCreate(TeeBoxRequest):
    pass

class TeeBoxResponse(BaseModel):
    id: UUID4
    name: str
    course_id: int
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class TeeBoxPatchRequest(BaseModel):
    name: Optional[str]
    course_id: Optional[UUID4]
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class StatusEnum(str, Enum):
    NEW = 'new'
    INPROGRESS = 'in_progress'
    DONE = 'done'

class HolesEnum(int, Enum):
    HALF = 9
    FULL = 18

class RoundRequest(BaseModel):
    course_id: UUID4
    tee_box_id: UUID4
    player_id: UUID4
    total_score: int
    holes: HolesEnum

class RoundPatchRequest(BaseModel):
    course_id: Optional[UUID4]
    tee_box_id: Optional[UUID4]
    player_id: Optional[UUID4]
    total_score: Optional[int]
    holes: HolesEnum = None

class RoundResponse(BaseModel):
    id: UUID4
    course_id: UUID4
    tee_box_id: UUID4
    player_id: UUID4
    total_score: int
    holes: int

class FairwayEnum(str, Enum):
    LEFT = '<'
    ON = 'o'
    RIGHT = '>'
    SHORT = 'v'
    LONG = '^'

class RoundHoleRequest(BaseModel):
    round_id: Optional[UUID4]
    hole_number: Optional[int]
    score: Optional[int]
    gir: Optional[bool]
    fairway: FairwayEnum = None
    putts: Optional[int]
    #penalties: Optional[int]
    #sand: Optional[bool]
    #water: Optional[bool]

class RoundHolePatchRequest(BaseModel):
    score: Optional[int]
    gir: Optional[bool]
    fairway: FairwayEnum = None
    putts: Optional[int]
    penalties: Optional[int]
    sand: Optional[bool]
    water: Optional[bool]

class RoundHoleResponse(BaseModel):
    id: UUID4
    round_id: UUID4
    #hole_number: int
    score: int
    gir: Optional[bool]
    fairway: Optional[str]
    putts: Optional[int]
    #penalties: Optional[int]
    #sand: Optional[bool]
    #water: Optional[bool]

class TeeBoxHoleTest(BaseModel):
    number: int
    yardage: int
    handicap: int
    par: int

class TeeBoxTest(BaseModel):
    name: str
    total_yardage: int
    slope: int
    rating: float
    holes: List[TeeBoxHoleTest]



