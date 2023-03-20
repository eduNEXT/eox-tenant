"""
Permission for eox_tenant api v1.
"""
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import ProgrammingError
from rest_framework import exceptions, permissions


def load_permissions():
    """
    Helper method to load a custom permission on DB that will be
    used to give access to the eox-tenant API.
    """
    try:
        if settings.EOX_TENANT_LOAD_PERMISSIONS:
            try:
                content_type = ContentType.objects.get_for_model(User)
                Permission.objects.get_or_create(
                    codename='can_call_eox_tenant',
                    name='Can access eox-tenant API',
                    content_type=content_type,
                )
            except ProgrammingError:
                # This code runs when the app is loaded, if a migration has not been
                # done a ProgrammingError exception is raised.
                # we are bypassing those cases to let migrations run smoothly.
                pass
    except ImproperlyConfigured:
        pass


class EoxTenantAPIPermission(permissions.BasePermission):
    """
    Defines a custom permissions to access eox-tenant API.
    These permissions make sure that a token is created with the client credentials of the same site is
    being used on, and the user has a valid SignUp source for the site.
    """

    def has_permission(self, request, view):
        """
        To grant access, checks if the requesting user:
            1) it's a staff user
            3) it's calling the API from a site authorized by the auth application or client
            4) has can call eox-tenant API permission
        """
        user = request.user

        if user.is_staff:
            return True

        try:
            application_uri_allowed = request.auth.application.redirect_uri_allowed(request.build_absolute_uri('/'))
        except Exception:  # pylint: disable=broad-except
            application_uri_allowed = False

        try:
            client_url_allowed = request.get_host() in request.auth.client.url
        except Exception:  # pylint: disable=broad-except
            client_url_allowed = False

        if client_url_allowed or application_uri_allowed:
            return user.has_perm('auth.can_call_eox_tenant')

        # If we get here either someone is using a token created on one site in a different site
        # or there was a missconfiguration of the oauth client.
        # we return the most basic message to prevent leaking important information .
        raise exceptions.NotAuthenticated(detail="Invalid token")
