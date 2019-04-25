from abc import ABC, abstractmethod
from typing import Dict, Optional
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class MemoryProvisioner(Provisioner):

    def __init__(self) -> None:
        self.pool: Dict[str, Tenant] = {}

    def provision_tenant(self, tenant: Tenant) -> None:
        tenant.id = tenant.id or str(uuid4())
        self.pool[tenant.id] = tenant
