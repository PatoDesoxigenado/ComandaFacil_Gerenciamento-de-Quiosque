from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.tenants.models import Tenant
from app.tenants.schemas import TenantCreate
from app.core.security import hash_password


async def get_tenant_by_slug(session: AsyncSession, slug: str):
    result = await session.execute(select(Tenant).where(Tenant.slug == slug))
    return result.scalar_one_or_none()


async def create_tenant(session: AsyncSession, data: TenantCreate) -> Tenant:
    schema_name = f"tenant_{data.slug}"

    tenant = Tenant(
        slug=data.slug,
        name=data.name,
        schema_name=schema_name,
    )
    session.add(tenant)
    await session.flush()

    await _create_schema(session, schema_name, data)
    await session.commit()
    await session.refresh(tenant)
    return tenant


async def _create_schema(session: AsyncSession, schema_name: str, data: TenantCreate):
    await session.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))

    await session.execute(text(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            full_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role VARCHAR(50) DEFAULT 'waiter',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """))

    await session.execute(text(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".tables (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            number INTEGER NOT NULL,
            seats INTEGER DEFAULT 4,
            is_occupied BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """))

    await session.execute(text(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".products (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price NUMERIC(10,2) NOT NULL,
            category VARCHAR(100),
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """))

    await session.execute(text(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".orders (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            table_id UUID NOT NULL,
            user_id UUID NOT NULL,
            status VARCHAR(50) DEFAULT 'open',
            total NUMERIC(10,2) DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        )
    """))

    await session.execute(text(f"""
        CREATE TABLE IF NOT EXISTS "{schema_name}".order_items (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            order_id UUID REFERENCES "{schema_name}".orders(id) ON DELETE CASCADE,
            product_id UUID NOT NULL,
            quantity INTEGER DEFAULT 1,
            unit_price NUMERIC(10,2) NOT NULL
        )
    """))

    # Cria o admin inicial do tenant
    hashed = hash_password(data.admin_password)
    await session.execute(text(f"""
        INSERT INTO "{schema_name}".users (full_name, email, hashed_password, role)
        VALUES ('Admin', :email, :password, 'admin')
        ON CONFLICT (email) DO NOTHING
    """), {"email": data.admin_email, "password": hashed})