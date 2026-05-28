from dataclasses import dataclass
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.database import AsyncSessionFactory
from app.core.settings import get_settings

settings = get_settings()

@dataclass
class TenantContext:
    tenant_id: str
    schema: str
    slug: str

class TenantMiddleware(BaseHTTPMiddleware):
    EXEMPT_PATHS = {"/health", "/docs", "/redoc", "/openapi.json", "/api/v1/tenants/"}

    async def dispatch(self, request, call_next) -> Response:
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        slug = self._extract_slug(request)
        if slug is None:
            return await call_next(request)

        tenant = await self._resolve_tenant(slug)
        if tenant is None:
            raise HTTPException(status_code=404, detail=f"Tenant '{slug}' nao encontrado")

        request.state.tenant = TenantContext(
            tenant_id=tenant["id"],
            schema=f"tenant_{slug}",
            slug=slug,
        )
        return await call_next(request)

    def _extract_slug(self, request) -> str | None:
        host = request.headers.get("host", "").split(":")[0]
        parts = host.split(".")
        base_parts = settings.APP_BASE_DOMAIN.split(".")
        if len(parts) > len(base_parts):
            slug = parts[0]
            if slug not in ("www", "api", "admin"):
                return slug
        return None

    async def _resolve_tenant(self, slug: str) -> dict | None:
        from sqlalchemy import text
        async with AsyncSessionFactory() as session:
            result = await session.execute(
                text("SELECT id, slug FROM tenants WHERE slug = :slug AND is_active = TRUE"),
                {"slug": slug},
            )
            row = result.mappings().one_or_none()
            return dict(row) if row else None