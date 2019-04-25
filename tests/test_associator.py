from typing import Dict
from pytest import fixture, raises
from tenark.models import Tenant
from tenark.common import QueryParser, TenantRetrievalError
from tenark.cataloguer import MemoryCataloguer
from tenark.provider import StandardProvider
from tenark.associator import Associator


@fixture
def associator() -> Associator:
    parser = QueryParser()
    cataloguer = MemoryCataloguer(parser)
    provider = StandardProvider()
    return Associator(cataloguer, provider)


def test_associator_instantiation(associator):
    assert associator is not None


def test_associator_establish_tenant(associator):
    tenant_id = '001'
    associator.cataloguer.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    associator.establish_tenant(tenant_id)
    tenant = associator.provider.get_tenant()
    assert tenant.slug == 'amazon'


def test_associator_get_current_tenant(associator):
    associator.provider.state.tenant = (
        Tenant(id='001', name='Amazon'))

    current_tenant = associator.get_current_tenant()
    assert isinstance(current_tenant, dict)
    assert current_tenant.get('id') == '001'
    assert current_tenant.get('name') == 'Amazon'


def test_associator_resolve_tenant(associator):
    associator.cataloguer.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    associator.resolve_tenant('microsoft')
    tenant = associator.provider.get_tenant()
    assert tenant.slug == 'microsoft'

    associator.resolve_tenant('Google')
    tenant = associator.provider.get_tenant()
    assert tenant.slug == 'google'


def test_associator_resolve_tenant_not_found(
        associator):
    associator.cataloguer.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft')
    }
    with raises(TenantRetrievalError):
        associator.resolve_tenant('yahoo')
