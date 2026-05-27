from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.tables.models import Table
from app.tables.schemas import TableCreate, TableUpdate

async def list_tables(db: AsyncSession) -> list[Table]:
    result = await db.execute(select(Table))
    return list(result.scalars().all())

async def create_table(db: AsyncSession, data: TableCreate) -> Table:
    table = Table(**data.model_dump())
    db.add(table)
    await db.commit()
    await db.refresh(table)
    return table

async def update_table(db: AsyncSession, table: Table, data: TableUpdate) -> Table:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(table, field, value)
    await db.commit()
    await db.refresh(table)
    return table