""" Backend abstraction. """
from importlib import import_module
from django.conf import settings


def get_strip_port_from_host(*args, **kwargs):
    """ Get get_strip_port_from_host. """
    backend_function = settings.COMMON_UTIL
    backend = import_module(backend_function)
    return backend.get_strip_port_from_host(*args, **kwargs)
