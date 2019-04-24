from pytest import fixture, raises
from tenark.catalog import CatalogSupplier


def test_catalog_supplier_methods():
    abstract_methods = CatalogSupplier.__abstractmethods__

    assert 'setup' in abstract_methods
    assert 'add_tenant' in abstract_methods
    assert 'get_tenant' in abstract_methods
    assert 'search_tenants' in abstract_methods
