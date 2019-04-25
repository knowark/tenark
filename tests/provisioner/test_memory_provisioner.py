from pytest import fixture, raises
from tenark.models import Tenant
from tenark.common import TenantProvisionError
from tenark.provisioner import Provisioner, MemoryProvisioner


@fixture
def provisioner() -> MemoryProvisioner:
    return MemoryProvisioner()


def test_memory_provisioner_setup(provisioner):
    provisioner.setup()
    assert provisioner.pool == {}


def test_memory_provisioner_provision_tenant(provisioner):
    tenant = Tenant(name="Servagro")
    provisioner.setup()
    provisioner.provision_tenant(tenant)
    assert len(provisioner.pool) == 1


def test_memory_provisioner_provision_tenant_no_setup(provisioner):
    tenant = Tenant(name="Servagro")
    with raises(TenantProvisionError):
        provisioner.provision_tenant(tenant)
