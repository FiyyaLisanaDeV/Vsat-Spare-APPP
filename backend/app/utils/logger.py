import sys
import os
from loguru import logger
from app.core.config import settings

# Hapus default handler
logger.remove()

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan> | "
    "{message}"
)

# Development: stdout
logger.add(
    sys.stdout,
    format=LOG_FORMAT,
    level=settings.LOG_LEVEL,
    colorize=True,
)

# Production: file dengan rotasi harian
LOG_DIR = "/logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger.add(
    f"{LOG_DIR}/app.log",
    format=LOG_FORMAT,
    level=settings.LOG_LEVEL,
    rotation="00:00",  # Rotasi tengah malam
    retention=f"{settings.LOG_RETENTION_DAYS} days",
    compression="zip",
    enqueue=True,  # Thread-safe
)

__all__ = ["logger"]
