from pytest import fixture
from tenark.models import Tenant
from tenark.provisioner import MemoryProvisioner


@fixture
def provisioner() -> MemoryProvisioner:
    return MemoryProvisioner()


def test_memory_provisioner_setup(provisioner):
    assert provisioner.pool == {}


def test_memory_provisioner_provision_tenant(provisioner):
    tenant = Tenant(id='001', name="Servagro")
    provisioner.provision_tenant(tenant)
    assert len(provisioner.pool) == 1
