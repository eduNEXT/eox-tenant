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

MICROSITE_CONFIGURATION_BACKEND = 'eox_tenant.edxapp_wrapper.backends.microsite_configuration_test_v1'

TEST_DICT_OVERRIDE_TEST = {
    "key1": "Some Value"
}
