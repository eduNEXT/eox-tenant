"""
Common settings for eox_tenant project.
"""
import os

from .common import *   # pylint: disable=wildcard-import


class SettingsClass(object):
    """ dummy settings class """
    pass


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)

MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_test_v1'

TEST_DICT_OVERRIDE_TEST = {
    "key1": "Some Value"
}

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests, we want everything to be disabled
    """
    settings.FEATURES['USE_MICROSITE_AVAILABLE_SCREEN'] = False
    settings.FEATURES['USE_REDIRECTION_MIDDLEWARE'] = False
