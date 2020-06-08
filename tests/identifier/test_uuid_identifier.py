from tenark.identifier import UuidIdentifier


def test_uuid_identifier_generate_id():
    identifier = UuidIdentifier()
    id = identifier.generate_id()

    assert len(id) == 36
