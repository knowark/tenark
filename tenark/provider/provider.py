from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models import Tenant


class Provider(ABC):
    """Tenant Provider."""

    @abstractmethod
    def setup(self, tenant: Tenant) -> None:
        "Setup current tenant method to be implemented."

    @abstractmethod
    def get_tenant(self) -> Tenant:
        """Get the current tenant"""
