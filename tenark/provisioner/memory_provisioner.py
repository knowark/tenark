from typing import Dict
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class MemoryProvisioner(Provisioner):

    def __init__(self) -> None:
        self.pool: Dict[str, Tenant] = {}

    @property
    def kind(self) -> str:
        return "memory"

    @property
    def location(self) -> str:
        return ""

    def provision_tenant(self, tenant: Tenant) -> None:
        self.pool[tenant.id] = tenant
