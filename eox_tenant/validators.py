"""
This overwrites the EdxOAuth2Validator behavior
"""
import logging

from crum import get_current_request
from django.conf import settings

from eox_tenant.edxapp_wrapper.oauth_dispatch import get_edx_oauth2_validator_class

EdxOAuth2Validator = get_edx_oauth2_validator_class()
logger = logging.getLogger(__name__)


class EoxTenantOAuth2Validator(EdxOAuth2Validator):
    """Class that restricts the token creation, the creation is restricted to the application redirect uris
    hence the current url request must be in the redirect_uris value in order to create a new token otherwise
    a 401 response will be returned.
    """

    def _load_application(self, client_id, request):
        """Return the application if the current url is allowed."""
        current_url = get_current_request().build_absolute_uri('/')
        allowed_applications = getattr(settings, 'ALLOWED_AUTH_APPLICATIONS', [])
        application = super()._load_application(client_id, request)

        if not application:
            return None

        application_name = application.name

        if application.redirect_uri_allowed(current_url) or application_name in allowed_applications:
            return application

        logger.warning(
            'The application <%s> has not been configured with the url <%s>',
            application_name,
            current_url,
        )

        return None
