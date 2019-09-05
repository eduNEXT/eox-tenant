""" Backend abstraction for course enrollments. """
from importlib import import_module
from django.conf import settings


def get_enrollments_model(*args, **kwargs):
    """ Call the enrollments backend function to get the enrollment model object. """
    backend_function = settings.EOX_TENANT_ENROLLMENTS_BACKEND
    backend = import_module(backend_function)
    return backend.get_enrollments_model(*args, **kwargs)


def get_enrollments_model_manager(*args, **kwargs):
    """ Call the enrollments backend function to get the enrollment model manager object. """
    backend_function = settings.EOX_TENANT_ENROLLMENTS_BACKEND
    backend = import_module(backend_function)
    return backend.get_enrollments_model_manager(*args, **kwargs)
