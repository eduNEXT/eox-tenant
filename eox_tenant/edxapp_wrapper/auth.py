"""
Auth definitions.
"""

from importlib import import_module
from django.conf import settings


def get_edx_auth_backend():
    """ Gets GeneratedCertificate model. """

    backend_function = settings.EOX_TENANT_EDX_AUTH_BACKEND
    backend = import_module(backend_function)

    return backend.get_edx_auth_backend()


def get_edx_auth_failed():
    """ Gets GeneratedCertificate model. """

    backend_function = settings.EOX_TENANT_EDX_AUTH_BACKEND
    backend = import_module(backend_function)

    return backend.get_edx_auth_failed()
