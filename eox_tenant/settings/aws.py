"""
Settings for eox_tenant project meant to be called on the edx-platform/*/envs/aws.py module
"""

from .common import *  # pylint: disable=wildcard-import


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Backend settings.
    settings.MICROSITE_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'MICROSITE_BACKEND',
        settings.MICROSITE_BACKEND
    )
    settings.MICROSITE_TEMPLATE_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'MICROSITE_TEMPLATE_BACKEND',
        settings.MICROSITE_TEMPLATE_BACKEND
    )
    settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_MAX_CONFIG_OVERRIDE_SECONDS',
        settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS
    )
    settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME = getattr(settings, 'ENV_TOKENS', {}).get(
        'CHANGE_DOMAIN_DEFAULT_SITE_NAME',
        settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME
    )
    settings.MICROSITES_ALL_ORGS_CACHE_KEY_TIMEOUT = getattr(settings, 'ENV_TOKENS', {}).get(
        'MICROSITES_ALL_ORGS_CACHE_KEY_TIMEOUT',
        settings.MICROSITES_ALL_ORGS_CACHE_KEY_TIMEOUT
    )

    if settings.SERVICE_VARIANT == "lms":
        settings.MIDDLEWARE_CLASSES += [
            'eox_tenant.middleware.RedirectionsMiddleware',
            'eox_tenant.middleware.PathRedirectionMiddleware',
            'eox_tenant.middleware.MicrositeCrossBrandingFilterMiddleware',
        ]
