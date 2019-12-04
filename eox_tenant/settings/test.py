"""
Common settings for eox_tenant project.
"""
from __future__ import absolute_import, unicode_literals

from .common import *   # pylint: disable=wildcard-import


class SettingsClass(object):
    """ dummy settings class """
    pass


SETTINGS = SettingsClass()
# This is executing the plugin_settings method imported from common module
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get('INSTALLED_APPS', [])
TEST_INSTALLED_APPS = [
    'django.contrib.sites',
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_test_v1'
GET_CONFIGURATION_HELPERS = 'eox_tenant.edxapp_wrapper.backends.configuration_helpers_test_v1'
GET_THEMING_HELPERS = 'eox_tenant.edxapp_wrapper.backends.theming_helpers_test_v1'

COURSE_KEY_PATTERN = r'(?P<course_key_string>[^/+]+(/|\+)[^/+]+(/|\+)[^/?]+)'
COURSE_ID_PATTERN = COURSE_KEY_PATTERN.replace('course_key_string', 'course_id')

TEST_DICT_OVERRIDE_TEST = {
    'key1': 'Some Value'
}

EOX_TENANT_SKIP_FILTER_FOR_TESTS = False
EOX_TENANT_LOAD_PERMISSIONS = True

FEATURES = {}
FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests, we want everything to be disabled
    """
    settings.MICROSITE_BACKEND = 'eox_tenant.backends.base.BaseMicrositeBackend'
    settings.FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
    settings.FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False
    settings.GET_CONFIGURATION_HELPERS = 'eox_tenant.edxapp_wrapper.backends.configuration_helpers_test_v1'
    settings.GET_THEMING_HELPERS = 'eox_tenant.edxapp_wrapper.backends.theming_helpers_test_v1'
    settings.EOX_TENANT_SKIP_FILTER_FOR_TESTS = True
    settings.EOX_TENANT_LOAD_PERMISSIONS = False
