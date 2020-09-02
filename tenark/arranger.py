from typing import Dict, Any
from .models import Tenant
from .cataloguer import Cataloguer
from .provisioner import Provisioner
from .identifier import Identifier
from .common import QueryDomain, TenantCreationError, TenantRetrievalError


class Arranger:
    def __init__(self, cataloguer: Cataloguer,
                 provisioner: Provisioner,
                 identifier: Identifier) -> None:
        self.cataloguer = cataloguer
        self.provisioner = provisioner
        self.identifier = identifier

    def ensure_tenant(self, tenant_dict: Dict[str, Any]) -> Dict[str, Any]:
        tenant_id = tenant_dict.get('id', '')
        try:
            result = self.cataloguer.get_tenant(tenant_id)
            return vars(result)
        except TenantRetrievalError:
            self.create_tenant(tenant_dict)
            return vars(self.cataloguer.get_tenant(tenant_id))

    def create_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        tenant_dict.setdefault('id', self.identifier.generate_id())
        tenant = Tenant(**tenant_dict)
        domain: QueryDomain = [
            '|', ('slug', '=', tenant.slug), ('name', '=', tenant.name)]

        self.cataloguer.load()
        duplicates = self.cataloguer.search_tenants(domain)

        if duplicates:
            duplicate_ids = [duplicate.id for duplicate in duplicates]
            if tenant_dict['id'] in duplicate_ids:
                return
            raise TenantCreationError(
                f'A tenant with slug "{tenant.slug}" already exists.')

        self.provisioner.provision_tenant(tenant)
        self.cataloguer.add_tenant(tenant)
