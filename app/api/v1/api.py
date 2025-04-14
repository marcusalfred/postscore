"""
API router for the v1 API.
"""
from fastapi import APIRouter, Depends
from core.security import get_current_superuser
from core.config import settings

from api.v1.endpoints import courses, players, rounds, auth, admin

# Create API router
api_router = APIRouter()

# Include routes for different resource types
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(rounds.router, prefix="/rounds", tags=["Rounds"])

# Add admin router with superuser dependency in production
if settings.ENVIRONMENT == "production":
    api_router.include_router(
        admin.router, 
        prefix="/admin", 
        tags=["Administration"],
        dependencies=[Depends(get_current_superuser)]
    )
else:
    # In development, allow admin access without authentication
    api_router.include_router(
        admin.router, 
        prefix="/admin", 
        tags=["Administration"]
    ) 