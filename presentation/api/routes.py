from fastapi import APIRouter, HTTPException
from uuid import UUID
from domain.models import MovementResponse, InventoryResponse
from usecases.movement_service import get_movement_by_id, get_product_quantity

router = APIRouter()


@router.get(
    "/api/movements/{movement_id}",
    tags=["Движение товара"],
    summary='Получить данные о перемещении',
    response_model=MovementResponse
)
async def get_movement(movement_id: UUID):
    record = await get_movement_by_id(movement_id)
    if not record:
        raise HTTPException(status_code=404, detail="Movement not found")

    dep = record.departure.dict() if record.departure else None
    arr = record.arrival.dict() if record.arrival else None

    time_diff = None
    qty_diff = None

    if dep and arr:
        t1 = record.departure.timestamp
        t2 = record.arrival.timestamp
        time_diff = int((t2 - t1).total_seconds())
        qty_diff = record.arrival.quantity - record.departure.quantity

    return MovementResponse(
        movement_id=movement_id,
        product_id=record.departure.product_id if record.departure else record.arrival.product_id,
        departure=dep,
        arrival=arr,
        time_diff_seconds=time_diff,
        quantity_diff=qty_diff
    )


@router.get(
    "/api/warehouses/{warehouse_id}/products/{product_id}",
    tags=["Склад"],
    summary='Данные о товаре на складе',
    response_model=InventoryResponse
)
async def get_inventory(warehouse_id: str, product_id: str):
    qty = await get_product_quantity(warehouse_id, product_id)
    return InventoryResponse(
        warehouse_id=warehouse_id,
        product_id=product_id,
        quantity=qty
    )
