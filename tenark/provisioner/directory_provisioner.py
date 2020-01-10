from typing import Dict
from pathlib import Path
from shutil import copytree
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class DirectoryProvisioner(Provisioner):

    def __init__(self, zones: Dict[str, str], template: str) -> None:
        self.zones = zones
        self.template = template
        self.default_directory = next(iter(self.zones.values()))

    def provision_tenant(self, tenant: Tenant) -> None:
        directory = self.zones.get(tenant.zone, self.default_directory)
        tenant_directory = str(Path(directory) / tenant.slug)
        copytree(self.template, tenant_directory)
