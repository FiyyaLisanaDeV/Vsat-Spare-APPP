import re
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from app.models.user import User, RefreshToken
from app.core.security import (
    verify_password, hash_password, create_access_token,
    create_refresh_token, decode_refresh_token, hash_token
)
from app.core.config import settings
from app.utils.logger import logger
from app.utils import errors as E


def validate_password_strength(password: str) -> bool:
    """Validasi kekuatan password: min 8 karakter, 1 huruf besar, 1 angka."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentikasi user. Return User jika sukses, None jika gagal."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_user_tokens(user: User, db: Session) -> tuple[str, str]:
    """Buat access token dan refresh token untuk user."""
    payload = {
        "user_id": user.id,
        "role": user.role.value if hasattr(user.role, "value") else user.role,
        "service_point_id": user.service_point_id,
    }
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    # Simpan hash refresh token ke database
    token_hash = hash_token(refresh_token)
    expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    db_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        revoked=False,
    )
    db.add(db_token)
    db.commit()

    return access_token, refresh_token


def revoke_refresh_token(db: Session, token: str) -> bool:
    """Revoke refresh token. Return True jika berhasil."""
    token_hash = hash_token(token)
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
        )
        .first()
    )
    if not db_token:
        return False

    db_token.revoked = True
    db.commit()
    return True


def refresh_access_token(db: Session, refresh_token: str) -> tuple[str, str]:
    """Refresh access token menggunakan refresh token yang valid."""
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_TOKEN_EXPIRED,
        )

    token_hash = hash_token(refresh_token)
    db_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
        )
        .first()
    )

    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_TOKEN_EXPIRED,
        )

    # Revoke token lama
    db_token.revoked = True
    db.flush()

    # Ambil user
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=E.AUTH_ACCOUNT_DISABLED,
        )

    # Buat token baru
    new_access, new_refresh = create_user_tokens(user, db)
    return new_access, new_refresh


def revoke_all_user_tokens(db: Session, user_id: int):
    """Revoke semua refresh token aktif milik user (digunakan saat restore)."""
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False,
    ).update({"revoked": True})
    db.commit()


def change_user_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str,
) -> User:
    """Ganti password user dengan validasi lengkap."""
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=E.AUTH_INVALID_CREDENTIALS,
        )

    if verify_password(new_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=E.AUTH_PASSWORD_SAME_AS_OLD,
        )

    if not validate_password_strength(new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=E.AUTH_PASSWORD_WEAK,
        )

    user.password_hash = hash_password(new_password)
    user.force_password_change = False
    db.commit()
    db.refresh(user)
    return user
