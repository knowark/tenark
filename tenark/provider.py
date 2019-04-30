from typing import Dict, Any
from .common import QueryDomain, TenantRetrievalError
from .models import Tenant
from .cataloguer import Cataloguer


class Provider:

    def __init__(self, cataloguer: Cataloguer) -> None:
        self.cataloguer = cataloguer

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        tenant = self.cataloguer.get_tenant(tenant_id)
        return vars(tenant)

    def resolve_tenant(self, name: str) -> Dict[str, Any]:
        domain: QueryDomain = ['|', ('slug', '=', name),
                               ('name', '=', name)]
        entities = self.cataloguer.search_tenants(domain)
        if not entities:
            raise TenantRetrievalError("Tenant not found.")

        tenant = entities.pop()
        return vars(tenant)
