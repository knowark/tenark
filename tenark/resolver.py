from typing import Dict, Optional
from .common import QueryParser
from .cataloguer import (
    Cataloguer, MemoryCataloguer, JsonCataloguer)
from .provisioner import (
    Provisioner, MemoryProvisioner, DirectoryProvisioner)
from .provider import Provider
from .arranger import Arranger


def resolve_cataloguer(options: Dict[str, str]) -> Cataloguer:
    parser = QueryParser()
    cataloguer: Optional[Cataloguer] = None
    if options.get('cataloguer_kind') == 'json':
        path = options['catalog_path']
        cataloguer = JsonCataloguer(path, parser)
    else:
        cataloguer = MemoryCataloguer(parser)

    return cataloguer


def resolve_provisioner(options: Dict[str, str]) -> Provisioner:
    parser = QueryParser()
    provisioner: Optional[Provisioner] = None
    if options.get('provisioner_kind') == 'directory':
        template = options['provision_template']
        data = options['data_directory']
        provisioner = DirectoryProvisioner(template, data)
    else:
        provisioner = MemoryProvisioner()

    return provisioner


def resolve_arranger(options: Dict[str, str]) -> Arranger:
    cataloguer = resolve_cataloguer(options)
    provisioner = resolve_provisioner(options)
    arranger = Arranger(cataloguer, provisioner)
    return arranger


def resolve_provider(options: Dict[str, str]) -> Provider:
    cataloguer = resolve_cataloguer(options)
    provider = Provider(cataloguer)
    return provider
