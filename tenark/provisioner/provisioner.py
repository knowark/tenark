from abc import ABC, abstractmethod
from ..models import Tenant


class Provisioner(ABC):
    """Tenant Provision service."""

    @property
    @abstractmethod
    def kind(self) -> str:
        "Show provisioner data kind."

    @property
    @abstractmethod
    def location(self) -> str:
        "Show provisioner data location."

    @abstractmethod
    def provision_tenant(self, tenant: Tenant) -> None:
        "Provision tenant method to be implemented."
