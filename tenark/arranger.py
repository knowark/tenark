from typing import Dict, List, Optional, Any
from .models import Tenant
from .cataloguer import Cataloguer
from .provisioner import Provisioner
from .common import QueryDomain, TenantCreationError


class Arranger:
    def __init__(self, cataloguer: Cataloguer,
                 provisioner: Provisioner) -> None:
        self.cataloguer = cataloguer
        self.provisioner = provisioner

    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        domain: QueryDomain = ['|', ('slug', '=', tenant.slug),
                               ('name', '=', tenant.name)]
        duplicates = self.cataloguer.search_tenants(domain)

        if duplicates:
            raise TenantCreationError(
                f'A tenant with slug "{tenant.slug}" already exists.')

        tenant = self.cataloguer.add_tenant(tenant)
        self.provisioner.provision_tenant(tenant)
