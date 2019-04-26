from .common import QueryParser
from .cataloguer import Cataloguer, MemoryCataloguer
from .provisioner import Provisioner, MemoryProvisioner
from .provider import Provider, StandardProvider
from .associator import Associator
from .arranger import Arranger


def resolve_cataloguer() -> Cataloguer:
    parser = QueryParser()
    cataloguer = MemoryCataloguer(parser)
    return cataloguer


def resolve_provisioner() -> Provisioner:
    provisioner = MemoryProvisioner()
    return provisioner


def resolve_provider() -> Provider:
    provider = StandardProvider()
    return provider


def resolve_arranger() -> Arranger:
    cataloguer = resolve_cataloguer()
    provisioner = resolve_provisioner()
    arranger = Arranger(cataloguer, provisioner)
    return arranger


def resolve_associator() -> Associator:
    cataloguer = resolve_cataloguer()
    provider = resolve_provider()
    associator = Associator(cataloguer, provider)
    return associator
