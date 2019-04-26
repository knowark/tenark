import json
from pathlib import Path
from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..common import (
    QueryParser, QueryDomain, TenantCatalogError, TenantRetrievalError)
from ..models import Tenant
from .cataloguer import Cataloguer


class JsonCataloguer(Cataloguer):

    def __init__(self, path: str, parser: QueryParser) -> None:
        self.path = path
        self.parser = parser
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

        with catalog_file.open('r+') as f:
            try:
                data = json.load(f)
                if self.collection in data:
                    return
            except json.JSONDecodeError as e:
                pass

            json.dump(self.catalog_schema, f, indent=2)

    def add_tenant(self, tenant: Tenant) -> Tenant:
        path = Path(self.path)
        with path.open() as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise TenantCatalogError(
                    f"The tenant catalog file <${self.path}> "
                    "is not valid json.")

        tenant.id = tenant.id or str(uuid4())

        data[self.collection].update({tenant.id: vars(tenant)})
        with path.open('w') as f:
            json.dump(data, f, indent=2)

        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        with open(self.path) as f:
            data = json.load(f)
            tenants = data.get(self.collection, {})
            tenant_dict = tenants.get(tenant_id)
            if not tenant_dict:
                raise TenantRetrievalError(
                    f"The entity with id {tenant_id} was not found.")
            return Tenant(**tenant_dict)

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        with open(self.path, 'r') as f:
            data = json.load(f)
            tenants_dict = data.get(self.collection, {})

        tenants = []
        filter_function = self.parser.parse(domain)
        for tenant_dict in tenants_dict.values():
            tenant = Tenant(**tenant_dict)

            if filter_function(tenant):
                tenants.append(tenant)

        return tenants
