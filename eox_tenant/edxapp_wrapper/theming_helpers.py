""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_theming_helpers(*args, **kwargs):
    """ Get BaseMicrositeBackend. """
    backend_function = settings.GET_THEMING_HELPERS
    backend = import_module(backend_function)
    return backend.get_theming_helpers(*args, **kwargs)
