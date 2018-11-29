""" Backend abstraction. """

from util.cache import cache  # pylint: disable=import-error
from util.memcache import fasthash  # pylint: disable=import-error


def get_util_cache():
    """ Backend to get util cache definition. """
    return cache


def get_util_memcache_fasthash(*args, **kwargs):
    """ Backend to get memcache fasthash function. """
    return fasthash(*args, **kwargs)
