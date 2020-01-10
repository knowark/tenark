import json
import psycopg2
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..common import (
    QueryParser, QueryDomain, TenantCatalogError, TenantRetrievalError)
from ..models import Tenant
from .cataloguer import Cataloguer


class SchemaCataloguer(Cataloguer):

    def __init__(self, dsn: str, schema: str ='public',
                 table: str = '__tenants__',
                 parser: QueryParser = None) -> None:
        self.dsn = dsn
        self.schema = schema
        self.table = table
        self.parser = parser or QueryParser()
        self.catalog: Dict[str, Tenant] = {}
        self._setup()

    def _setup(self) -> None:
        with psycopg2.connect(self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    f'CREATE SCHEMA IF NOT EXISTS {self.schema}')
                cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.schema}.{self.table} ("
                    "data JSONB)")
                cursor.execute(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS pk_{self.table}_id ON "
                    f"{self.schema}.{self.table} ((data ->> 'id'));")

        self._load()

    def _load(self) -> bool:
        query = f"SELECT data FROM {self.schema}.{self.table}"
        with psycopg2.connect(self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        for row in result:
            data, *_ = row
            self.catalog[data['id']] = Tenant(**data)

        return True

    def add_tenant(self, tenant: Tenant) -> Tenant:
        data = json.dumps(vars(tenant))
        query = f"INSERT INTO {self.schema}.{self.table} (data) VALUES (%s);"
        parameters = (data,)

        with psycopg2.connect(self.dsn) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)

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
