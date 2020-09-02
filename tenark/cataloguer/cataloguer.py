from abc import ABC, abstractmethod
from typing import List
from ..common import QueryDomain
from ..models import Tenant


class Cataloguer(ABC):
    """Tenant Catalog Supplier."""

    @abstractmethod
    def load(self, cache: bool = True) -> None:
        "Load method to be implemented."

    @abstractmethod
    def add_tenant(self, tenant: Tenant) -> Tenant:
        "Add tenant method to be implemented."

    @abstractmethod
    def get_tenant(self, tenant_id: str) -> Tenant:
        "Get tenant method to be implemented."

    @abstractmethod
    def search_tenants(self, domain: QueryDomain) -> List[Tenant]:
        "Search tenants method to be implemented."
