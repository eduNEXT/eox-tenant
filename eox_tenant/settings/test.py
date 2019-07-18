"""
Common settings for eox_tenant project.
"""

from .common import *   # pylint: disable=wildcard-import


class SettingsClass(object):
    """ dummy settings class """
    pass


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get("INSTALLED_APPS", [])
TEST_INSTALLED_APPS = [
    "django.contrib.sites",
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_test_v1'

TEST_DICT_OVERRIDE_TEST = {
    "key1": "Some Value"
}


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests, we want everything to be disabled
    """

    settings.MICROSITE_BACKEND = 'eox_tenant.backends.base.BaseMicrositeBackend'
    settings.MICROSITE_TEMPLATE_BACKEND = \
        'eox_tenant.backends.base.BaseMicrositeTemplateBackend'
    settings.FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
    settings.FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False
    settings.EOX_TENANT_SKIP_FILTER_FOR_TESTS = True
