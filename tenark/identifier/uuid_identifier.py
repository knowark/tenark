from uuid import uuid4
from .identifier import Identifier


class UuidIdentifier(Identifier):

    def generate_id(self) -> str:
        return str(uuid4())
