"""
Settings for eox_tenant project meant to be called on the edx-platform/*/envs/production.py module
"""

from .common import *  # pylint: disable=wildcard-import

EDX_AUTH_BACKEND = 'openedx.core.djangoapps.oauth_dispatch.dot_overrides.backends.EdxRateLimitedAllowAllUsersModelBackend'  # pylint: disable=line-too-long
EOX_TENANT_AUTH_BACKEND = 'eox_tenant.auth.TenantAwareAuthBackend'
DJANGO_CURRENT_SITE_MIDDLEWARE = 'django.contrib.sites.middleware.CurrentSiteMiddleware'

EOX_TENANT_CURRENT_SITE_MIDDLEWARE = 'eox_tenant.middleware.CurrentSiteMiddleware'
EOX_TENANT_MIDDLEWARES = [
    'eox_tenant.middleware.AvailableScreenMiddleware',
    'eox_tenant.middleware.MicrositeCrossBrandingFilterMiddleware',
]


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Backend settings.
    settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_MAX_CONFIG_OVERRIDE_SECONDS',
        settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS
    )
    settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME = getattr(settings, 'ENV_TOKENS', {}).get(
        'CHANGE_DOMAIN_DEFAULT_SITE_NAME',
        settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME
    )
    settings.EOX_TENANT_CACHE_KEY_TIMEOUT = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_CACHE_KEY_TIMEOUT',
        settings.EOX_TENANT_CACHE_KEY_TIMEOUT
    )
    settings.EOX_TENANT_EDX_AUTH_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_EDX_AUTH_BACKEND',
        settings.EOX_TENANT_EDX_AUTH_BACKEND
    )
    settings.EOX_TENANT_USERS_BACKEND = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_USERS_BACKEND',
        settings.EOX_TENANT_USERS_BACKEND
    )
    settings.EOX_TENANT_LOAD_PERMISSIONS = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_LOAD_PERMISSIONS',
        settings.EOX_TENANT_LOAD_PERMISSIONS
    )
    settings.EOX_TENANT_APPEND_LMS_MIDDLEWARE_CLASSES = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_APPEND_LMS_MIDDLEWARE_CLASSES',
        settings.EOX_TENANT_APPEND_LMS_MIDDLEWARE_CLASSES
    )
    settings.EOX_TENANT_ASYNC_TASKS_HANDLER_DICT = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_TENANT_ASYNC_TASKS_HANDLER_DICT',
        settings.EOX_TENANT_ASYNC_TASKS_HANDLER_DICT
    )
    settings.USE_EOX_TENANT = getattr(settings, 'ENV_TOKENS', {}).get(
        'USE_EOX_TENANT',
        settings.USE_EOX_TENANT
    )
    settings.GET_CERTIFICATES_MODULE = getattr(settings, 'ENV_TOKENS', {}).get(
        'GET_CERTIFICATES_MODULE',
        settings.GET_CERTIFICATES_MODULE
    )

    # Override the default site
    settings.SITE_ID = getattr(settings, 'ENV_TOKENS', {}).get(
        'SITE_ID',
        settings.SITE_ID
    )

    settings.TENANT_WISE_ALLOWED_PROXIES = getattr(settings, 'ENV_TOKENS', {}).get(
        'TENANT_WISE_ALLOWED_PROXIES',
        settings.TENANT_WISE_ALLOWED_PROXIES
    )

    # Validate if MIDDLEWARE_CLASSES attribute exists in the environment
    middleware = 'MIDDLEWARE_CLASSES'
    if not hasattr(settings, middleware):
        middleware = 'MIDDLEWARE'

    if DJANGO_CURRENT_SITE_MIDDLEWARE in getattr(settings, middleware) and getattr(settings, 'USE_EOX_TENANT', False):
        middleware_setting = getattr(settings, middleware)
        middleware_setting[getattr(settings, middleware).index(DJANGO_CURRENT_SITE_MIDDLEWARE)] = EOX_TENANT_CURRENT_SITE_MIDDLEWARE  # pylint: disable=line-too-long
        setattr(settings, middleware, middleware_setting)

    if settings.SERVICE_VARIANT == "lms":
        if settings.EOX_TENANT_APPEND_LMS_MIDDLEWARE_CLASSES:
            middleware_setting = getattr(settings, middleware) + EOX_TENANT_MIDDLEWARES
            setattr(settings, middleware, middleware_setting)

        settings.AUTHENTICATION_BACKENDS = [EOX_TENANT_AUTH_BACKEND if (backend == EDX_AUTH_BACKEND) else backend for backend in settings.AUTHENTICATION_BACKENDS]  # pylint: disable=line-too-long
