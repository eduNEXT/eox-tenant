"""
Oauth_dispatchs definitions.
"""

from importlib import import_module

from django.conf import settings


def get_edx_oauth2_validator_class():
    """ Backend to get EdxOAuth2Validator class """
    backend_function = settings.GET_OAUTH_DISPATCH_BACKEND
    backend = import_module(backend_function)

    return backend.get_edx_oauth2_validator_class()
