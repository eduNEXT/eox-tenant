"""
Common settings for eox_tenant project.
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eox_tenant'
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
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    # Plugin settings.
    settings.MICROSITE_BACKEND = 'eox_tenant.backends.database.EdunextCompatibleDatabaseMicrositeBackend'
    settings.MICROSITE_TEMPLATE_BACKEND = \
        'eox_tenant.backends.filebased.EdunextCompatibleFilebasedMicrositeTemplateBackend'
    settings.MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_h_v1'
    settings.MICROSITES_ALL_ORGS_CACHE_KEY_TIMEOUT = 300
    settings.GET_CONFIGURATION_HELPERS = 'eox_tenant.edxapp_wrapper.backends.configuration_helpers_h_v1'
    settings.GET_BRANDING_API = 'eox_tenant.edxapp_wrapper.backends.branding_api_h_v1'
    settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS = 300
    settings.EDXMAKO_MODULE_BACKEND = 'eox_tenant.edxapp_wrapper.backends.edxmako_h_v1'
    settings.UTILS_MODULE_BACKEND = 'eox_tenant.edxapp_wrapper.backends.util_h_v1'
    settings.CHANGE_DOMAIN_DEFAULT_SITE_NAME = "stage.edunext.co"
