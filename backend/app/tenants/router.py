from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.tenants import service
from app.tenants.schemas import TenantCreate, TenantRead

router = APIRouter(prefix="/tenants", tags=["Tenants"])


@router.post("/", response_model=TenantRead, status_code=201)
async def create_tenant(data: TenantCreate, db: AsyncSession = Depends(get_db)):
    existing = await service.get_tenant_by_slug(db, data.slug)
    if existing:
        raise HTTPException(status_code=409, detail="Slug ja em uso")
    return await service.create_tenant(db, data)