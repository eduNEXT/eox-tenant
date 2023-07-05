"""
Eox Tenant Wise.
==================
This module makes it possible to override the some platform Models using new proxy models.
"""
import inspect
from importlib import import_module

import six
from django.conf import settings

from eox_tenant.constants import LMS_ENVIRONMENT
from eox_tenant.tenant_aware_functions.released_languages import tenant_languages
from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy


def load_tenant_wise_overrides():
    """
    Here are all the necessary overrides for the platform models.
    """
    if getattr(settings, 'USE_EOX_TENANT', False):
        allowed_proxies = getattr(settings, 'TENANT_WISE_ALLOWED_PROXIES', {})

        if allowed_proxies.get('TenantSiteConfigProxy'):
            modules = ['openedx.core.djangoapps.site_configuration.models']

            if not LMS_ENVIRONMENT and hasattr(settings, 'CONTENTSTORE_PATH'):
                modules.append(settings.CONTENTSTORE_PATH)

            set_as_proxy(
                modules=modules,
                model='SiteConfiguration',
                proxy=TenantSiteConfigProxy
            )

            if settings.FEATURES.get("EDNX_SITE_AWARE_LOCALE", False):
                set_as_proxy(
                    modules='openedx.core.djangoapps.lang_pref.api',
                    model='released_languages',
                    proxy=tenant_languages
                )


def set_as_proxy(modules, model, proxy):
    """
    Helper to patch a loaded module with a proxy object that has all the Tenant wise properties.
    """
    if isinstance(modules, six.string_types):
        modules = set([modules])

    for module in modules:
        module = import_module(module)
        setattr(module, model, proxy)
