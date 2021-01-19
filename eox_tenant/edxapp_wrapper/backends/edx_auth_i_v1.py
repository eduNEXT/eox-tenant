""" Backend abstraction. """
from openedx.core.djangoapps.oauth_dispatch.dot_overrides.backends import (  # pylint: disable=import-error
    EdxRateLimitedAllowAllUsersModelBackend,
)
from openedx.core.djangoapps.user_authn.exceptions import AuthFailedError  # pylint: disable=import-error


def get_edx_auth_backend():
    """ Backend to get the default edx auth backend. """
    return EdxRateLimitedAllowAllUsersModelBackend


def get_edx_auth_failed():
    """ Backend to get the AuthFailedError class. """
    return AuthFailedError
