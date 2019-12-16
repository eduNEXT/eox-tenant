""" backend """
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers  # pylint: disable=import-error
from openedx.core.djangoapps.site_configuration import models  # pylint: disable=import-error


def get_configuration_helpers():
    """ backend function """
    return configuration_helpers


def get_site_configuration_models():
    """
    Backend function.

    Return <openedx.core.djangoapps.site_configuration.models>.
    """
    return models
