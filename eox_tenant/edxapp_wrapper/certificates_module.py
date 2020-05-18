""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_certificates_models(*args, **kwargs):
    """ Get the module models from <lms.djangoapps.certificates.models>. """
    backend_function = settings.GET_CERTIFICATES_MODULE
    backend = import_module(backend_function)
    return backend.get_certificates_models(*args, **kwargs)
