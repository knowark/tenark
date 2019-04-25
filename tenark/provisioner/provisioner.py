from abc import ABC, abstractmethod
from uuid import uuid4
from typing import List, Dict, Any, Optional
from ..models import Tenant


class Provisioner(ABC):
    """Tenant Provision service."""

    @abstractmethod
    def provision_tenant(self, tenant: Tenant) -> None:
        "Provision tenant method to be implemented."
