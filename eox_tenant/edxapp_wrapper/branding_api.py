""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_branding_api(*args, **kwargs):
    """ Get BaseMicrositeBackend. """
    backend_function = settings.GET_BRANDING_API
    backend = import_module(backend_function)
    return backend.get_branding_api(*args, **kwargs)
