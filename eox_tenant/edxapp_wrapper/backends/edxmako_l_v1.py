""" Backend abstraction. """

from common.djangoapps import edxmako  # pylint: disable=import-error


def get_edxmako_module():
    """ Backend to get edxmako module. """
    return edxmako
