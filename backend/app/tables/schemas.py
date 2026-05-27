import uuid
from pydantic import BaseModel

class TableCreate(BaseModel):
    number: int
    seats: int = 4

class TableUpdate(BaseModel):
    seats: int | None = None
    is_occupied: bool | None = None

class TableRead(BaseModel):
    id: uuid.UUID
    number: int
    seats: int
    is_occupied: bool

    model_config = {"from_attributes": True}