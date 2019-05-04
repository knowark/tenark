from uuid import uuid4


class UuidIdentifier:

    def generate_id(self) -> str:
        return str(uuid4())
