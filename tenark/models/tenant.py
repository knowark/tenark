import time
import unicodedata
from typing import Mapping
from ..common import TenantLocationError, TenantCreationError


class Tenant:
    def __init__(self, **attributes):
        now = int(time.time())
        self.id = attributes.get('id', '')
        self.created_at = now
        self.updated_at = now
        self.name = attributes['name']
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
        self.slug = self._normalize_slug(attributes.get('slug', self.name))
        self.attributes = attributes.get('attributes', {})
        self.data: Mapping[str, str] = attributes.get('data', {
            'memory': self.slug
        })

    def location(self, type: str = 'memory') -> str:
        if type not in self.data:
            raise TenantLocationError(
                f"No location found for '{type}' type "
                f"in tenant '{self.name}'.")
        return self.data[type]

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        stripped_slug = slug.strip().replace(" ", "_").lower()
        normalized_slug = unicodedata.normalize(
            'NFKD', stripped_slug).encode('ascii', 'ignore').decode('utf-8')
        if not normalized_slug:
            raise TenantCreationError("Invalid tenant 'slug' name.")
        return normalized_slug
