#!/usr/bin/python
"""
This file implements a class which is a handy utility to make any
call to the settings completely microsite aware by replacing the:
from django.conf import settings
with:
from openedx.conf import settings
"""
from django.conf import settings as base_settings

from eox_tenant.edxapp_wrapper.get_microsite_configuration import get_microsite

MICROSITE = get_microsite()


class MicrositeAwareSettings(object):
    """
    This class is a proxy object of the settings object from django.
    It will try to get a value from the microsite and default to the
    django settings
    """

    def __getattr__(self, name):
        try:
            if isinstance(MICROSITE.get_value(name), dict):
                return MICROSITE.get_dict(name, getattr(base_settings, name, None))
            return MICROSITE.get_value(name, getattr(base_settings, name))
        except KeyError:
            return getattr(base_settings, name)


settings = MicrositeAwareSettings()  # pylint: disable=invalid-name
