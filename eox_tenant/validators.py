"""
This overwrites the EdxOAuth2Validator behavior
"""
from crum import get_current_request

from eox_tenant.edxapp_wrapper.oauth_dispatch import get_edx_oauth2_validator_class

EdxOAuth2Validator = get_edx_oauth2_validator_class()


class EoxTenantOAuth2Validator(EdxOAuth2Validator):
    """
    Class that validates the token usage:
        * The token can only be used in the site it was created
    """

    def save_bearer_token(self, token, request, *args, **kwargs):
        """Save the token if the current url is in redirect_uris list."""
        request_uri = get_current_request()

        if request.client.redirect_uri_allowed(request_uri.build_absolute_uri('/')):
            super(EoxTenantOAuth2Validator, self).save_bearer_token(token, request, *args, **kwargs)
