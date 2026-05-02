from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    Application settings with support for environment variables.
    Uses Pydantic V2 BaseSettings for type validation.
    """

    # Database Configuration
    DATABASE_URL: str = "postgresql://vsat_user:password@postgres:5432/vsat_db"
    POSTGRES_USER: str = "vsat_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "vsat_db"

    # Database Pool Settings (SQLAlchemy)
    DB_POOL_SIZE: int = 20  # Connection pool size
    DB_MAX_OVERFLOW: int = 10  # Max overflow connections
    DB_POOL_RECYCLE: int = 3600  # Recycle connections every 1 hour
    DB_ECHO: bool = False  # Log SQL queries (disable in production)

    # JWT Authentication
    SECRET_KEY: str  # Must be at least 32 characters
    REFRESH_SECRET_KEY: str  # Separate key for refresh tokens
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Configuration
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100  # Requests per window
    RATE_LIMIT_WINDOW_SECONDS: int = 60  # Time window in seconds

    # Backup Configuration
    BACKUP_RETENTION: int = 14  # Days to keep backups
    MAX_UPLOAD_SIZE_MB: int = 200  # Max upload size

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_RETENTION_DAYS: int = 30

    # Timezone
    TZ: str = "Asia/Jakarta"

    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    @property
    def database_settings(self) -> dict:
        """Return SQLAlchemy connection pool settings."""
        return {
            "poolclass": "NullPool",  # Use for serverless environments
            "pool_size": self.DB_POOL_SIZE,
            "max_overflow": self.DB_MAX_OVERFLOW,
            "pool_recycle": self.DB_POOL_RECYCLE,
            "echo": self.DB_ECHO,
        }

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reloading from disk on every import.
    """
    return Settings()

# Create single instance for use throughout app
settings = get_settings()
