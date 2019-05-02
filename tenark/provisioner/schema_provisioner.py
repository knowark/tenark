from subprocess import run, PIPE
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class SchemaProvisioner(Provisioner):

    def __init__(self, database="", template='__template__', uri="") -> None:
        self.database = database
        self.template = template
        self.uri = uri

    def provision_tenant(self, tenant: Tenant) -> None:
        command = (
            f"pg_dump --schema={self.template} {self.database} | "
            f"sed 's/{self.template}/{tenant.slug}/g' | "
            f"psql -d {self.database}")
        run(command, shell=True, check=True)
