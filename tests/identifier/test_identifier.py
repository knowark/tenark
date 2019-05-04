from pytest import fixture, raises
from tenark.identifier import Identifier


def test_identifier_methods():
    abstract_methods = Identifier.__abstractmethods__

    assert 'generate_id' in abstract_methods
