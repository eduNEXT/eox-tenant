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
from eox_tenant.tenant_wise.proxies import TenantGeneratedCertificateProxy, TenantSiteConfigProxy


def load_tenant_wise_overrides():
    """
    Here are all the necessary overrides for the platform models.
    """
    if getattr(settings, 'USE_EOX_TENANT', False):
        allowed_proxies = getattr(settings, 'TENANT_WISE_ALLOWED_PROXIES', {})

        if allowed_proxies.get('TenantSiteConfigProxy'):
            modules = ['openedx.core.djangoapps.site_configuration.models']

            if not LMS_ENVIRONMENT:
                modules.append('contentstore.utils')

            set_as_proxy(
                modules=modules,
                model='SiteConfiguration',
                proxy=TenantSiteConfigProxy
            )

        if allowed_proxies.get('TenantGeneratedCertificateProxy') and LMS_ENVIRONMENT:
            set_package_members_as_proxy(
                package_name='lms.djangoapps.certificates',
                model='GeneratedCertificate',
                proxy=TenantGeneratedCertificateProxy,
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


def set_package_members_as_proxy(package_name, model, proxy):
    """
    Get the modules from the given package and set every one as a proxy.

    Args:
        package_name: String with the package name, example 'lms.djangoapps.courseware'.
        model: String The model name, example User.
        proxy: Class of proxy model example TenantGeneratedCertificateProxy.
    Returns:
        None
    """
    package = import_module(package_name)
    package_members = inspect.getmembers(package)

    set_as_proxy(
        modules=[member[1].__name__ for member in package_members if hasattr(member[1], model)],
        model=model,
        proxy=proxy
    )
