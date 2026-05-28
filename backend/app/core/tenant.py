from dataclasses import dataclass


@dataclass
class TenantContext:
    tenant_id: str
    schema: str
    slug: str