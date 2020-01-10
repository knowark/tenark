from pytest import fixture, raises
from tenark.common import QueryParser, TenantRetrievalError
from tenark.models import Tenant
from tenark.cataloguer import MemoryCataloguer


@fixture
def cataloguer() -> MemoryCataloguer:
    parser = QueryParser()
    return MemoryCataloguer(parser)


def test_memory_cataloguer_setup_catalog(cataloguer):
    assert cataloguer.catalog == {}


def test_memory_cataloguer_add_tenant(cataloguer):
    tenant = Tenant(id='001', name='Microsoft')
    tenant = cataloguer.add_tenant(tenant)
    assert len(cataloguer.catalog) == 1


def test_memory_cataloguer_search_tenants_empty(cataloguer):
    tenant = Tenant(id='001', name='Microsoft')
    tenants = cataloguer.search_tenants([])
    assert len(tenants) == 0


def test_memory_cataloguer_search_tenants(
        cataloguer: MemoryCataloguer):
    tenant = Tenant(id='003', name='Microsoft')
    cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='002', name='Google'),
        '003': Tenant(id='003', name='Microsoft'),
    }
    tenants = cataloguer.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1


def test_memory_cataloguer_get_tenant(
        cataloguer: MemoryCataloguer):
    cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='002', name='Google'),
        '003': Tenant(id='003', name='Microsoft'),
    }
    tenant = cataloguer.get_tenant('002')
    assert tenant.name == 'Google'


def test_memory_cataloguer_get_tenant_not_found(
        cataloguer: MemoryCataloguer):
    cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='002', name='Google'),
        '003': Tenant(id='003', name='Microsoft'),
    }
    with raises(TenantRetrievalError):
        cataloguer.get_tenant('004')
