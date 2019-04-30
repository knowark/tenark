from typing import Dict, Any
from .common import QueryDomain, TenantRetrievalError
from .models import Tenant
from .cataloguer import Cataloguer


class Provider:

    def __init__(self, cataloguer: Cataloguer) -> None:
        self.cataloguer = cataloguer

    def get_tenant(self, tenant_id: str) -> Tenant:
        return self.cataloguer.get_tenant(tenant_id)

    def resolve_tenant(self, tenant: str) -> Tenant:
        domain: QueryDomain = ['|', ('slug', '=', tenant),
                               ('name', '=', tenant)]
        entities = self.cataloguer.search_tenants(domain)
        if not entities:
            raise TenantRetrievalError("Tenant not found.")

        return entities.pop()
