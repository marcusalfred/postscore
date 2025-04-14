"""
POSTscore API - Golf score tracking application.

This is the main application entry point that sets up the FastAPI instance,
configures middleware, exception handlers, and includes all routes.
"""
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

# FastUI components for the index page
from fastui import AnyComponent, FastUI
from fastui import components as c

# New versioned API
from api.v1.api import api_router as api_v1_router

# Core modules
from core.config import settings
from core.logging import setup_logging, RequestLoggingMiddleware
from core.errors import APIException, ResourceNotFoundException, ValidationException, AuthorizationException, AuthenticationException, DatabaseException

# Set up logging
setup_logging()


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI instance.
    
    Returns:
        FastAPI: The configured application
    """
    app = FastAPI(
        title='POSTscore',
        description='An API to record your scores at different golf courses',
        version='0.2.0',
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
    
    # Exception handlers
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )

    @app.exception_handler(ResourceNotFoundException)
    async def not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(AuthorizationException)
    async def authorization_exception_handler(request: Request, exc: AuthorizationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(AuthenticationException)
    async def authentication_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # New versioned API
    app.include_router(api_v1_router, prefix=settings.API_V1_STR)
    
    # Root router for UI
    router = APIRouter()
    
    @router.get('/', response_model=FastUI, response_model_exclude_none=True)
    def api_index() -> list[AnyComponent]:
        # language=markdown
        markdown = """\
    POSTscore - Track your golf scores and stats!
    
    This application provides:
    
    * Player management
    * Course and tee box tracking
    * Round scoring
    * Statistics and analysis
    
    Check out the API documentation at [/docs](/docs) for available endpoints.
    """
        return [c.Markdown(content=markdown)]
    
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

