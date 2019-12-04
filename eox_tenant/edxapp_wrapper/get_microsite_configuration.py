""" Backend abstraction. """
from importlib import import_module
from django.conf import settings


def get_base_microsite_backend(*args, **kwargs):
    """ Get BaseMicrositeBackend. """
    backend_function = settings.MICROSITE_CONFIGURATION_BACKEND
    backend = import_module(backend_function)
    return backend.get_base_microsite_backend(*args, **kwargs)


def get_microsite_get_value(*args, **kwargs):
    """ Get get_value. """
    backend_function = settings.MICROSITE_CONFIGURATION_BACKEND
    backend = import_module(backend_function)
    return backend.get_microsite_get_value(*args, **kwargs)
