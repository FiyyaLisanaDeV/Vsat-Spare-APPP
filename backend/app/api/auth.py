from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.base import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, ChangePasswordRequest, MeResponse
from app.services import auth_service
from app.core.dependencies import get_current_user
from app.utils.responses import success_response, error_response
from app.utils.logger import logger
from app.utils import errors as E

router = APIRouter(prefix="/api/auth", tags=["Autentikasi"])
limiter = Limiter(key_func=get_remote_address)

COOKIE_NAME = "refresh_token"


@router.post("/login")
@limiter.limit("5/15minutes")
async def login(
    request: Request,
    response: Response,
    body: LoginRequest,
    db: Session = Depends(get_db),
):
    """Login dengan email dan password."""
    ip = get_remote_address(request)

    user = auth_service.authenticate_user(db, body.email, body.password)

    if not user:
        logger.warning(f"Login gagal | email={body.email} ip={ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_INVALID_CREDENTIALS,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_ACCOUNT_DISABLED,
        )

    access_token, refresh_token = auth_service.create_user_tokens(user, db)

    # Update last_login
    user.last_login = datetime.utcnow()
    db.commit()

    logger.info(f"Login berhasil | user_id={user.id} email={user.email} ip={ip}")

    # Set refresh token di httpOnly cookie
    response.set_cookie(
        key=COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=False,  # Set True di production dengan HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7,  # 7 hari
        path="/api/auth",
    )

    return {
        "success": True,
        "message": "Login berhasil",
        "data": {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "role": user.role.value if hasattr(user.role, "value") else user.role,
            "name": user.name,
            "force_password_change": user.force_password_change,
        },
    }


@router.post("/refresh")
async def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    """Refresh access token menggunakan refresh token dari httpOnly cookie."""
    refresh_token_cookie = request.cookies.get(COOKIE_NAME)

    if not refresh_token_cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_TOKEN_EXPIRED,
        )

    new_access, new_refresh = auth_service.refresh_access_token(db, refresh_token_cookie)

    # Set refresh token baru
    response.set_cookie(
        key=COOKIE_NAME,
        value=new_refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/api/auth",
    )

    return {
        "success": True,
        "message": "Token diperbarui",
        "data": {"access_token": new_access, "token_type": "bearer"},
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Logout dan revoke refresh token."""
    refresh_token_cookie = request.cookies.get(COOKIE_NAME)

    if refresh_token_cookie:
        auth_service.revoke_refresh_token(db, refresh_token_cookie)

    # Hapus cookie
    response.delete_cookie(key=COOKIE_NAME, path="/api/auth")

    logger.info(f"Logout | user_id={current_user.id}")

    return {"success": True, "message": "Logout berhasil", "data": None}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """Ambil data user yang sedang login."""
    return {
        "success": True,
        "message": "Berhasil",
        "data": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role.value if hasattr(current_user.role, "value") else current_user.role,
            "service_point_id": current_user.service_point_id,
            "force_password_change": current_user.force_password_change,
            "is_active": current_user.is_active,
        },
    }


@router.post("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Ganti password user."""
    auth_service.change_user_password(
        db, current_user, body.current_password, body.new_password
    )
    logger.info(f"Password diubah | user_id={current_user.id}")
    return {"success": True, "message": "Password berhasil diubah", "data": None}
