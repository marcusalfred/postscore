"""
Logging configuration for the application.
Provides structured logging for easier log analysis.
"""
import json
import logging
import sys
import time
from typing import Dict, Any, Optional, Union, List
from contextvars import ContextVar, Token
from datetime import datetime

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field

from core.config import settings

# Context variable to store request information
request_id_var: ContextVar[str] = ContextVar("request_id", default="")
request_context_var: ContextVar[Dict[str, Any]] = ContextVar("request_context", default={})


class JSONLogFormatter(logging.Formatter):
    """
    JSON log formatter for structured logging.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.
        
        Args:
            record: The log record
            
        Returns:
            str: JSON formatted log string
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "function": record.funcName,
        }
        
        # Add request context if available
        try:
            request_context = request_context_var.get()
            if request_context:
                log_data["request"] = request_context
        except LookupError:
            pass
        
        # Add request ID if available
        try:
            request_id = request_id_var.get()
            if request_id:
                log_data["request_id"] = request_id
        except LookupError:
            pass
        
        # Add extra attributes
        if hasattr(record, "props"):
            log_data.update(record.props)
        
        # Add exception info if available
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }
        
        return json.dumps(log_data)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log HTTP requests and responses and set request context.
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request and log request/response details.
        
        Args:
            request: The HTTP request
            call_next: The next middleware in the chain
            
        Returns:
            Response: The HTTP response
        """
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        request_id_token = request_id_var.set(request_id)
        
        # Set request context
        request_context = {
            "id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host if request.client else None,
            "headers": {k: v for k, v in request.headers.items() if k.lower() not in ["authorization", "cookie"]},
        }
        request_context_token = request_context_var.set(request_context)
        
        # Log request
        logging.info(f"Request: {request.method} {request.url.path}", extra={"props": {"request": request_context}})
        
        # Process request
        start_time = time.time()
        try:
            response = await call_next(request)
            
            # Log response
            duration = time.time() - start_time
            response_data = {
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            }
            logging.info(
                f"Response: {response.status_code} ({round(duration * 1000, 2)}ms)", 
                extra={"props": {"response": response_data}}
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            # Log exception
            duration = time.time() - start_time
            logging.exception(
                f"Request failed: {str(e)}", 
                extra={"props": {"duration_ms": round(duration * 1000, 2)}}
            )
            raise
        finally:
            # Clear context
            try:
                request_id_var.reset(request_id_token)
                request_context_var.reset(request_context_token)
            except LookupError:
                pass


def setup_logging():
    """
    Set up structured logging for the application.
    """
    # Get log level from settings
    log_level_name = settings.ENVIRONMENT.upper() if settings.ENVIRONMENT.upper() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] else "INFO"
    log_level = getattr(logging, log_level_name)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONLogFormatter())
    root_logger.addHandler(console_handler)
    
    # Configure other loggers
    for logger_name in ["uvicorn", "sqlalchemy.engine", "fastapi"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True
    
    # Log startup message
    logging.info(
        f"Logging initialized (level={log_level_name})", 
        extra={"props": {"environment": settings.ENVIRONMENT}}
    ) 