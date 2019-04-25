from pytest import fixture, raises
from tenark.models import Tenant
from tenark.provider import Provider, StandardProvider


@fixture
def provider() -> StandardProvider:
    return StandardProvider()


def test_standard_provider_instantiation(provider):
    assert isinstance(provider, Provider)


def test_standard_provider_setup(provider):
    tenant = Tenant(name='Alpina')
    assert provider.state.tenant is None
    provider.setup(tenant)
    assert provider.state.tenant == tenant


def test_standard_provider_get_tenant(provider):
    tenant = Tenant(name='Alpina')
    assert provider.state.tenant is None
    provider.setup(tenant)
    assert provider.get_tenant() == tenant


def test_standard_provider_get_tenant_not_set(provider):
    with raises(ValueError):
        assert provider.get_tenant()
