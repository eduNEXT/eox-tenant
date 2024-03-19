""" Backend abstraction. """
from django.contrib.auth.backends import AllowAllUsersModelBackend  # pylint: disable=import-error
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError  # pylint: disable=import-error


def get_edx_auth_backend():
    """ Backend to get the default edx auth backend. """
    return AllowAllUsersModelBackend


def get_edx_auth_failed():
    """ Backend to get the AuthFailedError class. """
    return AuthFailedError
