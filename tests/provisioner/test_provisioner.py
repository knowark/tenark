from pytest import fixture, raises
from tenark.provisioner import Provisioner


def test_provisioner_methods():
    abstract_methods = Provisioner.__abstractmethods__

    assert 'location' in abstract_methods
    assert 'provision_tenant' in abstract_methods
