
"""
This file implements the authentication backend for the openedx platform.
"""
import logging
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from eox_tenant.edxapp_wrapper.auth import get_edx_auth_backend, get_edx_auth_failed

EdxAuthBackend = get_edx_auth_backend()
AuthFailedError = get_edx_auth_failed()
AUDIT_LOG = logging.getLogger("audit")
UserModel = get_user_model()


class TenantAuthBackend(EdxAuthBackend):
    """
    Authentication Backend class which will check if the user has a signupsource in the requested site.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Override default method to use the method user_can_authenticate_on_tenant()
        """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)  # pylint: disable=protected-access

        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate_on_tenant(user, request):
                return user

    def user_can_authenticate_on_tenant(self, user, request):
        """
        Prevents users that signed up on a different tenant site to login in this site.
        """
        current_domain = request.META.get("HTTP_HOST")

        authorized_sources = getattr(settings, 'EDNX_ACCOUNT_REGISTRATION_SOURCES', [current_domain])
        sources = user.usersignupsource_set.all()

        is_authorized = False
        for source in sources:
            if any(re.match(pattern + "$", source.site) for pattern in authorized_sources):
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
                AUDIT_LOG.warning(
                    u"User `%s` tried to login in site `%s`, but was denied permission based on the signup sources.",
                    loggable_id,
                    current_domain,
                )
                raise AuthFailedError(_('User not authorized to perform this action'))
            else:
                AUDIT_LOG.warning(
                    u"User `%s` tried to login in site `%s`, the permission "
                    "should have beed denied based on the signup sources.",
                    loggable_id,
                    current_domain,
                )
        return True
