"""
Eox Tenant Monkey Patch
==================
This module makes it possible to override the some platform Models using new proxy models.
"""
from eox_tenant.monkey_patch.monkey_patch_proxys import TenantSiteConfigProxy
from eox_tenant.edxapp_wrapper.site_configuration_module import get_site_configuration_models

SiteConfigurationModels = get_site_configuration_models()


def load_monkey_patchs_overrides():
    """
    Here are all the necessary overrides for the platform models.
    """
    SiteConfigurationModels.SiteConfiguration = TenantSiteConfigProxy
