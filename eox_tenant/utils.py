#!/usr/bin/python
"""
"""
import hashlib
import urllib

from django.core import cache

try:
    cache = cache.caches['general']  # pylint: disable=invalid-name
except Exception:
    cache = cache.cache


def fasthash(string):
    """
    Hashes `string` into a string representation of a 128-bit digest.
    """
    md4 = hashlib.new("md4")
    md4.update(string)
    return md4.hexdigest()
