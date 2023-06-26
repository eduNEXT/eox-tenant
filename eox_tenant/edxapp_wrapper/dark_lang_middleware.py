""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_dark_lang_middleware(*args, **kwargs):
    """ Get DarkLangMiddleware. """
    backend_function = settings.DARK_LANG_MIDDLEWARE
    backend = import_module(backend_function)
    return backend.get_dark_lang_middleware(*args, **kwargs)
