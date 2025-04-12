from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class MovementEvent(BaseModel):
    movement_id: UUID
    warehouse_id: str
    timestamp: datetime
    event: str
    product_id: str
    quantity: int


class MovementRecord(BaseModel):
    arrival: Optional[MovementEvent] = None
    departure: Optional[MovementEvent] = None


class MovementResponse(BaseModel):
    movement_id: UUID
    product_id: str
    departure: Optional[MovementEvent]
    arrival: Optional[MovementEvent]
    time_diff_seconds: Optional[int]
    quantity_diff: Optional[int]


class InventoryResponse(BaseModel):
    warehouse_id: str
    product_id: str
    quantity: int
