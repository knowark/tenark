from pytest import raises
from typing import List, Dict, Sequence, Any
from tenark.cataloguer import (
    MemoryCataloguer, JsonCataloguer, SchemaCataloguer)
from tenark.provisioner import (
    MemoryProvisioner, DirectoryProvisioner, SchemaProvisioner)
from tenark.provider import Provider
from tenark.arranger import Arranger
from tenark import resolver


def test_resolver_resolve_cataloguer_no_options():
    options = {}
    cataloguer = resolver.resolve_cataloguer(options)

    assert isinstance(cataloguer, MemoryCataloguer)


def test_resolver_resolve_cataloguer_json(monkeypatch):
    monkeypatch.setattr(JsonCataloguer, '_setup', lambda self: None)
    options = {
        'cataloguer_kind': 'json'
    }
    with raises(KeyError):
        cataloguer = resolver.resolve_cataloguer(options)
    options['catalog_path'] = '/home/user/tenants.json'
    cataloguer = resolver.resolve_cataloguer(options)

    assert isinstance(cataloguer, JsonCataloguer)


def test_resolver_resolve_cataloguer_schema(monkeypatch):
    class CustomConnection():
        def open(self) -> None:
            """Open"""

        def close(self) -> None:
            """Close"""

        def execute(self, statement: str,
                    parameters: Sequence[Any] = []) -> str:
            """Execute"""

        def select(self, statement: str,
                   parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
            """Select"""

    options: Dict[str, Any] = {
        'cataloguer_kind': 'schema'
    }
    with raises(KeyError):
        cataloguer = resolver.resolve_cataloguer(options)

    options['catalog_connection'] = CustomConnection()
    cataloguer = resolver.resolve_cataloguer(options)

    assert isinstance(cataloguer, SchemaCataloguer)


def test_resolver_resolve_provisioner_no_options():
    options = {}
    provisioner = resolver.resolve_provisioner(options)

    assert isinstance(provisioner, MemoryProvisioner)


def test_resolver_resolve_provisioner_directory():
    options: Dict[str, Any] = {
        'provisioner_kind': 'directory'
    }
    with raises(KeyError):
        resolver.resolve_provisioner(options)
    options['provision_template'] = '/home/user/templates/__template__'
    with raises(KeyError):
        resolver.resolve_provisioner(options)
    options['provision_directory_zones'] = {
        'default':  '/home/user/data'
    }
    provisioner = resolver.resolve_provisioner(options)

    assert isinstance(provisioner, DirectoryProvisioner)


def test_resolver_resolve_provisioner_schema():
    options: Dict[str, Any] = {
        'provisioner_kind': 'schema'
    }
    with raises(KeyError):
        cataloguer = resolver.resolve_provisioner(options)
    options['provision_schema_zones'] = {
        'default': 'postgresql://postgres:postgres@localhost/db'
    }
    provisioner = resolver.resolve_provisioner(options)

    assert isinstance(provisioner, SchemaProvisioner)


def test_resolver_resolve_arranger():
    options = {}
    arranger = resolver.resolve_arranger(options)

    assert isinstance(arranger, Arranger)
    assert isinstance(arranger.cataloguer, MemoryCataloguer)
    assert isinstance(arranger.provisioner, MemoryProvisioner)


def test_resolver_resolve_provider():
    options = {}
    provider = resolver.resolve_provider({})

    assert isinstance(provider, Provider)
    assert isinstance(provider.cataloguer, MemoryCataloguer)


def test_resolver_resolve_managers():
    options = {}
    arranger, provider = resolver.resolve_managers({})

    assert isinstance(arranger, Arranger)
    assert isinstance(provider, Provider)
    assert isinstance(arranger.cataloguer, MemoryCataloguer)
    assert isinstance(provider.cataloguer, MemoryCataloguer)
    assert arranger.cataloguer is provider.cataloguer
