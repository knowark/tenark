from tenark.api import build_arranger, build_provider
from tenark.provider import Provider
from tenark.arranger import Arranger


def test_api_build_provider():
    provider = build_provider()
    assert isinstance(provider, Provider)


def test_api_build_arranger():
    arranger = build_arranger()
    assert isinstance(arranger, Arranger)
