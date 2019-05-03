from typing import Dict
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class MemoryProvisioner(Provisioner):

    def __init__(self) -> None:
        self.pool: Dict[str, Tenant] = {}

    @property
    def location(self) -> Dict[str, str]:
        return {
            "memory": ""
        }

    def provision_tenant(self, tenant: Tenant) -> None:
        self.pool[tenant.id] = tenant
