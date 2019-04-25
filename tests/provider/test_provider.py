from tenark.provider import Provider


def test_provider_methods():
    abstract_methods = Provider.__abstractmethods__

    assert 'setup' in abstract_methods
    assert 'get_tenant' in abstract_methods
