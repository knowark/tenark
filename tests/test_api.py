from tenark.api import build_arranger, build_associator
from tenark.associator import Associator
from tenark.arranger import Arranger


def test_api_build_associator():
    associator = build_associator()
    assert isinstance(associator, Associator)


def test_api_build_arranger():
    arranger = build_arranger()
    assert isinstance(arranger, Arranger)
