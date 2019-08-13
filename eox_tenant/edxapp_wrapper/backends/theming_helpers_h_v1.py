""" backend """
from openedx.core.djangoapps.theming import helpers as theming_helpers  # pylint: disable=import-error


def get_theming_helpers():
    """ backend function """
    return theming_helpers
