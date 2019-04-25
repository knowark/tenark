from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class MemoryProvisioner(Provisioner):

    def __init__(self) -> None:
        self.pool: Optional[Dict] = None

    def setup(self) -> bool:
        self.pool = {}
        return True

    def provision_tenant(self, tenant: Tenant) -> None:
        tenant.id = tenant.id or str(uuid4())
        if self.pool is None:
            raise TenantProvisionError(
                "Setup the provisioning environment first.")
        self.pool[tenant.id] = tenant
