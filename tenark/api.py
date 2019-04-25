from .arranger import Arranger
from .resolver import resolve_arranger


def build_arranger() -> Arranger:
    arranger = resolve_arranger()
    return arranger
