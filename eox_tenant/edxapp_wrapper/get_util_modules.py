""" Backend abstraction. """
from importlib import import_module
from django.conf import settings


def get_util_cache():
    """ Get util cache definition. """
    backend_function = settings.UTILS_MODULE_BACKEND
    backend = import_module(backend_function)
    return backend.get_util_cache


def get_util_memcache_fasthash(*args, **kwargs):
    """ Get memcache fasthash function. """
    backend_function = settings.UTILS_MODULE_BACKEND
    backend = import_module(backend_function)
    return backend.get_util_memcache_fasthash(*args, **kwargs)
