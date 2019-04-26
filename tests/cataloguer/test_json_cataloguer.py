import json
from pathlib import Path
from pytest import fixture, raises
from tenark.common import (
    QueryParser, TenantCatalogError, TenantRetrievalError)
from tenark.models import Tenant
from tenark.cataloguer import JsonCataloguer


@fixture
def cataloguer(tmp_path) -> JsonCataloguer:
    path = str(tmp_path / 'tenants.json')
    parser = QueryParser()
    return JsonCataloguer(path, parser)


def test_json_cataloguer_setup_catalog(cataloguer):
    with Path(cataloguer.path).open() as f:
        data = json.load(f)
        assert cataloguer.collection in data


def test_json_cataloguer_add_tenant(cataloguer):
    tenant = Tenant(name='Microsoft')
    tenant = cataloguer.add_tenant(tenant)

    with Path(cataloguer.path).open() as f:
        data = json.load(f)
        tenants = data['tenants']
        assert tenant.id in tenants


# def test_json_cataloguer_add_tenant_no_setup(cataloguer):
#     tenant = Tenant(name='Microsoft')
#     with raises(TenantCatalogError):
#         cataloguer.add_tenant(tenant)

def test_json_cataloguer_file_preexisting_empty_catalog(tmp_path):
    path = tmp_path / 'empty_tenants.json'
    with path.open('w') as f:
        f.write("")

    parser = QueryParser()
    cataloguer = JsonCataloguer(str(path), parser)

    with path.open() as f:
        data = json.load(f)
        assert cataloguer.collection in data


def test_json_cataloguer_file_preexisting_correct_catalog(tmp_path):
    path = tmp_path / 'correct_tenants.json'
    with path.open('w') as f:
        json.dump({
            "tenants": {}
        }, f, indent=2)

    parser = QueryParser()
    cataloguer = JsonCataloguer(str(path), parser)

    with path.open() as f:
        data = json.load(f)
        assert cataloguer.collection in data


def test_json_cataloguer_add_tenant_no_valid_json(cataloguer):
    tenant = Tenant(name='Microsoft')
    with Path(cataloguer.path).open('w') as f:
        f.write('{')

    with raises(TenantCatalogError):
        cataloguer.add_tenant(tenant)


def test_json_cataloguer_search_tenants_empty(cataloguer):
    tenant = Tenant(name='Microsoft')
    tenants = cataloguer.search_tenants([])
    assert len(tenants) == 0


def test_json_cataloguer_search_tenants(
        cataloguer: JsonCataloguer):
    tenant = Tenant(name='Microsoft')
    with Path(cataloguer.path).open('w') as f:
        json.dump({
            'tenants': {
                '001': vars(Tenant(name='Amazon')),
                '002': vars(Tenant(name='Google')),
                '003': vars(Tenant(name='Microsoft'))
            }
        }, f, indent=2)

    tenants = cataloguer.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1


def test_json_cataloguer_get_tenant(
        cataloguer: JsonCataloguer):

    with Path(cataloguer.path).open('w') as f:
        json.dump({
            'tenants': {
                '001': vars(Tenant(name='Amazon')),
                '002': vars(Tenant(name='Google')),
                '003': vars(Tenant(name='Microsoft'))
            }
        }, f, indent=2)

    tenant = cataloguer.get_tenant('002')
    assert tenant.name == 'Google'


def test_json_cataloguer_get_tenant_not_found(
        cataloguer: JsonCataloguer):
    with Path(cataloguer.path).open('w') as f:
        json.dump({
            'tenants': {
                '001': vars(Tenant(name='Amazon')),
                '002': vars(Tenant(name='Google')),
                '003': vars(Tenant(name='Microsoft'))
            }
        }, f, indent=2)

    with raises(TenantRetrievalError):
        cataloguer.get_tenant('004')


# def test_json_cataloguer_get_tenant_not_setup(
#         cataloguer: JsonCataloguer):
#     with raises(ValueError):
#         cataloguer.get_tenant('001')
