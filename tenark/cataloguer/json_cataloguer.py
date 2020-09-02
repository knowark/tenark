import json
from pathlib import Path
from typing import List, Dict, Any
from ..common import (
    QueryParser, QueryDomain, TenantRetrievalError)
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

    def load(self, cache: bool = True) -> None:
        catalog_file = Path(self.path)
        with catalog_file.open('r') as f:
            try:
                data = json.load(f)
                if self.collection in data:
                    for key, value in data[self.collection].items():
                        self.catalog[key] = Tenant(**value)
            except json.JSONDecodeError as e:
                pass

    def add_tenant(self, tenant: Tenant) -> Tenant:
        data: Dict[str, Any] = {self.collection: {}}
        catalog_file = Path(self.path)
        with catalog_file.open('r') as f:
            data = json.load(f)

        data[self.collection].update({tenant.id: vars(tenant)})

        with catalog_file.open('w') as f:
            json.dump(data, f, indent=2)

        self.load(False)

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

    def _setup(self) -> None:
        catalog_file = Path(self.path)

        if not catalog_file.exists():
            with catalog_file.open('w') as f:
                json.dump(self.catalog_schema, f, indent=2)
            return

        self.load()

        with catalog_file.open('w') as f:
            json.dump(self.catalog_schema, f, indent=2)
