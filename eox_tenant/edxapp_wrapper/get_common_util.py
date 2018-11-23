""" This module contains functions that we can safely define locally """


def strip_port_from_host(host):
    """
    As it would have been in util.url.strip_port_from_host
    """
    return host.split(':')[0]
