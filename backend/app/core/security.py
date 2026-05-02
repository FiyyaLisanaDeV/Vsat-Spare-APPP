from datetime import datetime, timedelta
from typing import Optional, Any, Dict
import bcrypt
from jose import jwt, JWTError
from app.core.config import settings
from app.utils.logger import logger

ALGORITHM = "HS256"


# ─── Password Hashing ────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt dengan cost factor 12."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password terhadap hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ─── JWT ─────────────────────────────────────────────────────────────────────

def create_access_token(data: Dict[str, Any]) -> str:
    """Buat access token JWT dengan expiry 15 menit."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Buat refresh token JWT dengan expiry 7 hari."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode dan validasi access token. Return None jika invalid/expired."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        return None


def decode_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode dan validasi refresh token. Return None jika invalid/expired."""
    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError as e:
        logger.error(f"Refresh JWT decode error: {str(e)}")
        return None


def hash_token(token: str) -> str:
    """Hash token untuk disimpan di database (bukan plain text)."""
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()
