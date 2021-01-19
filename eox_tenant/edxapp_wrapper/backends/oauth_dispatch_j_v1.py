""" Backend abstraction. """

from openedx.core.djangoapps.oauth_dispatch.dot_overrides.validators import (  # pylint: disable=import-error
    EdxOAuth2Validator,
)


def get_edx_oauth2_validator_class():
    """ Backend to get EdxOAuth2Validator class """
    return EdxOAuth2Validator
