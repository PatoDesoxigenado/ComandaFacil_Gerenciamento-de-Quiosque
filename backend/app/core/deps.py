from fastapi import Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import AsyncSessionFactory

async def get_tenant_db(request: Request):
    tenant = getattr(request.state, "tenant", None)
    if tenant is None:
        raise HTTPException(status_code=400, detail="Tenant nao identificado")

    async with AsyncSessionFactory() as session:
        await session.execute(text(f"SET search_path TO {tenant.schema}, public"))
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise