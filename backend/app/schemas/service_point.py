from typing import Optional
from pydantic import BaseModel, EmailStr


class ServicePointCreate(BaseModel):
    name: str
    type: str
    city: str
    province: str
    pic_name: str
    pic_phone: str
    pic_email: Optional[EmailStr] = None

    class Config:
        use_enum_values = True


class ServicePointUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    pic_name: Optional[str] = None
    pic_phone: Optional[str] = None
    pic_email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class ServicePointResponse(BaseModel):
    id: int
    name: str
    type: str
    city: str
    province: str
    pic_name: str
    pic_phone: str
    pic_email: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
