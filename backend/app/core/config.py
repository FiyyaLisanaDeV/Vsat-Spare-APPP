from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://vsat_user:password@postgres:5432/vsat_db"
    POSTGRES_USER: str = "vsat_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "vsat_db"

    # JWT
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

    # Backup
    BACKUP_RETENTION: int = 14
    MAX_UPLOAD_SIZE_MB: int = 200

    # Log
    LOG_LEVEL: str = "INFO"
    LOG_RETENTION_DAYS: int = 30

    # Timezone
    TZ: str = "Asia/Jakarta"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
