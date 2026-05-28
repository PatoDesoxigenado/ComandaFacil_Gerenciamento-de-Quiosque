from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import AsyncSessionFactory
from app.core.security import decode_token
from app.core.tenant import TenantContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_tenant(token: str = Depends(oauth2_scheme)) -> TenantContext:
    token_data = decode_token(token)
    return TenantContext(
        tenant_id=token_data.tenant_id,
        schema=f"tenant_{token_data.tenant_slug}",
        slug=token_data.tenant_slug,
    )


async def get_tenant_db(tenant: TenantContext = Depends(get_current_tenant)):
    async with AsyncSessionFactory() as session:
        await session.execute(text(f"SET search_path TO {tenant.schema}, public"))
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise