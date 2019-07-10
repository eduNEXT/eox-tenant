""" Backend test abstraction. """


def get_theming_helpers():
    """ Backend to get the theming helpers. """
    try:
        from openedx.core.djangoapps.theming import helpers as theming_helpers
    except ImportError:
        theming_helpers = object
    return theming_helpers
