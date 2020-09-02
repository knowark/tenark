import json
import time
from typing import Sequence, List, Dict, Protocol, Optional, Any
from ..common import (
    QueryParser, QueryDomain, TenantRetrievalError)
from ..models import Tenant
from .cataloguer import Cataloguer


class SchemaConnection(Protocol):
    def open(self) -> None:
        """Open the database connection"""

    def close(self) -> None:
        """Close the database connection"""

    def execute(self, statement: str,
                parameters: Sequence[Any] = []) -> str:
        """Execute data modification commands"""

    def select(self, statement: str,
               parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
        """Select data from the database"""


class SchemaCataloguer(Cataloguer):
    def __init__(self, connection: SchemaConnection,
                 lifespan: Optional[int] = 3600,
                 schema: str = 'public',
                 table: str = '__tenants__',
                 parser: QueryParser = None,
                 placeholder: str = '%s',
                 offset=1) -> None:
        self.connection = connection
        self.schema = schema
        self.table = table
        self.parser = parser or QueryParser()
        self.placeholder = placeholder
        self.offset = offset
        self.catalog: Dict[str, Tenant] = {}
        self.cache: Optional[int] = None
        self.lifespan = 3600.0
        self.expiration = 0.0
        self._setup()

    def load(self, cache=True) -> None:
        now = time.time()
        if cache and self.lifespan and now < self.expiration:
            return

        self.expiration = now + self.lifespan
        self.connection.open()
        query = f"SELECT data FROM {self.schema}.{self.table};"
        result = self.connection.select(query)
        for record in result:
            self.catalog[record['id']] = Tenant(**record)
        self.connection.close()

    def add_tenant(self, tenant: Tenant) -> Tenant:
        self.connection.open()
        data = json.dumps(vars(tenant))
        index = self.offset
        placeholders = self.placeholder.format(index=index)
        query = (f"INSERT INTO {self.schema}.{self.table} "
                 f"(data) VALUES ({placeholders});")
        parameters = (data,)

        self.connection.execute(query, parameters)
        self.connection.close()
        self.load(False)

        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant:
        self.load()
        tenant = self.catalog.get(tenant_id)
        if not tenant:
            raise TenantRetrievalError(
                f"The entity with id {tenant_id} was not found.")
        return tenant

    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        self.load()
        tenants = []
        filter_function = self.parser.parse(domain)
        for tenant in self.catalog.values():
            if filter_function(tenant):
                tenants.append(tenant)

        return tenants

    def _setup(self) -> None:
        self.connection.open()
        self.connection.execute(
            f"CREATE SCHEMA IF NOT EXISTS {self.schema}; "
            f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.table} ("
            "data JSONB); "
            f"CREATE UNIQUE INDEX IF NOT EXISTS pk_{self.table}_id ON "
            f"{self.schema}.{self.table} ((data ->> 'id'));")
        self.connection.close()
