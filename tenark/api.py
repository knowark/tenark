from .arranger import Arranger
from .provider import Provider
from .resolver import resolve_provider, resolve_arranger


def build_provider(**options) -> Provider:
    provider = resolve_provider(options)
    return provider


def build_arranger(**options) -> Arranger:
    arranger = resolve_arranger(options)
    return arranger
