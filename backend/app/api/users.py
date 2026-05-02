from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User, UserRole
from app.models.service_point import ServicePoint
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.dependencies import require_admin
from app.core.security import hash_password
from app.utils.logger import logger
from app.utils import errors as E

router = APIRouter(prefix="/api/users", tags=["Pengguna"])


def _user_to_dict(user: User, db: Session) -> dict:
    sp_name = None
    if user.service_point_id:
        sp = db.query(ServicePoint).filter(ServicePoint.id == user.service_point_id).first()
        sp_name = sp.name if sp else None
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else user.role,
        "service_point_id": user.service_point_id,
        "service_point_name": sp_name,
        "is_active": user.is_active,
        "force_password_change": user.force_password_change,
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "created_at": user.created_at.isoformat(),
    }


@router.get("")
def list_users(
    search: Optional[str] = Query(None),
    show_inactive: bool = Query(False),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = db.query(User)
    if not show_inactive:
        query = query.filter(User.is_active == True)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))

    total = query.count()
    per_page = 20
    users = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "success": True,
        "message": "Berhasil",
        "data": [_user_to_dict(u, db) for u in users],
        "pagination": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        },
    }


@router.post("", status_code=201)
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(status_code=409, detail=E.MASTER_EMAIL_DUPLICATE)

    if body.role == "user_sp" and not body.service_point_id:
        raise HTTPException(status_code=400, detail="Service point wajib untuk user SP.")

    user = User(
        name=body.name,
        email=body.email,
        password_hash=hash_password(body.password),
        role=body.role,
        service_point_id=body.service_point_id,
        is_active=True,
        force_password_change=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"User dibuat | action=tambah entity=user id={user.id} user_id={admin.id}")
    return {"success": True, "message": "Pengguna berhasil dibuat", "data": _user_to_dict(user, db)}


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)
    return {"success": True, "message": "Berhasil", "data": _user_to_dict(user, db)}


@router.put("/{user_id}")
def update_user(
    user_id: int,
    body: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    if body.email and body.email != user.email:
        existing = db.query(User).filter(User.email == body.email).first()
        if existing:
            raise HTTPException(status_code=409, detail=E.MASTER_EMAIL_DUPLICATE)

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    logger.info(f"User diupdate | action=edit entity=user id={user_id} user_id={admin.id}")
    return {"success": True, "message": "Pengguna berhasil diperbarui", "data": _user_to_dict(user, db)}


@router.patch("/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Tidak dapat menonaktifkan akun sendiri.")

    user.is_active = not user.is_active
    db.commit()
    action = "aktifkan" if user.is_active else "nonaktifkan"
    logger.info(f"User {action} | action=nonaktif entity=user id={user_id} user_id={admin.id}")
    status_msg = "diaktifkan" if user.is_active else "dinonaktifkan"
    return {"success": True, "message": f"Pengguna berhasil {status_msg}", "data": _user_to_dict(user, db)}


@router.post("/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """Reset password user dan set force_password_change = true."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    from app.core.security import hash_password as hp
    user.password_hash = hp("Vsat123!")
    user.force_password_change = True
    db.commit()

    logger.info(f"Password direset | user_id={user_id} by_admin={admin.id}")
    return {"success": True, "message": "Password berhasil direset. User wajib ganti password saat login.", "data": None}
