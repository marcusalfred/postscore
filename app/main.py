"""
POSTscore API - Golf score tracking application.

This is the main application entry point that sets up the FastAPI instance,
configures middleware, exception handlers, and includes all routes.
"""
import logging

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

_logger = logging.getLogger(__name__)

# New versioned API
from api.v1.api import api_router as api_v1_router

# Core modules
from core.config import settings
from core.logging import setup_logging, RequestLoggingMiddleware
from core.errors import APIException

# Set up logging
setup_logging()


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI instance.
    
    Returns:
        FastAPI: The configured application
    """
    if settings.ENVIRONMENT == "production" and settings.SECRET_KEY == "dev-secret-key-do-not-use-in-production":
        raise RuntimeError("SECRET_KEY must be set in production")

    app = FastAPI(
        title='POSTscore',
        description='An API to record your scores at different golf courses',
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Add middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers — single handler for APIException and all subclasses
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )
    
    # New versioned API
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    
    # Root router for UI
    router = APIRouter()
    
    @router.get('/')
    def api_index():
        return RedirectResponse(url='/docs')
    
    @router.get('/{path:path}', status_code=404)
    async def api_404():
        # So we don't fall through to the index page
        return {'message': 'Not Found'}
    
    app.include_router(router)
    
    # Custom OpenAPI schema with better organization
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
            
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": f"{settings.API_V1_STR}/auth/login",
                        "scopes": {},
                    }
                },
            }
        }
        
        # Group tags in a meaningful order
        openapi_schema["tags"] = [
            {"name": "Players", "description": "Player management operations"},
            {"name": "Courses", "description": "Golf course management operations"},
            {"name": "Rounds", "description": "Round and scoring operations"},
            {"name": "Authentication", "description": "Authentication operations"},
            {"name": "Admin", "description": "Administrative operations (super users only)"},
        ]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    return app


app = create_application()

