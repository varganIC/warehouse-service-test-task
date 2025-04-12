from domain.models import MovementEvent, MovementRecord
from typing import Dict, Optional
from uuid import UUID
from collections import defaultdict

movements: Dict[UUID, MovementRecord] = {}
warehouse_inventory: Dict[str, Dict[str, int]] = defaultdict(dict)


async def register_movement(event: MovementEvent):
    record = movements.setdefault(event.movement_id, MovementRecord())

    if event.event == "arrival":
        record.arrival = event
        warehouse_inventory[event.warehouse_id][event.product_id] = (
            warehouse_inventory[event.warehouse_id].get(event.product_id, 0)
            + event.quantity
        )

    elif event.event == "departure":
        record.departure = event
        current = warehouse_inventory[event.warehouse_id].get(event.product_id, 0)
        if current >= event.quantity:
            warehouse_inventory[event.warehouse_id][event.product_id] = (
                    current - event.quantity
            )


async def get_movement_by_id(movement_id: UUID) -> Optional[MovementRecord]:
    return movements.get(movement_id)


async def get_product_quantity(warehouse_id: str, product_id: str) -> int:
    return warehouse_inventory[warehouse_id].get(product_id, 0)
