from typing import Dict
from subprocess import run, PIPE
from uuid import uuid4
from ..common import TenantProvisionError
from ..models import Tenant
from .provisioner import Provisioner


class SchemaProvisioner(Provisioner):

    def __init__(self, uri: str, template='__template__') -> None:
        self.uri = uri
        self.template = template

    @property
    def location(self) -> Dict[str, str]:
        return {
            "schema": self.uri
        }

    def provision_tenant(self, tenant: Tenant) -> None:
        query = (
            f"pg_dump {self.uri} --schema={self.template} | "
            f"sed 's/{self.template}/{tenant.slug}/g' | "
            f"psql {self.uri}"
        )
        command = f'/bin/bash -euxo pipefail -c "{query}"'
        run(command, shell=True, check=True, stdout=PIPE, stderr=PIPE)
