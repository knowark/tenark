from tenark.provisioner import Provisioner


def test_provisioner_methods():
    abstract_methods = Provisioner.__abstractmethods__  # type: ignore

    assert 'provision_tenant' in abstract_methods
