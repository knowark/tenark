from typing import Dict
from subprocess import run, PIPE
from ..models import Tenant
from .provisioner import Provisioner


class SchemaProvisioner(Provisioner):

    def __init__(self, zones: Dict[str, str],
                 template='__template__') -> None:
        self.zones = zones
        self.template = template
        self.default_dsn = next(iter(self.zones.values()))

    def provision_tenant(self, tenant: Tenant) -> None:
        dsn = self.zones.get(tenant.zone, self.default_dsn)
        query = (
            f"pg_dump {dsn} --schema={self.template} | "
            f"sed 's/{self.template}/{tenant.slug}/g' | "
            f"psql {dsn}"
        )
        command = f'/bin/bash -euxo pipefail -c "{query}"'
        run(command, shell=True, check=True, stdout=PIPE, stderr=PIPE)
