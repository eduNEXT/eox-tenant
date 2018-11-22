"""
Common settings for eox_tenant project.
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = ()

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
    # Backends settings
    settings.MICROSITE_BACKEND = 'eox_tenant.backends.database.EdunextCompatibleDatabaseMicrositeBackend'
    settings.MICROSITE_TEMPLATE_BACKEND = 'eox_tenant.backends.filebased.EdunextCompatibleFilebasedMicrositeTemplateBackend'
    settings.MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_h_v1'
    settings.COMMON_UTIL = 'eox_tenant.edxapp_wrapper.backends.common_util_h_v1'

    settings.EOX_MAX_CONFIG_OVERRIDE_SECONDS = 300
