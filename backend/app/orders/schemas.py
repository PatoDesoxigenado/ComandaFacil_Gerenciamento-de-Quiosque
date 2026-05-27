import uuid
from typing import Optional
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: uuid.UUID
    quantity: int = 1


class OrderItemRead(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    table_id: uuid.UUID
    user_id: uuid.UUID
    items: list[OrderItemCreate]



class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderRead(BaseModel):
    id: uuid.UUID
    table_id: uuid.UUID
    user_id: uuid.UUID
    status: str
    total: float
    items: list[OrderItemRead] = []

    model_config = {"from_attributes": True}