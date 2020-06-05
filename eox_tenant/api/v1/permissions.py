"""
Permission for eox_tenant api v1.
"""
from rest_framework import permissions


class EoxTenantAPIPermission(permissions.BasePermission):
    """Only allows super user."""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
