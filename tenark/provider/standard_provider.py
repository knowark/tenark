from threading import local
from ..models import Tenant
from .provider import Provider


class StandardProvider(Provider):

    def __init__(self, tenant=None) -> None:
        self.state = local()
        self.state.__dict__.setdefault('tenant', tenant)

    def setup(self, tenant: Tenant) -> None:
        self.state.tenant = tenant

    def get_tenant(self) -> Tenant:
        if not self.state.tenant:
            raise ValueError('No tenant has been set.')
        return self.state.tenant
