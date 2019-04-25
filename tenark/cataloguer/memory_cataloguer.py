from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..common import QueryParser, QueryDomain
from ..models import Tenant
from .cataloguer import Cataloguer


class MemoryCataloguer(Cataloguer):

    def __init__(self, parser: QueryParser) -> None:
        self.catalog: Optional[Dict] = None
        self.parser = parser

    def setup(self) -> bool:
        self.catalog = {}
        return True

    def add_tenant(self, tenant: Tenant) -> Tenant:
        tenant.id = tenant.id or str(uuid4())
        if self.catalog is None:
            raise ValueError("Setup the tenant catalog first.")
        self.catalog[tenant.id] = tenant
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        if self.catalog is None:
            raise ValueError("Setup the tenant catalog first.")

        tenant = self.catalog.get(tenant_id)

        if not tenant:
            raise ValueError('Tenant not found.')

        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        tenants = []
        filter_function = self.parser.parse(domain)
        if self.catalog is None:
            raise ValueError("Setup the tenant catalog first.")
        for tenant in list(self.catalog.values()):
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
