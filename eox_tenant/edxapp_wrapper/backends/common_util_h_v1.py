""" Backend abstraction. """

from util.url import strip_port_from_host  # pylint: disable=import-error

def get_strip_port_from_host():
    """ Backend to get strip_port_from_host. """
    return strip_port_from_host
