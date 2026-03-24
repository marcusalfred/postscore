"""
Player repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db.models import Player
from schemas.pydantic_models import PlayerRequest, PlayerRequestPatch, PlayerResponse
from core.security import get_password_hash
from repositories.base import BaseRepository
from core.errors import ResourceNotFoundException, DatabaseException


class PlayerRepository(BaseRepository[Player, PlayerRequest, PlayerRequestPatch]):
    """
    Repository for Player operations.
    """
    
    def __init__(self):
        super().__init__(Player)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Player]:
        """
        Get a player by email (exact match, case-insensitive).
        
        Args:
            db: Database session
            email: Player email to search for
            
        Returns:
            Optional[Player]: The player if found, None otherwise
        """
        return db.execute(select(self.model).where(func.lower(self.model.email) == email.lower())).scalar_one_or_none()
    
    def get_by_name(self, db: Session, name: str) -> List[Player]:
        """
        Get players by name (partial match, case-insensitive).
        
        Args:
            db: Database session
            name: Player name to search for
            
        Returns:
            List[Player]: List of matching players
        """
        return db.execute(select(self.model).where(self.model.name.ilike(f'%{name}%'))).scalars().all()
    
    def get_all(self, db: Session, name: Optional[str] = None) -> List[Player]:
        """
        Get all players, optionally filtered by name.
        
        Args:
            db: Database session
            name: Optional name filter
            
        Returns:
            List[Player]: List of players
        """
        if name:
            return self.get_by_name(db, name)
        return db.execute(select(self.model)).scalars().all()
    
    def create_with_password(self, db: Session, obj_in: PlayerRequest) -> Player:
        """
        Create a new player with a hashed password.
        
        Args:
            db: Database session
            obj_in: Player data
            
        Returns:
            Player: The created player
        """
        # Create a dict of the player data
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        
        # Hash the password if provided
        if obj_in.password:
            obj_in_data["hashed_password"] = get_password_hash(obj_in.password)
            del obj_in_data["password"]
        
        # Create the player
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error creating player: {str(e)}")
    
    def update_password(self, db: Session, db_obj: Player, password: str) -> Player:
        """
        Update a player's password.
        
        Args:
            db: Database session
            db_obj: Player to update
            password: New password
            
        Returns:
            Player: The updated player
        """
        hashed_password = get_password_hash(password)
        db_obj.hashed_password = hashed_password
        db.add(db_obj)
        
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error updating player password: {str(e)}")


# Create a singleton instance
player_repository = PlayerRepository() 