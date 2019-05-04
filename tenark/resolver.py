from typing import Dict, Any, Optional
from .common import QueryParser
from .identifier import Identifier, UuidIdentifier
from .cataloguer import (
    Cataloguer, MemoryCataloguer, JsonCataloguer)
from .provisioner import (
    Provisioner, MemoryProvisioner,
    DirectoryProvisioner, SchemaProvisioner)
from .provider import Provider
from .arranger import Arranger


def resolve_identifier(options: Dict[str, Any]) -> Identifier:
    identifier = UuidIdentifier()
    return identifier


def resolve_cataloguer(options: Dict[str, Any]) -> Cataloguer:
    parser = QueryParser()
    cataloguer: Optional[Cataloguer] = None
    if options.get('cataloguer_kind') == 'json':
        path = options['catalog_path']
        cataloguer = JsonCataloguer(path, parser)
    else:
        cataloguer = MemoryCataloguer(parser)

    return cataloguer


def resolve_provisioner(options: Dict[str, Any]) -> Provisioner:
    parser = QueryParser()
    provisioner: Optional[Provisioner] = None
    if options.get('provisioner_kind') == 'directory':
        template = options['provision_template']
        data = options['data_directory']
        provisioner = DirectoryProvisioner(template, data)
    elif options.get('provisioner_kind') == 'schema':
        uri = options['provision_uri']
        provisioner = SchemaProvisioner(uri)
    else:
        provisioner = MemoryProvisioner()

    return provisioner


def resolve_arranger(options: Dict[str, Any]) -> Arranger:
    identifier = options.get('identifier', resolve_identifier(options))
    cataloguer = options.get('cataloguer', resolve_cataloguer(options))
    provisioner = options.get('provisioner', resolve_provisioner(options))
    arranger = Arranger(cataloguer, provisioner, identifier)
    return arranger


def resolve_provider(options: Dict[str, Any]) -> Provider:
    cataloguer = options.get('cataloguer', resolve_cataloguer(options))
    provider = Provider(cataloguer)
    return provider
