"""
The pipeline module defines functions that are used in the third party authentication flow
"""
from social_core.exceptions import AuthFailed


class EoxTenantAuthException(AuthFailed):
    """Auth process exception."""

    def __init__(self, backend, *args, **kwargs):
        self.backend = backend
        super().__init__(*args, **kwargs)


# pylint: disable=unused-argument,keyword-arg-before-vararg
def safer_associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.
    This pipeline entry is not 100% secure. It is better suited however for the
    multi-tenant case so we allow it for certain tenants.

    It replaces:
    https://github.com/python-social-auth/social-core/blob/master/social_core/pipeline/social_auth.py
    """
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if not users:
            return None
        if len(users) > 1:
            raise EoxTenantAuthException(
                backend,
                'The given email address is associated with another account'
            )
        if users[0].is_staff or users[0].is_superuser:
            raise EoxTenantAuthException(
                backend,
                'It is not allowed to auto associate staff or admin users'
            )
        return {'user': users[0],
                'is_new': False}

    return None
