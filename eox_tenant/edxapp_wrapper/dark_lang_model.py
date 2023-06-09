""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_dark_lang_config_model():
    """ Get DarkLangConfig function. """
    backend_function = settings.EOX_TENANT_DARK_LANG
    backend = import_module(backend_function)
    return backend.get_dark_lang_config_model()
