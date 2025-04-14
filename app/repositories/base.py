"""
Base repository class for database operations.
This module provides a generic repository pattern implementation
for basic CRUD operations.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.models import Base
from core.errors import ResourceNotFoundException

# Define type variables for models and schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository class with default CRUD operations.
    
    Attributes:
        model: SQLAlchemy model class
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the repository with the model class.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: str) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            Optional[ModelType]: The record if found, None otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_or_404(self, db: Session, id: str) -> ModelType:
        """
        Get a single record by ID or raise an exception if not found.
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            ModelType: The record
            
        Raises:
            ResourceNotFoundException: If the record is not found
        """
        obj = self.get(db, id)
        if obj is None:
            raise ResourceNotFoundException(self.model.__tablename__, id)
        return obj
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[ModelType]: List of records
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Create schema with the data
            
        Returns:
            ModelType: The created record
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record.
        
        Args:
            db: Database session
            db_obj: Record to update
            obj_in: Update schema with the data or dictionary
            
        Returns:
            ModelType: The updated record
        """
        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: str) -> ModelType:
        """
        Remove a record.
        
        Args:
            db: Database session
            id: Record ID
            
        Returns:
            ModelType: The removed record
            
        Raises:
            ResourceNotFoundException: If the record is not found
        """
        obj = self.get_or_404(db, id)
        db.delete(obj)
        db.commit()
        return obj 