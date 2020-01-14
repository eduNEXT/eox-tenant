"""
Eox Tenant Wise.
==================
This module makes it possible to override the some platform Models using new proxy models.
"""
from importlib import import_module

import six
from django.conf import settings

from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy, TenantGeneratedCertificateProxy


def load_tenant_wise_overrides():
    """
    Here are all the necessary overrides for the platform models.
    """
    if getattr(settings, 'USE_EOX_TENANT', False):
        allowed_proxies = getattr(settings, 'TENANT_WISE_ALLOWED_PROXIES', {})

        if allowed_proxies.get('TenantSiteConfigProxy'):
            set_as_proxy(
                modules='openedx.core.djangoapps.site_configuration.models',
                model='SiteConfiguration',
                proxy=TenantSiteConfigProxy
            )

        if allowed_proxies.get('TenantGeneratedCertificateProxy'):
            certificate_list = [
                'lms.djangoapps.certificates.models',
                'lms.djangoapps.certificates.queue',
            ]

            set_as_proxy(
                modules=certificate_list,
                model='GeneratedCertificate',
                proxy=TenantGeneratedCertificateProxy
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
