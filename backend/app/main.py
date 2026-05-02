from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.startup import verify_pg_tools
from app.utils.logger import logger
from app.utils import errors as E

# Import routers
from app.api import auth, users, service_points, items, backup

# Import scheduler
from app.scheduler.backup_scheduler import start_scheduler, stop_scheduler

# Rate limiter with configurable limits
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager for startup and shutdown events.
    Handles initialization of critical services and graceful shutdown.
    """
    # ─── Startup ───────────────────────────────────────────────────────────
    logger.info("=" * 70)
    logger.info("🚀 VSAT Spare Stock Management System - Startup")
    logger.info("=" * 70)

    startup_errors = []

    # Verify SECRET_KEY
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
        error_msg = "SECRET_KEY tidak ditemukan atau terlalu pendek di ENV!"
        logger.critical(error_msg)
        startup_errors.append(error_msg)

    # Verify REFRESH_SECRET_KEY
    if not settings.REFRESH_SECRET_KEY or len(settings.REFRESH_SECRET_KEY) < 32:
        error_msg = "REFRESH_SECRET_KEY tidak ditemukan atau terlalu pendek di ENV!"
        logger.critical(error_msg)
        startup_errors.append(error_msg)

    if startup_errors:
        raise RuntimeError(f"Startup failed: {'; '.join(startup_errors)}")

    # Verify PostgreSQL tools
    try:
        verify_pg_tools()
        logger.info("✓ PostgreSQL tools verified")
    except RuntimeError as e:
        logger.critical(f"✗ PostgreSQL verification failed: {str(e)}")
        raise

    # Start background scheduler
    try:
        start_scheduler()
        logger.info("✓ Background scheduler started")
    except Exception as e:
        logger.error(f"✗ Failed to start scheduler: {str(e)}")
        # Don't fail startup if scheduler fails, just log it
        pass

    logger.info("✓ Sistem siap digunakan")
    logger.info("=" * 70)

    yield

    # ─── Shutdown ──────────────────────────────────────────────────────────
    logger.info("=" * 70)
    logger.info("⏹️  VSAT Spare Stock Management System - Shutdown")
    logger.info("=" * 70)

    try:
        stop_scheduler()
        logger.info("✓ Background scheduler stopped")
    except Exception as e:
        logger.error(f"✗ Error stopping scheduler: {str(e)}")

    logger.info("✓ Sistem berhasil dimatikan")
    logger.info("=" * 70)


# ─── FastAPI App Initialization ────────────────────────────────────────────
app = FastAPI(
    title="VSAT Spare Stock Management API",
    description="API untuk sistem manajemen spare stock VSAT dengan authentication dan backup",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ─── Rate Limiter Configuration ────────────────────────────────────────────
if settings.RATE_LIMIT_ENABLED:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    logger.info("✓ Rate limiting enabled")

# ─── CORS Middleware ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour
)
logger.info(f"✓ CORS configured for origins: {', '.join(settings.cors_origins)}")

# ─── Global Exception Handlers ─────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch all unhandled exceptions and return safe error response.
    Prevents leaking sensitive information like stack traces to clients.
    """
    logger.error(
        f"Unhandled exception | "
        f"path={request.url.path} | "
        f"method={request.method} | "
        f"detail={str(exc)}"
    )
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": E.SERVER_ERROR,
            "errors": None,
        },
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded errors."""
    logger.warning(f"Rate limit exceeded for {request.client.host}")
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": E.AUTH_RATE_LIMIT,
            "errors": None,
        },
    )


# ─── Restore/Maintenance Middleware ────────────────────────────────────────
@app.middleware("http")
async def restore_lock_middleware(request: Request, call_next):
    """
    Middleware to reject requests during database restore.
    Allows health check and root endpoints to pass through.
    """
    from app.api.backup import _restore_in_progress

    if _restore_in_progress and request.url.path not in ("/health", "/", "/docs"):
        logger.warning(f"Request blocked during restore: {request.url.path}")
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "message": E.MAINTENANCE_MODE,
                "errors": None,
            },
        )
    return await call_next(request)


# ─── Request Logging Middleware ────────────────────────────────────────────
@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    """Log request details for debugging and monitoring."""
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} | "
        f"status={response.status_code} | "
        f"duration={process_time:.3f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


# ─── Health Check Endpoints ────────────────────────────────────────────────
@app.get("/health", tags=["System"], summary="Health check endpoint")
def health_check():
    """
    Check if API is running and database is accessible.
    Used by Docker health checks and load balancers.
    """
    return {
        "status": "ok",
        "message": "VSAT Spare API berjalan normal",
        "timestamp": time.time(),
    }


@app.get("/", tags=["System"], summary="Root endpoint")
def root():
    """Welcome endpoint with API information."""
    return {
        "message": "VSAT Spare Stock Management API",
        "version": "1.0.0",
        "docs": "/docs",
    }


# ─── API Routers ──────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(service_points.router, prefix="/service-points", tags=["Service Points"])
app.include_router(items.router, prefix="/items", tags=["Items"])
app.include_router(backup.router, prefix="/backup", tags=["Backup"])

logger.info("✓ All routers registered successfully")
