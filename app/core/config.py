"""
Application configuration settings.
This module manages all configuration for the application,
with support for environment variables and different environments.
"""
import os
from typing import Dict, List, Optional, Union, Any
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


_DEFAULT_SECRET_KEY = "dev-secret-key-do-not-use-in-production"


class Settings(BaseSettings):
    """
    Application settings that can be overridden by environment variables.
    """
    # API Settings
    API_V1_STR: str = "/api/v1"
    API_VERSION: str = "0.2.0"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", _DEFAULT_SECRET_KEY)
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 1 week
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database — uses the same DB_* vars as docker-compose and db/database.py
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "postgres")
    DB_NAME: str = os.environ.get("DB_NAME", "postscore")
    DB_PORT: str = os.environ.get("DB_PORT", "5432")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        db_url = (
            f"postgresql://{info.data.get('DB_USER')}:{info.data.get('DB_PASSWORD')}"
            f"@{info.data.get('DB_HOST')}:{info.data.get('DB_PORT')}/{info.data.get('DB_NAME', '')}"
        )
        return db_url

    # Initial superuser setup key
    SETUP_SECRET: Optional[str] = os.environ.get("SETUP_SECRET", None) or None
    
    # Environment name
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    
    # Debug mode
    DEBUG: bool = os.environ.get("DEBUG", "True").lower() in ("true", "1", "t")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore"
    }


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    return settings 