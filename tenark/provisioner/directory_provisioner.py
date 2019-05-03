from pathlib import Path
from shutil import copytree
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class DirectoryProvisioner(Provisioner):

    def __init__(self, template: str, data: str) -> None:
        self.template = template
        self.data = data

    @property
    def kind(self) -> str:
        return "directory"

    @property
    def location(self) -> str:
        return self.data

    def provision_tenant(self, tenant: Tenant) -> None:
        tenant_directory = str(Path(self.data) / tenant.slug)
        copytree(self.template, tenant_directory)
