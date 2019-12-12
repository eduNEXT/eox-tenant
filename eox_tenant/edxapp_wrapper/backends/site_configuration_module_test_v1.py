""" Backend test abstraction. """
from eox_tenant.test_utils import TestSiteConfigurationModels


def get_configuration_helpers():
    """ Backend to get the configuration helper. """
    try:
        from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
    except ImportError:
        configuration_helpers = object
    return configuration_helpers


def get_site_configuration_models():
    """ Backend to get the configuration helper. """
    return TestSiteConfigurationModels()
