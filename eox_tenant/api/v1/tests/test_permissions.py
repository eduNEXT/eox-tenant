#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test module for the permissions class
"""
from unittest.mock import patch

from django.test import TestCase
from mock import MagicMock
from rest_framework.exceptions import NotAuthenticated

from eox_tenant.api.v1.permissions import EoxTenantAPIPermission


class EoxTenantAPIPermissionTest(TestCase):
    """ Test cases for the EoxTenantAPIPermission class."""

    def test_permissions_for_staff(self):
        """ Staff always passes."""
        request = MagicMock()
        request.user.is_staff = True

        has_perm = EoxTenantAPIPermission().has_permission(request, MagicMock())

        self.assertTrue(has_perm)

    @patch.object(EoxTenantAPIPermission, "is_authorized_source_for_user")
    def test_not_authorized_source_for_user(self, mock_is_authorized_source_for_user):
        """ Tests the case where the user has no valid user signUp source with the site
        being used by the request.

        Expected behavior:
            has_permission method returns False
        """
        mock_is_authorized_source_for_user.return_value = False
        request = MagicMock()
        request.user.is_staff = False
        request.user.has_perm.return_value = False

        has_perm = EoxTenantAPIPermission().has_permission(request, MagicMock())

        mock_is_authorized_source_for_user.assert_called_once()
        self.assertFalse(has_perm)

    @patch.object(EoxTenantAPIPermission, "is_authorized_source_for_user")
    def test_read_user_permissions(self, mock_is_authorized_source_for_user):
        """ If the auth does not fail and the user has a valid signUp source,
        it comes down to check the domain in the client or application.

        Expected behavior:
            has_permission method returns False
        """
        mock_is_authorized_source_for_user.return_value = True
        request = MagicMock()
        request.user.is_staff = False
        request.user.has_perm.return_value = False

        has_perm = EoxTenantAPIPermission().has_permission(request, MagicMock())

        mock_is_authorized_source_for_user.assert_called_once()
        self.assertFalse(has_perm)

    @patch.object(EoxTenantAPIPermission, "is_authorized_source_for_user")
    def test_permissions_without_auth(self, mock_is_authorized_source_for_user):
        """ If anything in the auth fails, the NotAuthenticated exception is raised

        Expected behavior:
            NotAuthenticated exception is raised
        """
        mock_is_authorized_source_for_user.return_value = True
        request = MagicMock()
        request.user.is_staff = False
        request.user.has_perm.return_value = False
        request.auth = None

        with self.assertRaises(NotAuthenticated):
            EoxTenantAPIPermission().has_permission(request, MagicMock())

    @patch.object(EoxTenantAPIPermission, "is_authorized_source_for_user")
    def test_permissions_auth_dop(self, mock_is_authorized_source_for_user):
        """ Authorize the domain via the client.url.

        Expected behavior:
            has_permission method returns False
        """
        mock_is_authorized_source_for_user.return_value = True
        request = MagicMock()
        request.user.is_staff = False
        request.user.has_perm.return_value = True
        request.get_host.return_value = "domain.com"
        request.auth.client.url = "https://domain.com/"

        has_perm = EoxTenantAPIPermission().has_permission(request, MagicMock())

        mock_is_authorized_source_for_user.assert_called_once()
        self.assertTrue(has_perm)

    @patch.object(EoxTenantAPIPermission, "is_authorized_source_for_user")
    def test_permissions_auth_dot(self, mock_is_authorized_source_for_user):
        """ Authorize the domain via the application.allowed_uris

        Expected behavior:
            has_permission method returns False
        """
        mock_is_authorized_source_for_user.return_value = True
        request = MagicMock()
        request.user.is_staff = False
        request.user.has_perm.return_value = True
        request.auth.application.redirect_uri_allowed.return_value = True

        has_perm = EoxTenantAPIPermission().has_permission(request, MagicMock())

        mock_is_authorized_source_for_user.assert_called_once()
        self.assertTrue(has_perm)
