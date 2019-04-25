from pytest import raises, fixture
from typing import cast
from tenark.models import Tenant
from tenark.arranger import Arranger
from tenark.cataloguer import MemoryCataloguer
from tenark.provisioner import MemoryProvisioner
from tenark.common import TenantCreationError, QueryParser


@fixture
def arranger() -> Arranger:
    parser = QueryParser()
    cataloguer = MemoryCataloguer(parser)
    provisioner = MemoryProvisioner()
    return Arranger(cataloguer, provisioner)


def test_arranger_creation(
        arranger: Arranger) -> None:
    assert hasattr(Arranger, 'create_tenant')


def test_arranger_create_tenant(
        arranger: Arranger) -> None:
    provisioner = cast(MemoryProvisioner,
                       arranger.provisioner)
    tenant_dict = {"name": "Google"}
    arranger.create_tenant(tenant_dict)
    assert len(provisioner.pool) == 1


def test_arranger_create_tenant_duplicate(
        arranger: Arranger) -> None:
    provisioner = cast(MemoryProvisioner,
                       arranger.provisioner)
    cataloguer = cast(MemoryCataloguer,
                      arranger.cataloguer)
    cataloguer.catalog = {
        '001': Tenant(name='Amazon'),
        '002': Tenant(name='Google'),
        '003': Tenant(name='Microsoft'),
    }

    tenant_dict = {"name": "Google"}
    with raises(TenantCreationError):
        arranger.create_tenant(tenant_dict)
