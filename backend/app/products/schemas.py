import uuid
from typing import Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None


class ProductRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    price: float
    category: Optional[str]
    is_available: bool

    model_config = {"from_attributes": True}