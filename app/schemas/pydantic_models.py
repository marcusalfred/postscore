from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import date, datetime, time, timedelta
import ulid


class PlayerRequest(BaseModel):
    """Request model for creating or updating a player."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "John Doe",
            "email": "john@example.com",
            "zip": "12345",
            "handicap": 15.2,
            "ghin_number": "1234567"
        }
    })

    name: str = Field(..., min_length=2, max_length=100, description="Player's full name")
    email: EmailStr = Field(..., description="Email address (must be unique)")
    zip: str = Field(..., min_length=5, max_length=10, description="ZIP/Postal code")
    handicap: Optional[float] = Field(None, ge=0.0, le=54.0, description="Golf handicap (0-54)")
    ghin_number: Optional[str] = Field(None, description="GHIN number")
    password: Optional[str] = Field(None, min_length=8, description="Password (min 8 characters)")


class PlayerRequestPatch(BaseModel):
    """Request model for partially updating a player."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "handicap": 14.5,
            "zip": "90210"
        }
    })

    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Player's full name")
    email: Optional[EmailStr] = Field(None, description="Email address (must be unique)")
    zip: Optional[str] = Field(None, min_length=5, max_length=10, description="ZIP/Postal code")
    handicap: Optional[float] = Field(None, ge=0.0, le=54.0, description="Golf handicap (0-54)")
    ghin_number: Optional[str] = Field(None, description="GHIN number")


class PlayerResponse(BaseModel):
    """Response model for player data."""
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "01H0JMVKHWBH8QRE098XVGC9X4",
            "name": "John Doe",
            "email": "john@example.com",
            "zip": "12345",
            "handicap": 15.2,
            "ghin_number": "1234567",
            "is_active": True,
            "created_on": "2023-10-20T12:34:56.789Z"
        }
    })

    id: str = Field(..., description="Player ID (ULID)")
    name: str = Field(..., description="Player's full name")
    email: Optional[str] = Field(None, description="Email address")
    zip: Optional[str] = Field(None, description="ZIP/Postal code")
    handicap: Optional[float] = Field(None, description="Golf handicap")
    ghin_number: Optional[str] = Field(None, description="GHIN number")
    is_active: Optional[bool] = Field(default=True, description="Whether the player account is active")
    created_on: Optional[datetime] = Field(None, description="When the player was created")


class SignupResponse(BaseModel):
    """Response model for successful signup"""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "player": {
                "id": "01H0JMVKHWBH8QRE098XVGC9X4",
                "name": "John Doe",
                "email": "john@example.com",
                "zip": "12345",
                "handicap": 15.2,
                "ghin_number": "1234567",
                "is_active": True
            },
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    })

    player: PlayerResponse
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")

class TeeBoxHoleBase(BaseModel):
    number: int
    par: int
    yards: int
    handicap: int

class TeeBoxHoleResponse(TeeBoxHoleBase):
    """Response model for tee box hole data with ID."""
    model_config = ConfigDict(from_attributes=True)

    id: str

class TeeBoxBase(BaseModel):
    tee_id: str
    tee: str
    rating: Optional[float] = None
    slope: Optional[int] = None
    holes: List[TeeBoxHoleBase]


class CourseRequest(BaseModel):
    """Request model for creating a new course."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Augusta National Golf Club",
            "address": "2604 Washington Rd",
            "city": "Augusta",
            "state": "GA",
            "zip": "30904",
            "website": "https://www.augusta.com"
        }
    })

    name: str = Field(..., min_length=2, max_length=100, description="Name of the golf course")
    address: str = Field(..., min_length=5, max_length=100, description="Street address of the course")
    city: str = Field(..., min_length=2, max_length=50, description="City where the course is located")
    state: str = Field(..., min_length=2, max_length=2, description="Two-letter state code")
    zip: str = Field(..., min_length=5, max_length=10, description="ZIP/Postal code")
    website: str = Field(..., min_length=5, max_length=100, description="Course website URL")

class CourseRequestPatch(BaseModel):
    """Request model for updating an existing course."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Augusta National Golf Club",
            "website": "https://www.augusta.com"
        }
    })

    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Name of the golf course")
    address: Optional[str] = Field(None, min_length=5, max_length=100, description="Street address of the course")
    city: Optional[str] = Field(None, min_length=2, max_length=50, description="City where the course is located")
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="Two-letter state code")
    zip: Optional[str] = Field(None, min_length=5, max_length=10, description="ZIP/Postal code")
    website: Optional[str] = Field(None, min_length=5, max_length=100, description="Course website URL")

class CourseResponse(BaseModel):
    """Response model for course data."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    website: Optional[str] = None
    tees: List[TeeBoxBase] = []

    @property
    def location(self) -> str:
        """Returns a formatted location string."""
        return f"{self.city}, {self.state}"

class TeeBoxRequest(BaseModel):
    name: str
    course_id: str
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class TeeBoxCreate(TeeBoxRequest):
    pass

class TeeBoxResponse(BaseModel):
    id: str
    name: str
    course_id: str
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class TeeBoxPatchRequest(BaseModel):
    name: Optional[str]
    course_id: Optional[str]
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]

class StatusEnum(str, Enum):
    """Status of a round."""
    NEW = 'new'
    INPROGRESS = 'in_progress'
    DONE = 'done'

class HolesEnum(int, Enum):
    """Number of holes in a round."""
    HALF = 9
    FULL = 18

class RoundRequest(BaseModel):
    """Request model for creating a new round."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "course_id": "01H0JMVKHWBH8QRE098XVGC9X4",
            "tee_box_id": "01H0JMVKHWBH8QRE098XVGC9X5",
            "player_id": "01H0JMVKHWBH8QRE098XVGC9X6",
            "holes": 18,
            "start_time": "2023-10-20T08:30:00Z"
        }
    })

    course_id: str = Field(..., description="ID of the course")
    tee_box_id: str = Field(..., description="ID of the tee box")
    player_id: Optional[str] = Field(None, description="ID of the player")
    total_score: Optional[int] = Field(None, ge=18, description="Total score for the round")
    holes: HolesEnum = Field(..., description="Number of holes (9 or 18)")
    start_time: Optional[datetime] = Field(None, description="When the round started")

class RoundPatchRequest(BaseModel):
    """Request model for updating an existing round."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "total_score": 72,
            "end_time": "2023-10-20T12:30:00Z"
        }
    })

    course_id: Optional[str] = Field(None, description="ID of the course")
    tee_box_id: Optional[str] = Field(None, description="ID of the tee box")
    player_id: Optional[str] = Field(None, description="ID of the player")
    total_score: Optional[int] = Field(None, ge=18, description="Total score for the round")
    holes: Optional[HolesEnum] = Field(None, description="Number of holes (9 or 18)")
    start_time: Optional[datetime] = Field(None, description="When the round started")
    end_time: Optional[datetime] = Field(None, description="When the round ended")

class RoundResponse(BaseModel):
    """Response model for round data."""
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "01H0JMVKHWBH8QRE098XVGC9X7",
            "course_id": "01H0JMVKHWBH8QRE098XVGC9X4",
            "tee_box_id": "01H0JMVKHWBH8QRE098XVGC9X5",
            "player_id": "01H0JMVKHWBH8QRE098XVGC9X6",
            "total_score": 72,
            "holes": 18,
            "start_time": "2023-10-20T08:30:00Z",
            "end_time": "2023-10-20T12:30:00Z",
            "created_on": "2023-10-20T08:15:30Z"
        }
    })

    id: str = Field(..., description="Round ID (ULID)")
    course_id: str = Field(..., description="ID of the course")
    tee_box_id: str = Field(..., description="ID of the tee box")
    player_id: str = Field(..., description="ID of the player")
    total_score: Optional[int] = Field(None, description="Total score for the round")
    holes: int = Field(..., description="Number of holes (9 or 18)")
    start_time: Optional[datetime] = Field(None, description="When the round started")
    end_time: Optional[datetime] = Field(None, description="When the round ended")
    created_on: Optional[datetime] = Field(None, description="When the round was created")

class RoundHoleSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    tee_box_hole_id: str
    hole_number: Optional[int]
    score: Optional[int]
    gir: Optional[bool]
    fairway: Optional[str]
    putts: Optional[int]

class RoundWithHolesResponse(RoundResponse):
    round_holes: List[RoundHoleSummary] = []

class FairwayEnum(str, Enum):
    """Fairway hit status."""
    LEFT = '<'
    ON = 'o'
    RIGHT = '>'
    SHORT = 'v'
    LONG = '^'

class RoundHoleRequest(BaseModel):
    """Request model for creating a round hole."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "round_id": "01H0JMVKHWBH8QRE098XVGC9X7",
            "tee_box_hole_id": "01H0JMVKHWBH8QRE098XVGC9X8",
            "score": 4,
            "gir": True,
            "fairway": "o",
            "putts": 2
        }
    })

    round_id: str = Field(..., description="ID of the round")
    tee_box_hole_id: str = Field(..., description="ID of the tee box hole")
    score: int = Field(..., ge=1, description="Score for the hole")
    gir: Optional[bool] = Field(None, description="Green in regulation")
    fairway: Optional[FairwayEnum] = Field(None, description="Fairway hit status")
    putts: Optional[int] = Field(None, ge=0, description="Number of putts")
    penalties: Optional[int] = Field(None, ge=0, description="Number of penalty strokes")
    sand: Optional[bool] = Field(None, description="Hit from sand")
    water: Optional[bool] = Field(None, description="Hit from water")

class RoundHolePatchRequest(BaseModel):
    """Request model for updating a round hole."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "score": 5,
            "putts": 3
        }
    })

    score: Optional[int] = Field(None, ge=1, description="Score for the hole")
    gir: Optional[bool] = Field(None, description="Green in regulation")
    fairway: Optional[FairwayEnum] = Field(None, description="Fairway hit status")
    putts: Optional[int] = Field(None, ge=0, description="Number of putts")
    penalties: Optional[int] = Field(None, ge=0, description="Number of penalty strokes")
    sand: Optional[bool] = Field(None, description="Hit from sand")
    water: Optional[bool] = Field(None, description="Hit from water")

class RoundHoleResponse(BaseModel):
    """Response model for round hole data."""
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "01H0JMVKHWBH8QRE098XVGC9X9",
            "round_id": "01H0JMVKHWBH8QRE098XVGC9X7",
            "tee_box_hole_id": "01H0JMVKHWBH8QRE098XVGC9X8",
            "score": 4,
            "gir": True,
            "fairway": "o",
            "putts": 2,
            "penalties": 0,
            "sand": False,
            "water": False,
            "created_on": "2023-10-20T08:35:15Z"
        }
    })

    id: str = Field(..., description="Round hole ID (ULID)")
    round_id: str = Field(..., description="ID of the round")
    tee_box_hole_id: str = Field(..., description="ID of the tee box hole")
    score: int = Field(..., description="Score for the hole")
    gir: Optional[bool] = Field(None, description="Green in regulation")
    fairway: Optional[str] = Field(None, description="Fairway hit status")
    putts: Optional[int] = Field(None, description="Number of putts")
    penalties: Optional[int] = Field(None, description="Number of penalty strokes")
    sand: Optional[bool] = Field(None, description="Hit from sand")
    water: Optional[bool] = Field(None, description="Hit from water")
    created_on: Optional[datetime] = Field(None, description="When the round hole was created")

class RoundHoleDetailResponse(RoundHoleResponse):
    """Detailed response model for round hole data with context."""
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "01H0JMVKHWBH8QRE098XVGC9X9",
            "round_id": "01H0JMVKHWBH8QRE098XVGC9X7",
            "tee_box_hole_id": "01H0JMVKHWBH8QRE098XVGC9X8",
            "score": 4,
            "gir": True,
            "fairway": "o",
            "putts": 2,
            "penalties": 0,
            "sand": False,
            "water": False,
            "created_on": "2023-10-20T08:35:15Z",
            "hole_number": 12,
            "par": 3,
            "yards": 155,
            "handicap": 18,
            "course_id": "01H0JMVKHWBH8QRE098XVGC9X4",
            "player_id": "01H0JMVKHWBH8QRE098XVGC9X6"
        }
    })

    hole_number: Optional[int] = Field(None, description="Hole number (1-18)")
    par: Optional[int] = Field(None, description="Par for the hole")
    yards: Optional[int] = Field(None, description="Hole yardage")
    handicap: Optional[int] = Field(None, description="Hole handicap (1-18)")
    course_id: Optional[str] = Field(None, description="Course ID for the round")
    player_id: Optional[str] = Field(None, description="Player ID for the round")

# Authentication models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None

class RoundStatsResponse(BaseModel):
    """Response model for round statistics."""
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "total_score": 72,
            "par": 72,
            "to_par": 0,
            "greens_in_regulation": 12,
            "gir_percentage": 66.7,
            "fairways_hit": 10,
            "fairways_percentage": 71.4,
            "avg_putts_per_hole": 1.8,
            "total_putts": 32,
            "penalties": 2,
            "sand_shots": 1,
            "water_shots": 0
        }
    })

    total_score: Optional[int] = None
    par: Optional[int] = None
    to_par: Optional[int] = None
    greens_in_regulation: Optional[int] = None
    gir_percentage: Optional[float] = None
    fairways_hit: Optional[int] = None
    fairways_percentage: Optional[float] = None
    avg_putts_per_hole: Optional[float] = None
    total_putts: Optional[int] = None
    penalties: Optional[int] = None
    sand_shots: Optional[int] = None
    water_shots: Optional[int] = None

class TeeBoxDetailResponse(BaseModel):
    """Response model for detailed tee box data with hole IDs."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    course_id: str
    rating: Optional[float]
    slope: Optional[int]
    yardage: Optional[int]
    hex: Optional[str]
    holes: List[TeeBoxHoleResponse]


class TeeBoxHoleDetailResponse(BaseModel):
    """Response model for detailed tee box hole data."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    tee_box_id: str
    number: int
    par: int
    yards: int
    handicap: int
    tee_box_name: Optional[str]
    course_id: Optional[str]



