"""
Common settings for eox_tenant project.
"""

from path import Path as path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eox_tenant',
    'organizations',
]

TIME_ZONE = 'UTC'

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Plugin settings.
    settings.CONTENTSTORE_PATH = 'cms.djangoapps.contentstore.utils'
    settings.EOX_TENANT_CACHE_KEY_TIMEOUT = 300
    settings.GET_OAUTH_DISPATCH_BACKEND = 'eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1'
    settings.GET_BRANDING_API = 'eox_tenant.edxapp_wrapper.backends.branding_api_l_v1'
    settings.GET_SITE_CONFIGURATION_MODULE = 'eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1'
    settings.GET_THEMING_HELPERS = 'eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1'
    settings.EOX_TENANT_EDX_AUTH_BACKEND = "eox_tenant.edxapp_wrapper.backends.edx_auth_n_v1"
    settings.EOX_TENANT_USERS_BACKEND = 'eox_tenant.edxapp_wrapper.backends.users_p_v1'
    settings.EOX_TENANT_BEARER_AUTHENTICATION = 'eox_tenant.edxapp_wrapper.backends.bearer_authentication_l_v1'
    settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS = 300
    settings.EDXMAKO_MODULE_BACKEND = 'eox_tenant.edxapp_wrapper.backends.edxmako_l_v1'
    settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME = "stage.edunext.co"
    settings.EOX_TENANT_LOAD_PERMISSIONS = True
    settings.EOX_TENANT_APPEND_LMS_MIDDLEWARE_CLASSES = False
    settings.USE_EOX_TENANT = True

    settings.EOX_TENANT_ASYNC_TASKS_HANDLER_DICT = {
        "openedx.core.djangoapps.schedules.tasks.ScheduleRecurringNudge": "get_host_from_siteid",
    }
    settings.TENANT_WISE_ALLOWED_PROXIES = {
        'TenantSiteConfigProxy': True,
    }

    if hasattr(settings, 'OAUTH2_PROVIDER'):
        settings.OAUTH2_PROVIDER['OAUTH2_VALIDATOR_CLASS'] = 'eox_tenant.validators.EoxTenantOAuth2Validator'

    try:
        settings.MAKO_TEMPLATE_DIRS_BASE.insert(0, path(__file__).abspath().dirname().dirname() / 'templates')
    except AttributeError:
        pass

    settings.EOX_TENANT_RESTRICTED_COURSE_PATTERNS = [
        "courses",
        "(api/course_home/.+)",
    ]
