import json
from types import MethodType
from typing import Sequence, List, Dict, Any
from pytest import fixture, raises
from tenark.common import (
    QueryParser, TenantRetrievalError)
from tenark.models import Tenant
from tenark.cataloguer import SchemaCataloguer


@fixture
def connection():
    class MockConnection:
        def __init__(self) -> None:
            self._opened = []
            self._closed = []
            self._execute_statement = ''
            self._execute_parameters = None

        def open(self) -> None:
            self._opened.append(True)

        def close(self) -> None:
            self._closed.append(True)

        def execute(self, statement: str,
                    parameters: Sequence[Any] = [PermissionError]) -> str:
            self._execute_statement = statement
            self._execute_parameters = parameters
            return statement

        def select(self, statement: str,
                   parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
            self._select_statement = statement
            self._select_parameters = parameters
            return []

    return MockConnection()


@fixture
def loaded_connection(connection):
    def loaded_select(self, statement: str,
                      parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
        self._select_statement = statement
        self._select_parameters = parameters
        tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
        tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'
        return [
            {'id': tenant_2_id, 'name': 'Google'},
            {'id': tenant_1_id, 'name': 'Amazon'}
        ]

    connection.select = MethodType(loaded_select, connection)

    return connection


@fixture
def cataloguer(connection) -> SchemaCataloguer:
    cataloguer = SchemaCataloguer(connection)

    return cataloguer


@fixture
def loaded_cataloguer(cataloguer) -> SchemaCataloguer:
    tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
    tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'

    cataloguer.catalog = {
        tenant_1_id: Tenant(**{
            'id': tenant_1_id,
            'name': 'Amazon'
        }),
        tenant_2_id: Tenant(**{
            'id': tenant_2_id,
            'name': 'Google'
        })
    }

    return cataloguer


def test_schema_connection(connection):
    connection = connection
    assert hasattr(connection, 'open')
    assert hasattr(connection, 'close')
    assert hasattr(connection, 'execute')
    assert hasattr(connection, 'select')


def test_schema_cataloguer_initialization(cataloguer):
    assert cataloguer.schema == 'public'
    assert cataloguer.table == '__tenants__'
    assert isinstance(cataloguer.parser, QueryParser)
    assert cataloguer.connection._execute_statement == (
        "CREATE SCHEMA IF NOT EXISTS public; "
        "CREATE TABLE IF NOT EXISTS public.__tenants__ (data JSONB); "
        "CREATE UNIQUE INDEX IF NOT EXISTS "
        "pk___tenants___id ON public.__tenants__ ((data ->> 'id'));"
    )


def test_schema_cataloguer_add_tenant(cataloguer):
    tenant_id = 'ec002b8d-30eb-447a-ac5b-be966763723b'
    tenant = Tenant(
        id=tenant_id,
        name='Microsoft')
    tenant = cataloguer.add_tenant(tenant)

    assert cataloguer.connection._opened == [True, True, True]
    assert cataloguer.connection._closed == [True, True, True]

    assert cataloguer.connection._execute_statement == (
        'INSERT INTO public.__tenants__ (data) VALUES ($1);')
    tenant_json = next(iter(cataloguer.connection._execute_parameters))
    tenant_dict = json.loads(tenant_json)

    assert len(tenant_dict['id']) == 36
    assert tenant_dict['name'] == 'Microsoft'


def test_schema_cataloguer_get_tenant(loaded_cataloguer):
    tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
    tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'

    tenant_2 = loaded_cataloguer.get_tenant(tenant_2_id)
    assert tenant_2.name == 'Google'

    tenant_1 = loaded_cataloguer.get_tenant(tenant_1_id)
    assert tenant_1.name == 'Amazon'

    assert loaded_cataloguer.connection._opened == [True, True]
    assert loaded_cataloguer.connection._closed == [True, True]


def test_schema_cataloguer_get_tenant_cached(loaded_cataloguer):
    loaded_cataloguer.expiration = 9999999999
    tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
    tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'

    tenant_2 = loaded_cataloguer.get_tenant(tenant_2_id)
    assert tenant_2.name == 'Google'

    tenant_1 = loaded_cataloguer.get_tenant(tenant_1_id)
    assert tenant_1.name == 'Amazon'

    assert loaded_cataloguer.connection._opened == [True]
    assert loaded_cataloguer.connection._closed == [True]


def test_schema_cataloguer_get_tenant_not_found(loaded_cataloguer):
    with raises(TenantRetrievalError):
        loaded_cataloguer.get_tenant('004')


def test_schema_cataloguer_search_tenants(loaded_cataloguer):
    tenants = loaded_cataloguer.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1
    assert tenants[0].name == 'Amazon'


def test_schema_cataloguer_load(cataloguer, loaded_connection):
    cataloguer.connection = loaded_connection

    tenants = cataloguer.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1
    assert tenants[0].name == 'Amazon'
