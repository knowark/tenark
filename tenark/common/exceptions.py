
class TenarkError(Exception):
    """Tenark's base error class."""


# Tenancy

class TenantError(TenarkError):
    """Tenancy base error class."""


class TenantLocationError(TenantError):
    """The tenant location type was not found."""


class TenantCreationError(TenantError):
    """The tenant couldn't be created."""


class TenantRetrievalError(TenantError):
    """The tenant couldn't be found."""


class TenantProvisionError(TenantError):
    """The tenant couldn't be provisioned."""


class TenantCatalogError(TenantError):
    """The tenant couldn't be provisioned."""
