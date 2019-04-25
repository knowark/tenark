from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..common import QueryParser, QueryDomain, TenantRetrievalError
from ..models import Tenant
from .cataloguer import Cataloguer


class MemoryCataloguer(Cataloguer):

    def __init__(self, parser: QueryParser) -> None:
        self.parser = parser
        self.catalog: Dict[str, Tenant] = {}

    def add_tenant(self, tenant: Tenant) -> Tenant:
        tenant.id = tenant.id or str(uuid4())
        self.catalog[tenant.id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        tenant = self.catalog.get(tenant_id)

        if not tenant:
            raise TenantRetrievalError('Tenant not found.')

        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        tenants = []
        filter_function = self.parser.parse(domain)
        for tenant in self.catalog.values():
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
