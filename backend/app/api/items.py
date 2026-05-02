from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.models.item import ItemType, ItemCategory, SpareItem
from app.models.stock import Stock
from app.schemas.item import (
    ItemTypeCreate, ItemTypeUpdate,
    ItemCategoryCreate, ItemCategoryUpdate,
    SpareItemCreate, SpareItemUpdate,
)
from app.core.dependencies import require_admin
from app.utils.logger import logger
from app.utils import errors as E

router = APIRouter(prefix="/api/items", tags=["Master Data Barang"])


# ═══════════════════════════════════════════════════════════════════════════════
# ITEM TYPES
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/types")
def list_item_types(
    search: Optional[str] = Query(None),
    show_inactive: bool = Query(False),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = db.query(ItemType)
    if not show_inactive:
        query = query.filter(ItemType.is_active == True)
    if search:
        query = query.filter(ItemType.name.ilike(f"%{search}%"))
    total = query.count()
    per_page = 20
    items = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "success": True,
        "message": "Berhasil",
        "data": [{"id": t.id, "name": t.name, "is_active": t.is_active,
                  "created_at": t.created_at.isoformat()} for t in items],
        "pagination": {"total": total, "page": page, "per_page": per_page,
                       "total_pages": (total + per_page - 1) // per_page},
    }


@router.post("/types", status_code=201)
def create_item_type(
    body: ItemTypeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    item_type = ItemType(name=body.name, is_active=True)
    db.add(item_type)
    db.commit()
    db.refresh(item_type)
    logger.info(f"ItemType dibuat | action=tambah entity=item_type id={item_type.id} user_id={admin.id}")
    return {"success": True, "message": "Jenis barang berhasil dibuat",
            "data": {"id": item_type.id, "name": item_type.name, "is_active": item_type.is_active}}


@router.put("/types/{type_id}")
def update_item_type(
    type_id: int,
    body: ItemTypeUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    item_type = db.query(ItemType).filter(ItemType.id == type_id).first()
    if not item_type:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(item_type, field, value)
    db.commit()
    db.refresh(item_type)
    return {"success": True, "message": "Jenis barang berhasil diperbarui",
            "data": {"id": item_type.id, "name": item_type.name, "is_active": item_type.is_active}}


@router.patch("/types/{type_id}/toggle-active")
def toggle_item_type(
    type_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    item_type = db.query(ItemType).filter(ItemType.id == type_id).first()
    if not item_type:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    if item_type.is_active:
        active_cats = db.query(ItemCategory).filter(
            ItemCategory.type_id == type_id, ItemCategory.is_active == True
        ).count()
        if active_cats > 0:
            raise HTTPException(status_code=400,
                                detail=E.MASTER_TYPE_IN_USE.format(n=active_cats))

    item_type.is_active = not item_type.is_active
    db.commit()
    status_msg = "diaktifkan" if item_type.is_active else "dinonaktifkan"
    return {"success": True, "message": f"Jenis barang berhasil {status_msg}", "data": None}


# ═══════════════════════════════════════════════════════════════════════════════
# ITEM CATEGORIES
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/categories")
def list_item_categories(
    type_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    show_inactive: bool = Query(False),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = db.query(ItemCategory)
    if not show_inactive:
        query = query.filter(ItemCategory.is_active == True)
    if type_id:
        query = query.filter(ItemCategory.type_id == type_id)
    if search:
        query = query.filter(ItemCategory.name.ilike(f"%{search}%"))
    total = query.count()
    per_page = 20
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for cat in items:
        type_obj = db.query(ItemType).filter(ItemType.id == cat.type_id).first()
        result.append({
            "id": cat.id, "name": cat.name, "type_id": cat.type_id,
            "type_name": type_obj.name if type_obj else None,
            "is_active": cat.is_active, "created_at": cat.created_at.isoformat(),
        })
    return {"success": True, "message": "Berhasil", "data": result,
            "pagination": {"total": total, "page": page, "per_page": per_page,
                           "total_pages": (total + per_page - 1) // per_page}}


@router.post("/categories", status_code=201)
def create_item_category(
    body: ItemCategoryCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    type_obj = db.query(ItemType).filter(ItemType.id == body.type_id).first()
    if not type_obj:
        raise HTTPException(status_code=404, detail="Jenis barang tidak ditemukan.")
    cat = ItemCategory(type_id=body.type_id, name=body.name, is_active=True)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    logger.info(f"ItemCategory dibuat | id={cat.id} user_id={admin.id}")
    return {"success": True, "message": "Kategori berhasil dibuat",
            "data": {"id": cat.id, "name": cat.name, "type_id": cat.type_id, "is_active": cat.is_active}}


@router.put("/categories/{cat_id}")
def update_item_category(
    cat_id: int,
    body: ItemCategoryUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    cat = db.query(ItemCategory).filter(ItemCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(cat, field, value)
    db.commit()
    db.refresh(cat)
    return {"success": True, "message": "Kategori berhasil diperbarui",
            "data": {"id": cat.id, "name": cat.name, "is_active": cat.is_active}}


@router.patch("/categories/{cat_id}/toggle-active")
def toggle_item_category(
    cat_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    cat = db.query(ItemCategory).filter(ItemCategory.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    if cat.is_active:
        active_items = db.query(SpareItem).filter(
            SpareItem.category_id == cat_id, SpareItem.is_active == True
        ).count()
        if active_items > 0:
            raise HTTPException(status_code=400,
                                detail=E.MASTER_CATEGORY_IN_USE.format(n=active_items))

    cat.is_active = not cat.is_active
    db.commit()
    status_msg = "diaktifkan" if cat.is_active else "dinonaktifkan"
    return {"success": True, "message": f"Kategori berhasil {status_msg}", "data": None}


# ═══════════════════════════════════════════════════════════════════════════════
# SPARE ITEMS
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/spare")
def list_spare_items(
    search: Optional[str] = Query(None),
    type_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    show_inactive: bool = Query(False),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    query = db.query(SpareItem)
    if not show_inactive:
        query = query.filter(SpareItem.is_active == True)
    if type_id:
        query = query.filter(SpareItem.type_id == type_id)
    if category_id:
        query = query.filter(SpareItem.category_id == category_id)
    if search:
        query = query.filter(
            SpareItem.name.ilike(f"%{search}%") | SpareItem.sku.ilike(f"%{search}%")
        )
    total = query.count()
    per_page = 20
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    result = []
    for item in items:
        type_obj = db.query(ItemType).filter(ItemType.id == item.type_id).first()
        cat_obj = db.query(ItemCategory).filter(ItemCategory.id == item.category_id).first()
        result.append({
            "id": item.id, "sku": item.sku, "name": item.name,
            "type_id": item.type_id, "type_name": type_obj.name if type_obj else None,
            "category_id": item.category_id, "category_name": cat_obj.name if cat_obj else None,
            "unit": item.unit, "requires_serial": item.requires_serial,
            "min_stock": item.min_stock, "catatan": item.catatan,
            "is_active": item.is_active,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
        })
    return {"success": True, "message": "Berhasil", "data": result,
            "pagination": {"total": total, "page": page, "per_page": per_page,
                           "total_pages": (total + per_page - 1) // per_page}}


@router.post("/spare", status_code=201)
def create_spare_item(
    body: SpareItemCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    existing = db.query(SpareItem).filter(SpareItem.sku == body.sku).first()
    if existing:
        raise HTTPException(status_code=409, detail=E.MASTER_SKU_DUPLICATE)

    item = SpareItem(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"SpareItem dibuat | action=tambah entity=spare_item sku={item.sku} user_id={admin.id}")
    return {"success": True, "message": "Spare item berhasil dibuat", "data": {"id": item.id, "sku": item.sku}}


@router.put("/spare/{item_id}")
def update_spare_item(
    item_id: int,
    body: SpareItemUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    item = db.query(SpareItem).filter(SpareItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    logger.info(f"SpareItem diupdate | action=edit entity=spare_item id={item_id} user_id={admin.id}")
    return {"success": True, "message": "Spare item berhasil diperbarui", "data": {"id": item.id}}


@router.patch("/spare/{item_id}/toggle-active")
def toggle_spare_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    item = db.query(SpareItem).filter(SpareItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=E.MASTER_NOT_FOUND)

    if item.is_active:
        sp_with_stock = db.query(Stock).filter(
            Stock.spare_item_id == item_id, Stock.qty > 0
        ).count()
        if sp_with_stock > 0:
            raise HTTPException(status_code=400,
                                detail=E.MASTER_ITEM_HAS_STOCK.format(n=sp_with_stock))

    item.is_active = not item.is_active
    db.commit()
    status_msg = "diaktifkan" if item.is_active else "dinonaktifkan"
    logger.info(f"SpareItem {status_msg} | id={item_id} user_id={admin.id}")
    return {"success": True, "message": f"Spare item berhasil {status_msg}", "data": None}
