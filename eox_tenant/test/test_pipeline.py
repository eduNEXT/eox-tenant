#!/usr/bin/python
"""
Tests for the pipeline module used in multi-tenant third party auth.
"""
from django.test import TestCase
from mock import MagicMock

from eox_tenant.pipeline import EoxTenantAuthException, safer_associate_by_email


class AssociationByEmailTest(TestCase):
    """
    Test the custom association backend.
    """

    def setUp(self):
        self.backend_mock = MagicMock()
        self.user_mock = MagicMock()
        self.backend_mock.strategy.storage.user.get_users_by_email.return_value = [self.user_mock]

    def test_regular_user_works(self):
        """
        A non admin user will be assigned and returned.
        """
        self.user_mock.is_staff = False
        self.user_mock.is_superuser = False
        result = safer_associate_by_email(self.backend_mock, {'email': 'fake@example.com'})
        self.assertEqual(self.user_mock, result['user'])

    def test_staff_user_fails(self):
        """
        A user with a global staff flag cant be assigned.
        """
        self.user_mock.is_staff = True
        self.user_mock.is_superuser = False
        with self.assertRaises(EoxTenantAuthException):
            safer_associate_by_email(self.backend_mock, {'email': 'fake@example.com'})

    def test_superadmin_user_fails(self):
        """
        A superuser cant be assigned.
        """
        self.user_mock.is_staff = False
        self.user_mock.is_superuser = True
        with self.assertRaises(EoxTenantAuthException):
            safer_associate_by_email(self.backend_mock, {'email': 'fake@example.com'})
