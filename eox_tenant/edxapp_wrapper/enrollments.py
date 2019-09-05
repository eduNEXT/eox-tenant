""" Backend abstraction. """
from importlib import import_module
from django.conf import settings


def get_enrollments_model(*args, **kwargs):
    """ Get BaseMicrositeBackend. """
    backend_function = settings.EOX_TENANT_ENROLLMENTS_BACKEND
    backend = import_module(backend_function)
    return backend.get_enrollments_model(*args, **kwargs)


def get_enrollments_model_manager(*args, **kwargs):
    """ Get BaseMicrositeBackend. """
    backend_function = settings.EOX_TENANT_ENROLLMENTS_BACKEND
    backend = import_module(backend_function)
    return backend.get_enrollments_model_manager(*args, **kwargs)
