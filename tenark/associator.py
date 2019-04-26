from typing import Dict, Any
from .common import QueryDomain, TenantRetrievalError
from .cataloguer import Cataloguer
from .provider import Provider


class Associator:

    def __init__(self, cataloguer: Cataloguer,
                 provider: Provider) -> None:
        self.cataloguer = cataloguer
        self.provider = provider

    def establish_tenant(self, tenant_id: str) -> None:
        tenant = self.cataloguer.get_tenant(tenant_id)
        self.provider.setup(tenant)

    def resolve_tenant(self, tenant: str) -> None:
        domain: QueryDomain = ['|', ('slug', '=', tenant),
                               ('name', '=', tenant)]
        entities = self.cataloguer.search_tenants(domain)
        if not entities:
            raise TenantRetrievalError("Tenant not found.")

        for entity in entities:
            self.provider.setup(entity)

    def get_current_tenant(self) -> Dict[str, Any]:
        current = self.provider.get_tenant()
        return vars(current)
