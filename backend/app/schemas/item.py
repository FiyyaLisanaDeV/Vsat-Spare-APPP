from typing import Optional
from pydantic import BaseModel


# ─── Item Type ────────────────────────────────────────────────────────────────

class ItemTypeCreate(BaseModel):
    name: str


class ItemTypeUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class ItemTypeResponse(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: str

    class Config:
        from_attributes = True


# ─── Item Category ────────────────────────────────────────────────────────────

class ItemCategoryCreate(BaseModel):
    type_id: int
    name: str


class ItemCategoryUpdate(BaseModel):
    name: Optional[str] = None
    type_id: Optional[int] = None
    is_active: Optional[bool] = None


class ItemCategoryResponse(BaseModel):
    id: int
    type_id: int
    name: str
    is_active: bool
    created_at: str
    type_name: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Spare Item ───────────────────────────────────────────────────────────────

class SpareItemCreate(BaseModel):
    sku: str
    name: str
    type_id: int
    category_id: int
    unit: str
    requires_serial: bool = False
    min_stock: int = 0
    catatan: Optional[str] = None


class SpareItemUpdate(BaseModel):
    name: Optional[str] = None
    type_id: Optional[int] = None
    category_id: Optional[int] = None
    unit: Optional[str] = None
    requires_serial: Optional[bool] = None
    min_stock: Optional[int] = None
    catatan: Optional[str] = None
    is_active: Optional[bool] = None


class SpareItemResponse(BaseModel):
    id: int
    sku: str
    name: str
    type_id: int
    category_id: int
    unit: str
    requires_serial: bool
    min_stock: int
    catatan: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str
    type_name: Optional[str] = None
    category_name: Optional[str] = None

    class Config:
        from_attributes = True
