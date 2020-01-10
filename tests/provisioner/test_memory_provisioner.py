from pytest import fixture, raises
from tenark.models import Tenant
from tenark.common import TenantProvisionError
from tenark.provisioner import Provisioner, MemoryProvisioner


@fixture
def provisioner() -> MemoryProvisioner:
    return MemoryProvisioner()


def test_memory_provisioner_setup(provisioner):
    assert provisioner.pool == {}


def test_memory_provisioner_properties(provisioner):
    assert provisioner.location == {
        "memory": ""
    }


def test_memory_provisioner_provision_tenant(provisioner):
    tenant = Tenant(id='001',name="Servagro")
    provisioner.provision_tenant(tenant)
    assert len(provisioner.pool) == 1
