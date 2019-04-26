from tenark.cataloguer import MemoryCataloguer
from tenark.provisioner import MemoryProvisioner
from tenark.provider import StandardProvider
from tenark.associator import Associator
from tenark.arranger import Arranger
from tenark import resolver


def test_resolver_resolve_catalog():
    cataloguer = resolver.resolve_cataloguer()
    assert isinstance(cataloguer, MemoryCataloguer)


def test_resolver_resolve_provisioner():
    provisioner = resolver.resolve_provisioner()
    assert isinstance(provisioner, MemoryProvisioner)


def test_resolver_resolve_arranger():
    arranger = resolver.resolve_arranger()
    assert isinstance(arranger, Arranger)
    assert isinstance(arranger.cataloguer, MemoryCataloguer)
    assert isinstance(arranger.provisioner, MemoryProvisioner)


def test_resolver_resolve_associator():
    associator = resolver.resolve_associator()
    assert isinstance(associator, Associator)
    assert isinstance(associator.cataloguer, MemoryCataloguer)
    assert isinstance(associator.provider, StandardProvider)
