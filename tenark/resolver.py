from .common import QueryParser
from .cataloguer import Cataloguer, MemoryCataloguer
from .provisioner import Provisioner, MemoryProvisioner
from .arranger import Arranger


def resolve_cataloguer() -> Cataloguer:
    parser = QueryParser()
    cataloguer = MemoryCataloguer(parser)
    return cataloguer


def resolve_provisioner() -> Provisioner:
    provisioner = MemoryProvisioner()
    return provisioner


def resolve_arranger() -> Arranger:
    cataloguer = resolve_cataloguer()
    provisioner = resolve_provisioner()
    arranger = Arranger(cataloguer, provisioner)
    return arranger
