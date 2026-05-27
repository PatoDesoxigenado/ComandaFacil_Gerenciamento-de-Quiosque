from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine, Base
from app.core.tenant import TenantMiddleware
from app.api.v1.router import api_router
from app.tenants.models import Tenant


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="ComandaFacil API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(TenantMiddleware)

app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok"}