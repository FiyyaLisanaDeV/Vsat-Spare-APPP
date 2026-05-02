from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.startup import verify_pg_tools
from app.utils.logger import logger
from app.utils import errors as E

# Import routers
from app.api import auth, users, service_points, items, backup

# Import scheduler
from app.scheduler.backup_scheduler import start_scheduler, stop_scheduler

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup dan shutdown events."""
    # Startup
    logger.info("=== VSAT Spare Stock Management System - Startup ===")

    # Verifikasi SECRET_KEY
    if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
        logger.critical("SECRET_KEY tidak ditemukan atau terlalu pendek di ENV!")
        raise RuntimeError("SECRET_KEY wajib diisi minimal 32 karakter di .env")

    # Verifikasi pg_dump tersedia
    try:
        verify_pg_tools()
    except RuntimeError as e:
        logger.critical(str(e))
        raise

    # Start scheduler
    start_scheduler()
    logger.info("Sistem siap digunakan.")

    yield

    # Shutdown
    stop_scheduler()
    logger.info("=== Sistem dimatikan ===")


# ─── App Init ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="VSAT Spare Stock Management API",
    description="API untuk sistem manajemen spare stock VSAT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Rate Limiter ─────────────────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Global Exception Handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Tangkap semua error 500 — jangan expose stack trace ke client."""
    logger.error(f"Unhandled exception | path={request.url.path} | detail={str(exc)}")
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
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "message": E.AUTH_RATE_LIMIT,
            "errors": None,
        },
    )


# ─── Restore Middleware ────────────────────────────────────────────────────────
@app.middleware("http")
async def restore_lock_middleware(request: Request, call_next):
    """Tolak semua request (kecuali health) saat restore berjalan."""
    from app.api.backup import _restore_in_progress
    if _restore_in_progress and request.url.path not in ("/health", "/"):
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "message": E.MAINTENANCE_MODE,
                "errors": None,
            },
        )
    return await call_next(request)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "message": "VSAT Spare API berjalan normal"}


@app.get("/", tags=["System"])
def root():
    return {"message": "VSAT Spare Stock Management API v1.0"}


# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(service_points.router)
app.include_router(items.router)
app.include_router(backup.router)
