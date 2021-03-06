from pytest import fixture, raises
from tenark.models import Tenant
from tenark.common import QueryParser, TenantRetrievalError
from tenark.cataloguer import MemoryCataloguer
from tenark.provider import Provider


@fixture
def provider() -> Provider:
    parser = QueryParser()
    cataloguer = MemoryCataloguer(parser)
    return Provider(cataloguer)


def test_provider_instantiation(provider):
    assert provider is not None


def test_provider_get_tenant(provider):
    tenant_id = '001'
    provider.cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='002', name='Google'),
        '003': Tenant(id='003', name='Microsoft')
    }
    tenant = provider.get_tenant(tenant_id)
    assert tenant['slug'] == 'amazon'


def test_provider_resolve_tenant(provider):
    provider.cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='002', name='Google'),
        '003': Tenant(id='003', name='Microsoft')
    }
    tenant = provider.resolve_tenant('microsoft')
    assert tenant['slug'] == 'microsoft'

    tenant = provider.resolve_tenant('Google')
    assert tenant['slug'] == 'google'


def test_provider_resolve_tenant_not_found(
        provider):
    provider.cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='001', name='Google'),
        '003': Tenant(id='001', name='Microsoft')
    }
    with raises(TenantRetrievalError):
        provider.resolve_tenant('yahoo')


def test_provider_search_tenants(provider):
    provider.cataloguer.catalog = {
        '001': Tenant(id='001', name='Amazon'),
        '002': Tenant(id='001', name='Google'),
        '003': Tenant(id='001', name='Microsoft')
    }
    domain = []
    tenants = provider.search_tenants([])
    assert len(tenants) == 3
    for tenant in tenants:
        assert isinstance(tenant, dict)
