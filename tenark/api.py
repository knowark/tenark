from .arranger import Arranger
from .associator import Associator
from .resolver import resolve_associator, resolve_arranger


def build_associator(**options) -> Associator:
    associator = resolve_associator(options)
    return associator


def build_arranger(**options) -> Arranger:
    arranger = resolve_arranger(options)
    return arranger
