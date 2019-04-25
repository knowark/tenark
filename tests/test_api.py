from tenark.api import build_arranger
from tenark.arranger import Arranger


def test_api_build_arranger():
    arranger = build_arranger()
    assert isinstance(arranger, Arranger)
