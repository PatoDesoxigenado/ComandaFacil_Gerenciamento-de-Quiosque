from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.tenants.models import Tenant

router = APIRouter(prefix="/auth", tags=["Auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Busca o tenant pelo email do usuario
    result = await db.execute(select(Tenant).where(Tenant.is_active == True))
    tenants = result.scalars().all()

    user = None
    tenant = None

    for t in tenants:
        schema = t.schema_name
        user_result = await db.execute(
            text(f'SELECT id, email, hashed_password, role FROM "{schema}".users WHERE email = :email AND is_active = TRUE'),
            {"email": form_data.username},
        )
        found = user_result.mappings().one_or_none()
        if found:
            user = found
            tenant = t
            break

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = create_access_token({
        "sub": str(user["id"]),
        "tenant_id": str(tenant.id),
        "tenant_slug": tenant.slug,
        "role": user["role"],
    })

    return TokenResponse(access_token=token)