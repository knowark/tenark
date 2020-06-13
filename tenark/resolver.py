from typing import Dict, Any, Optional, Tuple
from .identifier import Identifier, UuidIdentifier
from .cataloguer import (
    Cataloguer, MemoryCataloguer, JsonCataloguer,
    SchemaCataloguer)
from .provisioner import (
    Provisioner, MemoryProvisioner,
    DirectoryProvisioner, SchemaProvisioner)
from .provider import Provider
from .arranger import Arranger


def resolve_identifier(options: Dict[str, Any]) -> Identifier:
    identifier = UuidIdentifier()
    return identifier


def resolve_cataloguer(options: Dict[str, Any]) -> Cataloguer:
    cataloguer: Optional[Cataloguer] = None
    if options.get('cataloguer_kind') == 'json':
        path = options['catalog_path']
        cataloguer = JsonCataloguer(path)
    elif options.get('cataloguer_kind') == 'schema':
        connection = options['catalog_connection']
        cataloguer = SchemaCataloguer(connection)
    else:
        cataloguer = MemoryCataloguer()

    return cataloguer


def resolve_provisioner(options: Dict[str, Any]) -> Provisioner:
    provisioner: Optional[Provisioner] = None
    if options.get('provisioner_kind') == 'directory':
        template = options['provision_template']
        zones = options['provision_directory_zones']
        provisioner = DirectoryProvisioner(zones, template)
    elif options.get('provisioner_kind') == 'schema':
        zones = options['provision_schema_zones']
        provisioner = SchemaProvisioner(zones)
    else:
        provisioner = MemoryProvisioner()

    return provisioner


def resolve_arranger(options: Dict[str, Any]) -> Arranger:
    identifier = options.setdefault(
        'identifier', resolve_identifier(options))
    cataloguer = options.setdefault(
        'cataloguer', resolve_cataloguer(options))
    provisioner = options.setdefault(
        'provisioner', resolve_provisioner(options))
    return Arranger(cataloguer, provisioner, identifier)


def resolve_provider(options: Dict[str, Any]) -> Provider:
    cataloguer = options.setdefault(
        'cataloguer', resolve_cataloguer(options))
    return Provider(cataloguer)


def resolve_managers(options: Dict[str, Any]) -> Tuple[Arranger, Provider]:
    arranger = resolve_arranger(options)
    provider = resolve_provider(options)
    return arranger, provider
