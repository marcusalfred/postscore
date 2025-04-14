"""
API endpoints for administrative operations.
These endpoints are only accessible to superusers.
"""
from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.security import get_current_superuser
from db.database import get_db
from db.models import Player
from core.errors import DatabaseException

router = APIRouter()

@router.post(
    "/run-migration",
    status_code=status.HTTP_200_OK,
    summary="Run database migrations",
    description="Execute SQL migrations to update the database schema. Only accessible to superusers.",
    tags=["Administration"]
)
async def run_migration(
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_superuser)
) -> Any:
    """
    Run database migrations.
    
    Args:
        db: Database session
        current_user: Authenticated superuser
        
    Returns:
        Dict: Status message
        
    Raises:
        DatabaseException: If there's an error running the migration
    """
    try:
        # Example migration to add timestamp columns
        sql = """
        DO $$
        BEGIN
            -- Add created_on column to tables that don't have it
            IF NOT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'players' AND column_name = 'created_on'
            ) THEN
                ALTER TABLE players ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
            
            IF NOT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'courses' AND column_name = 'created_on'
            ) THEN
                ALTER TABLE courses ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
            
            IF NOT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'tee_boxes' AND column_name = 'created_on'
            ) THEN
                ALTER TABLE tee_boxes ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
            
            IF NOT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'tee_box_holes' AND column_name = 'created_on'
            ) THEN
                ALTER TABLE tee_box_holes ADD COLUMN created_on TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW();
            END IF;
        END $$;
        """
        
        # Execute the SQL directly
        db.execute(sql)
        db.commit()
        
        return {"status": "success", "message": "Migration completed successfully"}
    except Exception as e:
        db.rollback()
        raise DatabaseException(f"Error running migration: {str(e)}")


@router.get(
    "/system-info",
    status_code=status.HTTP_200_OK,
    summary="Get system information",
    description="Get information about the system, including database stats. Only accessible to superusers.",
    tags=["Administration"]
)
async def get_system_info(
    db: Session = Depends(get_db),
    current_user: Player = Depends(get_current_superuser)
) -> Any:
    """
    Get system information.
    
    Args:
        db: Database session
        current_user: Authenticated superuser
        
    Returns:
        Dict: System information
        
    Raises:
        DatabaseException: If there's an error retrieving system information
    """
    try:
        # Count records in main tables
        player_count = db.query(Player).count()
        
        # Get other counts
        course_count_result = db.execute("SELECT COUNT(*) FROM courses").scalar()
        round_count_result = db.execute("SELECT COUNT(*) FROM rounds").scalar()
        
        return {
            "status": "success",
            "data": {
                "database": {
                    "player_count": player_count,
                    "course_count": course_count_result,
                    "round_count": round_count_result
                },
                "api_version": "0.2.0"
            }
        }
    except Exception as e:
        raise DatabaseException(f"Error retrieving system information: {str(e)}") 