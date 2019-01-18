"""
Common settings for eox_tenant project.
"""

import sys
from path import Path as path
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

EDX_PLATFORM_ROOT = path("/edx/app/edxapp/edx-platform")
COMMON_ROOT = EDX_PLATFORM_ROOT / "common"
OPENEDX_ROOT = EDX_PLATFORM_ROOT / "openedx"
LMS_ROOT = EDX_PLATFORM_ROOT / "lms"

sys.path.append(EDX_PLATFORM_ROOT)
sys.path.append(OPENEDX_ROOT)
sys.path.append(COMMON_ROOT / 'djangoapps')
sys.path.append(LMS_ROOT / 'djangoapps')


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
