"""
Round repository for database operations.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import func, select
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
        return db.execute(select(self.model).where(self.model.player_id == player_id)).scalars().all()
    
    def get_by_course(self, db: Session, course_id: str) -> List[Round]:
        """
        Get all rounds for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            List[Round]: List of rounds for the course
        """
        return db.execute(select(self.model).where(self.model.course_id == course_id)).scalars().all()
    
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
        round_holes = db.execute(select(RoundHole).where(RoundHole.round_id == round_id)).scalars().all()

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
        existing_hole = db.execute(
            select(RoundHole).where(
                RoundHole.round_id == round_id,
                RoundHole.tee_box_hole_id == tee_box_hole_id
            )
        ).scalar_one_or_none()
        
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
        round_hole = db.execute(select(RoundHole).where(RoundHole.id == round_hole_id)).scalar_one_or_none()
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
        round_hole = db.execute(select(RoundHole).where(RoundHole.id == round_hole_id)).scalar_one_or_none()
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
        round_holes = db.execute(select(RoundHole).where(RoundHole.round_id == round_id)).scalars().all()

        # Calculate total score
        scored_holes = [hole.score for hole in round_holes if hole.score is not None]
        total_score = sum(scored_holes) if scored_holes else None
        
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
        tee_box_hole = db.execute(select(TeeBoxHole).where(TeeBoxHole.id == tee_box_hole_id)).scalar_one_or_none()
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
        round_hole = db.execute(select(RoundHole).where(RoundHole.id == round_hole_id)).scalar_one_or_none()
        if round_hole is None:
            raise ResourceNotFoundException("RoundHole", round_hole_id)

        # Get additional context
        round_obj = self.get(db, round_hole.round_id)
        tee_box_hole = db.execute(select(TeeBoxHole).where(TeeBoxHole.id == round_hole.tee_box_hole_id)).scalar_one_or_none()
        
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


    def get_round_stats(self, db: Session, round_id: str) -> Dict[str, Any]:
        """
        Calculate statistics for a round.

        Args:
            db: Database session
            round_id: Round ID

        Returns:
            Dict[str, Any]: Statistics matching RoundStatsResponse fields

        Raises:
            ResourceNotFoundException: If the round is not found
        """
        # Verify round exists
        round_obj = self.get(db, round_id)
        if round_obj is None:
            raise ResourceNotFoundException("Round", round_id)

        # Fetch all round holes
        round_holes = db.execute(
            select(RoundHole).where(RoundHole.round_id == round_id)
        ).scalars().all()

        if not round_holes:
            return {
                "total_score": None,
                "par": None,
                "to_par": None,
                "greens_in_regulation": None,
                "gir_percentage": None,
                "fairways_hit": None,
                "fairways_percentage": None,
                "avg_putts_per_hole": None,
                "total_putts": None,
                "penalties": None,
                "sand_shots": None,
                "water_shots": None,
            }

        # Fetch TeeBoxHoles for par values
        tee_box_hole_ids = [rh.tee_box_hole_id for rh in round_holes]
        tee_box_holes = db.execute(
            select(TeeBoxHole).where(TeeBoxHole.id.in_(tee_box_hole_ids))
        ).scalars().all()
        tbh_map = {tbh.id: tbh for tbh in tee_box_holes}

        played_holes = len(round_holes)

        # total_score
        scored_holes = [rh.score for rh in round_holes if rh.score is not None]
        total_score = sum(scored_holes) if scored_holes else None

        # par (sum of par for played holes)
        par_values = [
            tbh_map[rh.tee_box_hole_id].par
            for rh in round_holes
            if rh.tee_box_hole_id in tbh_map and tbh_map[rh.tee_box_hole_id].par is not None
        ]
        par = sum(par_values) if par_values else None

        # to_par
        to_par = (total_score - par) if (total_score is not None and par is not None) else None

        # greens_in_regulation
        gir_holes = [rh for rh in round_holes if rh.gir is not None]
        greens_in_regulation = sum(1 for rh in gir_holes if rh.gir is True)
        gir_percentage = (
            round(greens_in_regulation / played_holes * 100, 1) if played_holes > 0 else None
        )

        # fairways_hit — only applies to non-par-3 holes
        non_par3_holes = [
            rh for rh in round_holes
            if rh.tee_box_hole_id in tbh_map and tbh_map[rh.tee_box_hole_id].par != 3
        ]
        fairways_applicable = len(non_par3_holes)
        fairways_hit = sum(1 for rh in non_par3_holes if rh.fairway == 'o')
        fairways_percentage = (
            round(fairways_hit / fairways_applicable * 100, 1) if fairways_applicable > 0 else None
        )

        # putts
        holes_with_putts = [rh for rh in round_holes if rh.putts is not None]
        total_putts = sum(rh.putts for rh in holes_with_putts) if holes_with_putts else None
        avg_putts_per_hole = (
            round(total_putts / len(holes_with_putts), 1)
            if holes_with_putts and total_putts is not None
            else None
        )

        # penalties
        holes_with_penalties = [rh for rh in round_holes if rh.penalties is not None]
        penalties = sum(rh.penalties for rh in holes_with_penalties) if holes_with_penalties else None

        # sand_shots
        holes_with_sand = [rh for rh in round_holes if rh.sand is not None]
        sand_shots = sum(1 for rh in holes_with_sand if rh.sand is True) if holes_with_sand else None

        # water_shots
        holes_with_water = [rh for rh in round_holes if rh.water is not None]
        water_shots = sum(1 for rh in holes_with_water if rh.water is True) if holes_with_water else None

        return {
            "total_score": total_score,
            "par": par,
            "to_par": to_par,
            "greens_in_regulation": greens_in_regulation,
            "gir_percentage": gir_percentage,
            "fairways_hit": fairways_hit,
            "fairways_percentage": fairways_percentage,
            "avg_putts_per_hole": avg_putts_per_hole,
            "total_putts": total_putts,
            "penalties": penalties,
            "sand_shots": sand_shots,
            "water_shots": water_shots,
        }


# Create a singleton instance
round_repository = RoundRepository()