"""
Centralized exception handling for the application.
This module defines standard exceptions that can be raised throughout the application
and handled consistently by FastAPI's exception handlers.
"""
from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class APIException(HTTPException):
    """Base exception for all API errors."""
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class ResourceNotFoundException(APIException):
    """Raised when a requested resource is not found."""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_type} with id {resource_id} not found"
        )


class ValidationException(APIException):
    """Raised when input validation fails."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class AuthorizationException(APIException):
    """Raised when a user is not authorized to perform an action."""
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class AuthenticationException(APIException):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "Could not validate credentials", headers: Dict[str, str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers or {"WWW-Authenticate": "Bearer"}
        )


class DatabaseException(APIException):
    """Raised when a database operation fails."""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        ) 