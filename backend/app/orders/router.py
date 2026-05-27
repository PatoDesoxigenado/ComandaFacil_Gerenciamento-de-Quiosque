import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_tenant_db
from app.orders import service
from app.orders.schemas import OrderCreate, OrderRead, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderRead])
async def list_orders(db: AsyncSession = Depends(get_tenant_db)):
    return await service.list_orders(db)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(order_id: uuid.UUID, db: AsyncSession = Depends(get_tenant_db)):
    order = await service.get_order(db, str(order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    return order


@router.post("/", response_model=OrderRead, status_code=201)
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_tenant_db)):
    try:
        return await service.create_order(db, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: uuid.UUID,
    data: OrderUpdate,
    db: AsyncSession = Depends(get_tenant_db),
):
    from app.orders.models import Order
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido nao encontrado")
    return await service.update_order(db, order, data)