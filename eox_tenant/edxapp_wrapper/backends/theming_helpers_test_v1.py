""" Backend test abstraction. """
from eox_tenant.test_utils import test_theming_helpers


def get_theming_helpers():
    """ Backend to get the theming helpers. """
    try:
        from openedx.core.djangoapps.theming import helpers as theming_helpers
    except ImportError:
        theming_helpers = test_theming_helpers()
    return theming_helpers
