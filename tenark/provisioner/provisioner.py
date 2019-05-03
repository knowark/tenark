from typing import Dict
from abc import ABC, abstractmethod
from ..models import Tenant


class Provisioner(ABC):
    """Tenant Provision service."""

    @property
    @abstractmethod
    def location(self) -> Dict[str, str]:
        "Show provisioner data location."

    @abstractmethod
    def provision_tenant(self, tenant: Tenant) -> None:
        "Provision tenant method to be implemented."
