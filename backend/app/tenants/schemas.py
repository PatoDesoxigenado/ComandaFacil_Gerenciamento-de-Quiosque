import re
from pydantic import BaseModel, field_validator, EmailStr
import uuid
from datetime import datetime


SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


class TenantCreate(BaseModel):
    name: str
    slug: str
    admin_email: EmailStr
    admin_password: str

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        v = v.lower().strip()
        if len(v) < 3:
            raise ValueError("Slug deve ter no minimo 3 caracteres")
        reserved = {"www", "api", "admin", "app"}
        if v in reserved:
            raise ValueError(f"Slug '{v}' e reservado")
        if not SLUG_PATTERN.match(v):
            raise ValueError("Slug deve conter apenas letras minusculas, numeros e hifens, sem comecar ou terminar com hifen")
        return v

    @field_validator("admin_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Senha deve ter no minimo 6 caracteres")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter no minimo 2 caracteres")
        return v


class TenantRead(BaseModel):
    id: uuid.UUID
    slug: str
    name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}