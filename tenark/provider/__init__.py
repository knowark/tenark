from .tenant import Tenant


tenant = None


def get_tenant():
    if not tenant:
        tenant = Tenant()

    return tenant


def reset_tenant():
    tenant = None
