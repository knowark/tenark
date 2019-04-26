from .arranger import Arranger
from .associator import Associator
from .resolver import resolve_associator, resolve_arranger


def build_associator() -> Associator:
    associator = resolve_associator()
    return associator


def build_arranger() -> Arranger:
    arranger = resolve_arranger()
    return arranger
