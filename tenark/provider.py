from typing import List, Dict, Any
from .common import QueryDomain, TenantRetrievalError
from .cataloguer import Cataloguer


class Provider:

    def __init__(self, cataloguer: Cataloguer) -> None:
        self.cataloguer = cataloguer

    def get_tenant(self, tenant_id: str) -> Dict[str, Any]:
        tenant = self.cataloguer.get_tenant(tenant_id)
        return vars(tenant)

    def search_tenants(self, domain: QueryDomain) -> List[Dict[str, Any]]:
        return [vars(tenant) for tenant in sorted(
            self.cataloguer.search_tenants(domain),
            key=lambda x: x.name)]

    def resolve_tenant(self, name: str) -> Dict[str, Any]:
        domain: QueryDomain = ['|', ('slug', '=', name),
                               ('name', '=', name)]
        entities = self.cataloguer.search_tenants(domain)
        if not entities:
            raise TenantRetrievalError("Tenant not found.")

        tenant = entities.pop()
        return vars(tenant)
