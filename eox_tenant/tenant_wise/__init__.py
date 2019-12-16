"""
Eox Tenant Wise.
==================
This module makes it possible to override the some platform Models using new proxy models.
"""
from eox_tenant.edxapp_wrapper.site_configuration_module import get_site_configuration_models
from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy

SiteConfigurationModels = get_site_configuration_models()


def load_tenant_wise_overrides():
    """
    Here are all the necessary overrides for the platform models.
    """
    SiteConfigurationModels.SiteConfiguration = TenantSiteConfigProxy
