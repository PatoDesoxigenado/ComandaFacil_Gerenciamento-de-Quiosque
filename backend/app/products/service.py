from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductUpdate


async def list_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(select(Product).where(Product.is_available == True))
    return list(result.scalars().all())


async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(db: AsyncSession, product: Product, data: ProductUpdate) -> Product:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product