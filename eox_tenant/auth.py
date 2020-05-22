
"""
This file implements the authentication backend for the openedx platform.
"""
import logging
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from eox_tenant.edxapp_wrapper.auth import get_edx_auth_backend, get_edx_auth_failed
from eox_tenant.edxapp_wrapper.theming_helpers import get_theming_helpers
from eox_tenant.permissions import LOGIN_ALL_TENANTS_PERMISSION_NAME

AuthFailedError = get_edx_auth_failed()
AUDIT_LOG = logging.getLogger("audit")
EdxAuthBackend = get_edx_auth_backend()
UserModel = get_user_model()
theming_helpers = get_theming_helpers()


class TenantAwareAuthBackend(EdxAuthBackend):
    """
    Authentication Backend class which will check if the user has a signupsource in the requested site.
    """
    def user_can_authenticate(self, user):
        """
        Override user_can_authenticate method with the logic to be tenant aware.
        """
        # List storing validations applied
        validations = []
        # Run the default validation from the parent class and add it to the validations list
        user_can_authenticate = super(TenantAwareAuthBackend, self).user_can_authenticate(user)
        validations.append(user_can_authenticate)

        # Perform the custom auth-on-tenant validation
        can_auth_on_tenant = self.user_can_authenticate_on_tenant(user)
        validations.append(can_auth_on_tenant)

        # All validations must return True
        return all(validations)

    def user_can_authenticate_on_tenant(self, user):
        """
        Prevent users that signed up on a different tenant site to login in this site.
        """
        # Check if the user has a permission to login to all tenants
        if user.has_perm(LOGIN_ALL_TENANTS_PERMISSION_NAME):
            return True

        request = theming_helpers.get_current_request()
        # If this is not executed in the scope of a request, just allow the authentication
        if not request:
            return True

        current_domain = request.META.get("HTTP_HOST")

        authorized_sources = getattr(settings, 'EDNX_ACCOUNT_REGISTRATION_SOURCES', [current_domain])
        sources = user.usersignupsource_set.all()

        is_authorized = False
        for source in sources:
            if any(re.match(pattern + "$", source.site, re.IGNORECASE) for pattern in authorized_sources):
                is_authorized = True

        email = getattr(user, 'email', None)
        if settings.REGISTRATION_EMAIL_PATTERNS_ALLOWED is not None:
            # Taken from forms.AccountCreationForm
            allowed_patterns = settings.REGISTRATION_EMAIL_PATTERNS_ALLOWED
            if not any(re.match(pattern + "$", email) for pattern in allowed_patterns):
                # This email is not on the whitelist of allowed emails.
                is_authorized = False

        if not is_authorized:
            loggable_id = user.id if user else "<unknown>"
            if settings.FEATURES.get('EDNX_ENABLE_STRICT_LOGIN', False):
                # Only if the EDNX_ENABLE_STRICT_LOGIN feature flag is active, an exception is raised when
                # the user is not authorized to login to the current tenant. The exception error message is
                # displayed on the standard login page
                AUDIT_LOG.warning(
                    u"User `%s` tried to login in site `%s`, but was denied permission based on the signup sources.",
                    loggable_id,
                    current_domain,
                )
                raise AuthFailedError(_('User not authorized to perform this action'))
            else:
                AUDIT_LOG.warning(
                    u"User `%s` tried to login in site `%s`, the permission "
                    "should have been denied based on the signup sources.",
                    loggable_id,
                    current_domain,
                )
        return True
