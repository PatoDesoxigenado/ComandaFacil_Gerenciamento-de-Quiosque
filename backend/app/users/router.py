import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_tenant_db
from app.users.models import User
from app.users import service
from app.users.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_tenant_db)):
    return await service.list_users(db)


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_tenant_db)):
    existing = await service.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email ja cadastrado")
    return await service.create_user(db, data)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_tenant_db),
):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return await service.update_user(db, user, data)