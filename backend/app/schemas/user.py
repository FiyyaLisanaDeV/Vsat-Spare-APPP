from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
import re


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
    service_point_id: Optional[int] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ("admin_jakarta", "user_sp"):
            raise ValueError("Role tidak valid.")
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    service_point_id: Optional[int] = None
    is_active: Optional[bool] = None
    force_password_change: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    service_point_id: Optional[int]
    is_active: bool
    force_password_change: bool
    last_login: Optional[str] = None
    created_at: str
    service_point_name: Optional[str] = None

    class Config:
        from_attributes = True
