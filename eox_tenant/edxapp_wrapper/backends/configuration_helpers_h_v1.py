""" backend """
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers  # pylint: disable=import-error


def get_configuration_helpers():
    """ backend function """
    return configuration_helpers
