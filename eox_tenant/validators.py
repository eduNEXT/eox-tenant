"""
This overwrites the EdxOAuth2Validator behavior
"""
from crum import get_current_request

from eox_tenant.edxapp_wrapper.oauth_dispatch import get_edx_oauth2_validator_class

EdxOAuth2Validator = get_edx_oauth2_validator_class()


class EoxTenantOAuth2Validator(EdxOAuth2Validator):
    """Class that restricts the token creation, the creation is restricted to the application redirect uris
    hence the current url request must be in the redirect_uris value in order to create a new token otherwise
    a 401 response will be returned.
    """

    def _load_application(self, client_id, request):
        """Return the application if the current url is allowed."""
        application = super(EoxTenantOAuth2Validator, self)._load_application(client_id, request)

        if application and application.redirect_uri_allowed(get_current_request().build_absolute_uri('/')):
            return application

        return None
