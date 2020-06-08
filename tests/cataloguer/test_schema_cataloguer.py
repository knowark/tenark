import json
import psycopg2
from pytest import fixture, raises
from tenark.common import (
    QueryParser, TenantRetrievalError)
from tenark.models import Tenant
from tenark.cataloguer import SchemaCataloguer


@fixture(scope="session")
def database():
    database = "tenark_catalog"
    postgres_dsn = f"dbname=postgres user=postgres password=postgres"
    with psycopg2.connect(postgres_dsn) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {database}")
            cursor.execute(f"CREATE DATABASE {database}")

    return database


@fixture
def cataloguer(database) -> SchemaCataloguer:
    dsn = f"dbname={database} user=postgres"
    schema = 'public'
    table = '__tenants__'
    parser = QueryParser()

    cataloguer = SchemaCataloguer(dsn, schema, table, parser)

    connection = psycopg2.connect(cataloguer.dsn)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            f"TRUNCATE TABLE {cataloguer.schema}.{cataloguer.table};")

    return cataloguer


@fixture
def loaded_cataloguer(cataloguer) -> SchemaCataloguer:
    tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
    tenant_1_value = json.dumps({
        'id': tenant_1_id,
        'name': 'Amazon'
    })
    tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'
    tenant_2_value = json.dumps({
        'id': tenant_2_id,
        'name': 'Google'
    })

    connection = psycopg2.connect(cataloguer.dsn)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {cataloguer.schema}.{cataloguer.table} (data)"
            f"VALUES (%s);", (tenant_1_value,))
        cursor.execute(
            f"INSERT INTO {cataloguer.schema}.{cataloguer.table} (data)"
            f"VALUES (%s);", (tenant_2_value,))

    cataloguer._load()

    return cataloguer


def test_schema_cataloguer_setup_catalog(cataloguer):
    connection = psycopg2.connect(cataloguer.dsn)
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT data FROM {cataloguer.schema}.{cataloguer.table}")
        result = cursor.fetchall()

    assert result == []


def test_schema_cataloguer_add_tenant(cataloguer):
    tenant_id = 'ec002b8d-30eb-447a-ac5b-be966763723b'
    tenant = Tenant(
        id=tenant_id,
        name='Microsoft')
    tenant = cataloguer.add_tenant(tenant)

    connection = psycopg2.connect(cataloguer.dsn)
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT data FROM {cataloguer.schema}.{cataloguer.table}")
        result = cursor.fetchall()

    tenant_dict = result[0][0]
    assert tenant_dict['id'] == tenant_id


def test_schema_cataloguer_get_tenant(loaded_cataloguer):
    tenant_1_id = '946568c6-f102-40b3-8a64-920d66f4180d'
    tenant_2_id = 'b5807a8a-8bc1-4d91-98d0-424068494876'

    tenant_2 = loaded_cataloguer.get_tenant(tenant_2_id)
    assert tenant_2.name == 'Google'

    tenant_1 = loaded_cataloguer.get_tenant(tenant_1_id)
    assert tenant_1.name == 'Amazon'


def test_schema_cataloguer_get_tenant_not_found(loaded_cataloguer):
    with raises(TenantRetrievalError):
        loaded_cataloguer.get_tenant('004')


def test_schema_cataloguer_search_tenants(loaded_cataloguer):
    tenants = loaded_cataloguer.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1
    assert tenants[0].name == 'Amazon'


# def test_json_cataloguer_file_preexisting_empty_catalog(tmp_path):
#     path = tmp_path / 'empty_tenants.json'
#     with path.open('w') as f:
#         f.write("")

#     parser = QueryParser()
#     cataloguer = JsonCataloguer(str(path), parser)

#     with path.open() as f:
#         data = json.load(f)
#         assert cataloguer.collection in data


# def test_json_cataloguer_file_preexisting_correct_catalog(tmp_path):
#     path = tmp_path / 'correct_tenants.json'
#     with path.open('w') as f:
#         json.dump({
#             "tenants": {}
#         }, f, indent=2)

#     parser = QueryParser()
#     cataloguer = JsonCataloguer(str(path), parser)

#     with path.open() as f:
#         data = json.load(f)
#         assert cataloguer.collection in data


# def test_json_cataloguer_file_incorrect_json_catalog(tmp_path):
#     path = tmp_path / 'incorrect_tenants.json'
#     with path.open('w') as f:
#         f.write("{}")

#     parser = QueryParser()
#     cataloguer = JsonCataloguer(str(path), parser)

#     with path.open() as f:
#         data = json.load(f)
#         assert cataloguer.collection in data


# def test_json_cataloguer_search_tenants_empty(cataloguer):
#     tenant = Tenant(name='Microsoft')
#     tenants = cataloguer.search_tenants([])
#     assert len(tenants) == 0


# def test_json_cataloguer_search_tenants(
#         cataloguer: JsonCataloguer):
#     tenant = Tenant(name='Microsoft')
#     with Path(cataloguer.path).open('w') as f:
#         json.dump({
#             'tenants': {
#                 '001': vars(Tenant(name='Amazon')),
#                 '002': vars(Tenant(name='Google')),
#                 '003': vars(Tenant(name='Microsoft'))
#             }
#         }, f, indent=2)

#     cataloguer._load()
#     tenants = cataloguer.search_tenants(
#         [('slug', '=', 'amazon')])
#     assert len(tenants) == 1
