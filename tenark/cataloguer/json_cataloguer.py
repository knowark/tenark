import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..common import (
    QueryParser, QueryDomain, TenantCatalogError, TenantRetrievalError)
from ..models import Tenant
from .cataloguer import Cataloguer


class JsonCataloguer(Cataloguer):

    def __init__(self, path: str, parser: QueryParser = None) -> None:
        self.path = path
        self.parser = parser or QueryParser()
        self.catalog: Dict[str, Tenant] = {}
        self.collection = 'tenants'
        self.catalog_schema: Dict = {
            self.collection: {}
        }
        self._setup()

    def _setup(self) -> None:
        catalog_file = Path(self.path)

        if not catalog_file.exists():
            with catalog_file.open('w') as f:
                json.dump(self.catalog_schema, f, indent=2)
            return

        loaded = self._load()
        if loaded:
            return

        with catalog_file.open('w') as f:
            json.dump(self.catalog_schema, f, indent=2)

    def _load(self) -> bool:
        catalog_file = Path(self.path)
        with catalog_file.open('r') as f:
            try:
                data = json.load(f)
                if self.collection in data:
                    for key, value in data[self.collection].items():
                        self.catalog[key] = Tenant(**value)
                    return True
            except json.JSONDecodeError as e:
                pass

        return False

    def add_tenant(self, tenant: Tenant) -> Tenant:
        path = Path(self.path)
        data = {'tenants': dict(self.catalog)}
        data[self.collection].update({tenant.id: vars(tenant)})
        with path.open('w') as f:
            json.dump(data, f, indent=2)

        self._load()

        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        tenant = self.catalog.get(tenant_id)
        if not tenant:
            raise TenantRetrievalError(
                f"The entity with id {tenant_id} was not found.")
        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        tenants = []
        filter_function = self.parser.parse(domain)
        for tenant in self.catalog.values():
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
