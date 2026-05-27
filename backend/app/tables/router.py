from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_tenant_db
from app.tables import service
from app.tables.schemas import TableCreate, TableRead, TableUpdate

router = APIRouter(prefix="/tables", tags=["Tables"])

@router.get("/", response_model=list[TableRead])
async def list_tables(db: AsyncSession = Depends(get_tenant_db)):
    return await service.list_tables(db)

@router.post("/", response_model=TableRead, status_code=201)
async def create_table(data: TableCreate, db: AsyncSession = Depends(get_tenant_db)):
    return await service.create_table(db, data)

@router.patch("/{table_id}", response_model=TableRead)
async def update_table(
    table_id: str,
    data: TableUpdate,
    db: AsyncSession = Depends(get_tenant_db),
):
    table = await db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Mesa nao encontrada")
    return await service.update_table(db, table, data)