from typing import Dict, List, Optional, Any
from .models import Tenant
from .cataloguer import Cataloguer
from .provisioner import Provisioner
from .identifier import Identifier
from .common import QueryDomain, TenantCreationError


class Arranger:
    def __init__(self, cataloguer: Cataloguer,
                 provisioner: Provisioner,
                 identifier: Identifier) -> None:
        self.cataloguer = cataloguer
        self.provisioner = provisioner
        self.identifier = identifier

    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant = Tenant(**tenant_dict)
        domain: QueryDomain = [
            '|', ('slug', '=', tenant.slug), ('name', '=', tenant.name)]
        duplicates = self.cataloguer.search_tenants(domain)

        if duplicates:
            raise TenantCreationError(
                f'A tenant with slug "{tenant.slug}" already exists.')

        tenant.id = tenant_dict.get('id', self.identifier.generate_id())
        tenant.data = tenant_dict.get('data', self.provisioner.location)
        self.provisioner.provision_tenant(tenant)
        self.cataloguer.add_tenant(tenant)
