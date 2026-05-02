from pydantic import BaseModel, EmailStr, field_validator
import re


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
    name: str
    force_password_change: bool


class RefreshRequest(BaseModel):
    pass  # Refresh token diambil dari httpOnly cookie


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password minimal 8 karakter, mengandung huruf besar dan angka.")
        return v


class MeResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    service_point_id: int | None
    force_password_change: bool
    is_active: bool

    class Config:
        from_attributes = True
