""" Backend abstraction. """
from importlib import import_module

from django.conf import settings


def get_language_preference_middleware(*args, **kwargs):
    """ Get DarkLangMiddleware. """
    backend_function = settings.LANGUAGE_PREFERENCE_MIDDLEWARE
    backend = import_module(backend_function)
    return backend.get_language_preference_middleware(*args, **kwargs)