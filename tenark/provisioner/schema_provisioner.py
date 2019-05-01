from abc import ABC, abstractmethod
from typing import Dict, Optional
from pathlib import Path
from shutil import copytree
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class SchemaProvisioner(Provisioner):

    def __init__(self, template_dsn: str, database_dsn: str,
                 template='__template__') -> None:
        self.template_dsn = template_dsn
        self.database_dsn = database_dsn
        self.template = template

    def provision_tenant(self, tenant: Tenant) -> None:
        pass
        # tenant_directory = str(Path(self.data) / tenant.slug)
        # copytree(self.template, tenant_directory)
