""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_edxmako_module():
    """ Get edxmako module. """
    backend_function = settings.EDXMAKO_MODULE_BACKEND
    backend = import_module(backend_function)
    return backend.get_edxmako_module()
