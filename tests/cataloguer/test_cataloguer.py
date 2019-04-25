from pytest import fixture, raises
from tenark.cataloguer import Cataloguer


def test_cataloguer_methods():
    abstract_methods = Cataloguer.__abstractmethods__

    assert 'setup' in abstract_methods
    assert 'add_tenant' in abstract_methods
    assert 'get_tenant' in abstract_methods
    assert 'search_tenants' in abstract_methods
