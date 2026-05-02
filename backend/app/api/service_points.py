from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.models.service_point import ServicePoint, ServicePointType
from app.schemas.service_point import ServicePointCreate, ServicePointUpdate
from app.core.dependencies import require_admin
from app.utils.logger import logger
from app.utils import errors as E

router = APIRouter(prefix="/api/service-points", tags=["Service Point"])


def _sp_to_dict(sp: ServicePoint) -> dict:
    return {
        "id": sp.id,
        "name": sp.name,
        "type": sp.type.value if hasattr(sp.type, "value") else sp.type,
        "city": sp.city,
        "province": sp.province,
        "pic_name": sp.pic_name,
        "pic_phone": sp.pic_phone,
        "pic_email": sp.pic_email,
        "is_active": sp.is_active,
        "created_at": sp.created_at.isoformat(),
        "updated_at": sp.updated_at.isoformat(),
    }


@router.get("")
def list_service_points(
    search: Optional[str] = Query(None),
    show_inactive: bool = Query(False),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = db.query(ServicePoint)
    if not show_inactive:
        query = query.filter(ServicePoint.is_active == True)
    if search:
        query = query.filter(ServicePoint.name.ilike(f"%{search}%"))

    total = query.count()
    per_page = 20
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "success": True,
        "message": "Berhasil",
        "data": [_sp_to_dict(sp) for sp in items],
        "pagination": {"total": total, "page": page, "per_page": per_page,
                       "total_pages": (total + per_page - 1) // per_page},
    }


@router.post("", status_code=201)
def create_service_point(
    body: ServicePointCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    sp = ServicePoint(**body.model_dump())
    db.add(sp)
    db.commit()
    db.refresh(sp)
    logger.info(f"ServicePoint dibuat | action=tambah entity=service_point id={sp.id} user_id={admin.id}")
    return {"success": True, "message": "Service point berhasil dibuat", "data": _sp_to_dict(sp)}


@router.get("/{sp_id}")
def get_service_point(
    sp_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    sp = db.query(ServicePoint).filter(ServicePoint.id == sp_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)
    return {"success": True, "message": "Berhasil", "data": _sp_to_dict(sp)}


@router.put("/{sp_id}")
def update_service_point(
    sp_id: int,
    body: ServicePointUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    sp = db.query(ServicePoint).filter(ServicePoint.id == sp_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    for field, value in body.model_dump(exclude_none=True).items():
        setattr(sp, field, value)

    db.commit()
    db.refresh(sp)
    logger.info(f"ServicePoint diupdate | action=edit entity=service_point id={sp_id} user_id={admin.id}")
    return {"success": True, "message": "Service point berhasil diperbarui", "data": _sp_to_dict(sp)}


@router.patch("/{sp_id}/toggle-active")
def toggle_service_point_active(
    sp_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    sp = db.query(ServicePoint).filter(ServicePoint.id == sp_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    sp.is_active = not sp.is_active
    db.commit()
    status_msg = "diaktifkan" if sp.is_active else "dinonaktifkan"
    logger.info(f"ServicePoint {status_msg} | id={sp_id} user_id={admin.id}")
    return {"success": True, "message": f"Service point berhasil {status_msg}", "data": _sp_to_dict(sp)}
