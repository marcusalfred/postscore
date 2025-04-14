"""
Round repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import Round, RoundHole, TeeBoxHole
from schemas.pydantic_models import RoundRequest, RoundPatchRequest, RoundResponse
from repositories.base import BaseRepository
from core.errors import ResourceNotFoundException, DatabaseException, ValidationException


class RoundRepository(BaseRepository[Round, RoundRequest, RoundPatchRequest]):
    """
    Repository for Round operations.
    """
    
    def __init__(self):
        super().__init__(Round)
    
    def get_by_player(self, db: Session, player_id: str) -> List[Round]:
        """
        Get all rounds for a player.
        
        Args:
            db: Database session
            player_id: Player ID
            
        Returns:
            List[Round]: List of rounds for the player
        """
        return db.query(self.model).filter(self.model.player_id == player_id).all()
    
    def get_by_course(self, db: Session, course_id: str) -> List[Round]:
        """
        Get all rounds for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List[Round]: List of rounds for the course
        """
        return db.query(self.model).filter(self.model.course_id == course_id).all()
    
    def get_round_with_holes(self, db: Session, round_id: str) -> Dict[str, Any]:
        """
        Get a round with all its holes.
        
        Args:
            db: Database session
            round_id: Round ID
            
        Returns:
            Dict[str, Any]: Round data with holes
            
        Raises:
            ResourceNotFoundException: If the round is not found
        """
        round_obj = self.get(db, round_id)
        
        if round_obj is None:
            raise ResourceNotFoundException("Round", round_id)
        
        # Get round holes
        round_holes = db.query(RoundHole).filter(RoundHole.round_id == round_id).all()
        
        # Create response data
        return {
            "id": round_obj.id,
            "course_id": round_obj.course_id,
            "tee_box_id": round_obj.tee_box_id,
            "player_id": round_obj.player_id,
            "total_score": round_obj.total_score,
            "holes": round_obj.holes,
            "start_time": round_obj.start_time,
            "end_time": round_obj.end_time,
            "created_on": round_obj.created_on,
            "round_holes": [
                {
                    "id": hole.id,
                    "score": hole.score,
                    "gir": hole.gir,
                    "fairway": hole.fairway,
                    "putts": hole.putts,
                    "tee_box_hole_id": hole.tee_box_hole_id,
                    "hole_number": self._get_hole_number(db, hole.tee_box_hole_id)
                }
                for hole in round_holes
            ]
        }
    
    def add_round_hole(self, db: Session, round_id: str, tee_box_hole_id: str, hole_data: Dict[str, Any]) -> RoundHole:
        """
        Add a hole to a round.
        
        Args:
            db: Database session
            round_id: Round ID
            tee_box_hole_id: Tee box hole ID
            hole_data: Hole data
            
        Returns:
            RoundHole: The created round hole
            
        Raises:
            ResourceNotFoundException: If the round is not found
            ValidationException: If a score for this hole already exists
            DatabaseException: If there's an error creating the round hole
        """
        # Verify the round exists
        round_obj = self.get(db, round_id)
        if round_obj is None:
            raise ResourceNotFoundException("Round", round_id)
        
        # Check if a score for this hole already exists
        existing_hole = db.query(RoundHole).filter(
            RoundHole.round_id == round_id,
            RoundHole.tee_box_hole_id == tee_box_hole_id
        ).first()
        
        if existing_hole:
            # Get hole number for better error message
            hole_number = self._get_hole_number(db, tee_box_hole_id)
            raise ValidationException(f"A score for hole {hole_number} already exists for this round. Use the update endpoint instead.")
        
        # Create the round hole
        try:
            round_hole = RoundHole(
                round_id=round_id,
                tee_box_hole_id=tee_box_hole_id,
                **hole_data
            )
            db.add(round_hole)
            db.commit()
            db.refresh(round_hole)
            
            # Update the round's total score
            self._update_round_total_score(db, round_id)
            
            return round_hole
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error adding round hole: {str(e)}")
    
    def update_round_hole(self, db: Session, round_hole_id: str, hole_data: Dict[str, Any]) -> RoundHole:
        """
        Update a round hole.
        
        Args:
            db: Database session
            round_hole_id: Round hole ID
            hole_data: Hole data
            
        Returns:
            RoundHole: The updated round hole
            
        Raises:
            ResourceNotFoundException: If the round hole is not found
            DatabaseException: If there's an error updating the round hole
        """
        # Get the round hole
        round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
        if round_hole is None:
            raise ResourceNotFoundException("RoundHole", round_hole_id)
        
        # Update the round hole
        try:
            for key, value in hole_data.items():
                if hasattr(round_hole, key):
                    setattr(round_hole, key, value)
            
            db.add(round_hole)
            db.commit()
            db.refresh(round_hole)
            
            # Update the round's total score
            self._update_round_total_score(db, round_hole.round_id)
            
            return round_hole
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error updating round hole: {str(e)}")
    
    def delete_round_hole(self, db: Session, round_hole_id: str) -> None:
        """
        Delete a round hole.
        
        Args:
            db: Database session
            round_hole_id: Round hole ID
            
        Raises:
            ResourceNotFoundException: If the round hole is not found
            DatabaseException: If there's an error deleting the round hole
        """
        # Get the round hole
        round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
        if round_hole is None:
            raise ResourceNotFoundException("RoundHole", round_hole_id)
        
        round_id = round_hole.round_id
        
        # Delete the round hole
        try:
            db.delete(round_hole)
            db.commit()
            
            # Update the round's total score
            self._update_round_total_score(db, round_id)
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Error deleting round hole: {str(e)}")
    
    def _update_round_total_score(self, db: Session, round_id: str) -> None:
        """
        Update a round's total score based on its holes.
        
        Args:
            db: Database session
            round_id: Round ID
        """
        # Get all holes for the round
        round_holes = db.query(RoundHole).filter(RoundHole.round_id == round_id).all()
        
        # Calculate total score
        total_score = sum(hole.score for hole in round_holes if hole.score is not None)
        
        # Update the round
        round_obj = self.get(db, round_id)
        if round_obj:
            round_obj.total_score = total_score
            db.add(round_obj)
            db.commit()
    
    def _get_hole_number(self, db: Session, tee_box_hole_id: str) -> Optional[int]:
        """
        Get the hole number for a tee box hole.
        
        Args:
            db: Database session
            tee_box_hole_id: Tee box hole ID
            
        Returns:
            Optional[int]: The hole number if found, None otherwise
        """
        tee_box_hole = db.query(TeeBoxHole).filter(TeeBoxHole.id == tee_box_hole_id).first()
        return tee_box_hole.hole_number if tee_box_hole else None
        
    def get_round_hole(self, db: Session, round_hole_id: str) -> Dict[str, Any]:
        """
        Get detailed information for a round hole.
        
        Args:
            db: Database session
            round_hole_id: Round hole ID
            
        Returns:
            Dict[str, Any]: Round hole data with additional context
            
        Raises:
            ResourceNotFoundException: If the round hole is not found
        """
        # Get the round hole
        round_hole = db.query(RoundHole).filter(RoundHole.id == round_hole_id).first()
        if round_hole is None:
            raise ResourceNotFoundException("RoundHole", round_hole_id)
        
        # Get additional context
        round_obj = self.get(db, round_hole.round_id)
        tee_box_hole = db.query(TeeBoxHole).filter(TeeBoxHole.id == round_hole.tee_box_hole_id).first()
        
        # Create response data
        response_data = {
            "id": round_hole.id,
            "round_id": round_hole.round_id,
            "tee_box_hole_id": round_hole.tee_box_hole_id,
            "score": round_hole.score,
            "gir": round_hole.gir,
            "fairway": round_hole.fairway,
            "putts": round_hole.putts,
            "penalties": round_hole.penalties,
            "sand": round_hole.sand,
            "water": round_hole.water,
            "created_on": round_hole.created_on,
            # Additional context
            "hole_number": tee_box_hole.hole_number if tee_box_hole else None,
            "par": tee_box_hole.par if tee_box_hole else None,
            "yards": tee_box_hole.yardage if tee_box_hole else None,
            "handicap": tee_box_hole.handicap if tee_box_hole else None,
            "course_id": round_obj.course_id if round_obj else None,
            "player_id": round_obj.player_id if round_obj else None
        }
        
        return response_data


# Create a singleton instance
round_repository = RoundRepository() 