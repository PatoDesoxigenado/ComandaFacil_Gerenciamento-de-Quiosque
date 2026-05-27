from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.orders.models import Order, OrderItem
from app.orders.schemas import OrderCreate, OrderUpdate
from app.products.models import Product


async def list_orders(db: AsyncSession) -> list[Order]:
    result = await db.execute(
        select(Order).options(selectinload(Order.items))
    )
    return list(result.scalars().all())


async def get_order(db: AsyncSession, order_id: str) -> Order | None:
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    return result.scalar_one_or_none()


async def create_order(db: AsyncSession, data: OrderCreate) -> Order:
    order = Order(
        table_id=data.table_id,
        user_id=data.user_id,
    )
    db.add(order)
    await db.flush()  # gera o id do pedido

    total = 0.0
    for item_data in data.items:
        product = await db.get(Product, item_data.product_id)
        if not product:
            raise ValueError(f"Produto {item_data.product_id} nao encontrado")

        unit_price = float(product.price)
        total += unit_price * item_data.quantity

        item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=unit_price,
        )
        db.add(item)

    order.total = total
    await db.commit()
    await db.refresh(order)
    return order


async def update_order(db: AsyncSession, order: Order, data: OrderUpdate) -> Order:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(order, field, value)
    await db.commit()
    await db.refresh(order)
    return order