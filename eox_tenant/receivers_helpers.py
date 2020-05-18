"""
Common utilities for use along signals file.
"""
from django.conf import settings

from eox_tenant.models import Microsite, TenantConfig


def get_tenant_config_by_domain(domain):
    """
    Reach for the configuration for a given domain.

    **Arguments**
        domain: String parameter.

    **Returns**
        configurations: dict
        external_key: String
    """
    if not getattr(settings, 'USE_EOX_TENANT', False):
        return {}, None

    configurations, external_key = TenantConfig.get_configs_for_domain(domain)

    if configurations and external_key:
        return configurations, external_key

    microsite = Microsite.get_microsite_for_domain(domain)

    if microsite:
        configurations = microsite.values
        external_key = microsite.key

    return configurations, external_key
