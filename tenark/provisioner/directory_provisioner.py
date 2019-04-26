from abc import ABC, abstractmethod
from typing import Dict, Optional
from pathlib import Path
from shutil import copytree
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class DirectoryProvisioner(Provisioner):

    def __init__(self, template: str, data: str) -> None:
        self.template = template
        self.data = data

    def provision_tenant(self, tenant: Tenant) -> None:
        tenant_directory = str(Path(self.data) / tenant.slug)
        copytree(self.template, tenant_directory)
