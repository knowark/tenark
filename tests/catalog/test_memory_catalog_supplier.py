from pytest import fixture, raises
from tenark.common import QueryParser
from tenark.tenant import Tenant
from tenark.catalog import MemoryCatalogSupplier


@fixture
def catalog_supplier() -> MemoryCatalogSupplier:
    parser = QueryParser()
    return MemoryCatalogSupplier(parser)


def test_memory_catalog_supplier_setup_catalog(catalog_supplier):
    catalog_supplier.setup()
    assert catalog_supplier.catalog == {}


def test_memory_catalog_supplier_add_tenant(catalog_supplier):
    tenant = Tenant(name='Microsoft')
    catalog_supplier.setup()
    tenant = catalog_supplier.add_tenant(tenant)
    assert len(catalog_supplier.catalog) == 1


def test_memory_catalog_supplier_add_tenant_no_setup(catalog_supplier):
    tenant = Tenant(name='Microsoft')
    with raises(ValueError):
        catalog_supplier.add_tenant(tenant)


def test_memory_catalog_supplier_search_tenants_empty(catalog_supplier):
    tenant = Tenant(name='Microsoft')
    catalog_supplier.setup()
    tenants = catalog_supplier.search_tenants([])
    assert len(tenants) == 0


def test_memory_catalog_supplier_search_tenants(
        catalog_supplier: MemoryCatalogSupplier):
    tenant = Tenant(name='Microsoft')
    catalog_supplier.setup()
    catalog_supplier.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }
    tenants = catalog_supplier.search_tenants(
        [('slug', '=', 'amazon')])
    assert len(tenants) == 1


def test_memory_catalog_supplier_search_tenants_no_setup(
        catalog_supplier: MemoryCatalogSupplier):
    with raises(ValueError):
        tenants = catalog_supplier.search_tenants([])


def test_memory_catalog_supplier_get_tenant(
        catalog_supplier: MemoryCatalogSupplier):
    catalog_supplier.setup()
    catalog_supplier.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }
    tenant = catalog_supplier.get_tenant('002')
    assert tenant.name == 'Google'


def test_memory_catalog_supplier_get_tenant_not_found(
        catalog_supplier: MemoryCatalogSupplier):
    catalog_supplier.setup()
    catalog_supplier.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }
    with raises(ValueError):
        catalog_supplier.get_tenant('004')


def test_memory_catalog_supplier_get_tenant_not_setup(
        catalog_supplier: MemoryCatalogSupplier):
    with raises(ValueError):
        catalog_supplier.get_tenant('001')
