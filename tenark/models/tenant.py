import time
import unicodedata
from typing import Mapping
from ..common import TenantLocationError, TenantCreationError


class Tenant:
    def __init__(self, **attributes):
        self.id = attributes['id']
        self.created_at = attributes.get('created_at', int(time.time()))
        self.updated_at = attributes.get('updated_at', self.created_at)
        self.name = attributes['name']
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
        self.slug = self._normalize_slug(attributes.get('slug', self.name))
        self.attributes = attributes.get('attributes', {})
        self.zone = attributes.get('zone', '')

    @staticmethod
    def _normalize_slug(slug: str) -> str:
        stripped_slug = slug.strip().replace(" ", "_").lower()
        normalized_slug = unicodedata.normalize(
            'NFKD', stripped_slug).encode('ascii', 'ignore').decode('utf-8')
        if not normalized_slug:
            raise TenantCreationError("Invalid tenant 'slug' name.")
        return normalized_slug
