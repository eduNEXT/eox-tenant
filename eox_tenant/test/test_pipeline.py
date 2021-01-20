#!/usr/bin/python
"""
Tests for the pipeline module used in multi-tenant third party auth.
"""
from django.test import TestCase
from mock import MagicMock

from eox_tenant.pipeline import EoxTenantAuthException, safer_associate_by_email, safer_associate_by_signupsource


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


class AssociationUserSignUpSoruceTest(TestCase):
    """
    Test association backend by signupsource.
    """
    def setUp(self):
        """setUp."""
        self.request = MagicMock()
        self.request['HTTP_HOST'].return_value = 'valid.domain.org'

        self.backend_mock = MagicMock()
        self.user_mock = MagicMock()

        usersignup_source = MagicMock()
        usersignup_source.site = 'valid.domain.org'

        usersignup_source_set = MagicMock()
        usersignup_source_set.filter.return_value.exists.return_value = True

        self.user_mock.usersignupsource_set = usersignup_source_set
        self.backend_mock.strategy.storage.user.get_users_by_email.return_value = [self.user_mock]

    def test_regular_user_works(self):
        """Works if the user is not admin or staff and has signupsource of the current host."""
        self.user_mock.is_staff = False
        self.user_mock.is_superuser = False

        result = safer_associate_by_signupsource(self.backend_mock, self.request, {'email': 'fake@example.com'})

        self.assertEqual(self.user_mock, result['user'])

    def test_staff_user_fails(self):
        """Fails if user is staff."""
        self.user_mock.is_staff = True
        self.user_mock.is_superuser = False

        with self.assertRaises(EoxTenantAuthException):
            safer_associate_by_signupsource(self.backend_mock, self.request, {'email': 'fake@example.com'})

    def test_superuser_user_fails(self):
        """Fails if user is superuser."""
        self.user_mock.is_staff = False
        self.user_mock.is_superuser = True

        with self.assertRaises(EoxTenantAuthException):
            safer_associate_by_signupsource(self.backend_mock, self.request, {'email': 'fake@example.com'})

    def test_not_allow_microsite_host(self):
        """Fails if user does not belong to current host."""
        self.user_mock.is_staff = False
        self.user_mock.is_superuser = False

        mock_signupsource = MagicMock()
        mock_signupsource.filter.return_value.exists.return_value = False
        self.user_mock.signupsource_set = mock_signupsource
        self.backend_mock.strategy.storage.user.get_users_by_email.return_value = [self.user_mock]

        with self.assertRaises(EoxTenantAuthException):
            safer_associate_by_signupsource(self.backend_mock, self.request, {'email': 'fake@example.com'})
