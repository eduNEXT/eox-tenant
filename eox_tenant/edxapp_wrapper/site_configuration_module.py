""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_configuration_helpers(*args, **kwargs):
    """ Get configuration_helpers function. """
    backend_function = settings.GET_SITE_CONFIGURATION_MODULE
    backend = import_module(backend_function)
    return backend.get_configuration_helpers(*args, **kwargs)


def get_site_configuration_models(*args, **kwargs):
    """ Get the module models from <openedx.core.djangoapps.site_configuration.models>. """
    backend_function = settings.GET_SITE_CONFIGURATION_MODULE
    backend = import_module(backend_function)
    return backend.get_site_configuration_models(*args, **kwargs)
