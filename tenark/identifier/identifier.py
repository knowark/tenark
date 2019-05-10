from abc import ABC, abstractmethod


class Identifier(ABC):
    """Identifier Service."""

    @abstractmethod
    def generate_id(self) -> str:
        "Generate ID method to be implemented."
