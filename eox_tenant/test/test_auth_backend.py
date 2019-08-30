#!/usr/bin/python
"""
Module for Auth backend tests.
"""
import mock

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, override_settings


class TenantAwareAuthBackendTest(TestCase):
    """
    Test tenant aware auth backend.
    """
    def setUp(self):
        """ setup """
        self.request_factory = RequestFactory()

        self.user = User.objects.create_user(
            username='validuser',
            password='12345',
            email='user@valid.domain.org',
        )

        usersignup_source = mock.MagicMock()
        usersignup_source.site = 'valid.domain.org'

        usersignup_source_set = mock.MagicMock()
        usersignup_source_set.all.return_value = [usersignup_source]

        self.user.usersignupsource_set = usersignup_source_set

    @override_settings(
        REGISTRATION_EMAIL_PATTERNS_ALLOWED=None,
        FEATURES={
            'EDNX_ENABLE_STRICT_LOGIN': True
        })
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_failed')
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_backend')
    def test_authentication_with_signupsource(self, edx_auth_backend_mock, edx_auth_failed_mock):
        """
        Test if the user can authenticate in a domain where the user has signupsource
        """
        edx_auth_backend_mock.return_value = object
        edx_auth_failed_mock.return_value = Exception

        from eox_tenant.auth import TenantAwareAuthBackend

        request = self.request_factory.get('/login')

        http_host = 'valid.domain.org'
        request.META['HTTP_HOST'] = http_host

        auth_backend = TenantAwareAuthBackend()
        auth_backend.request = request

        user_can_authenticate_on_tenant = auth_backend.user_can_authenticate_on_tenant(self.user)

        self.assertTrue(user_can_authenticate_on_tenant)

    @override_settings(
        REGISTRATION_EMAIL_PATTERNS_ALLOWED=None,
        FEATURES={
            'EDNX_ENABLE_STRICT_LOGIN': True
        })
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_failed')
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_backend')
    def test_authentication_without_signupsource(self, edx_auth_backend_mock, edx_auth_failed_mock):
        """
        Test if the user can authenticate in a domain where the user does not have signupsource
        """
        edx_auth_backend_mock.return_value = object
        edx_auth_failed_mock.return_value = Exception

        from eox_tenant.auth import TenantAwareAuthBackend

        request = self.request_factory.get('/login')

        http_host = 'invalid.domain.org'
        request.META['HTTP_HOST'] = http_host

        auth_backend = TenantAwareAuthBackend()
        auth_backend.request = request

        with self.assertRaises(Exception):
            auth_backend.user_can_authenticate_on_tenant(self.user)

    @override_settings(
        REGISTRATION_EMAIL_PATTERNS_ALLOWED=[
            "^.*@valid\\.domain\\.org$",
        ],
        FEATURES={
            'EDNX_ENABLE_STRICT_LOGIN': True
        })
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_failed')
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_backend')
    def test_authentication_allowed_patterns(self, edx_auth_backend_mock, edx_auth_failed_mock):
        """
        Test if the user can authenticate using an email that matches with the allowed patterns
        """
        edx_auth_backend_mock.return_value = object
        edx_auth_failed_mock.return_value = Exception

        from eox_tenant.auth import TenantAwareAuthBackend

        request = self.request_factory.get('/login')

        http_host = 'valid.domain.org'
        request.META['HTTP_HOST'] = http_host

        auth_backend = TenantAwareAuthBackend()
        auth_backend.request = request

        user_can_authenticate_on_tenant = auth_backend.user_can_authenticate_on_tenant(self.user)

        self.assertTrue(user_can_authenticate_on_tenant)

    @override_settings(
        REGISTRATION_EMAIL_PATTERNS_ALLOWED=[
            "^.*@invalid\\.domain\\.org$",
        ],
        FEATURES={
            'EDNX_ENABLE_STRICT_LOGIN': True
        })
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_failed')
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_backend')
    def test_authentication_without_allowed_patterns(self, edx_auth_backend_mock, edx_auth_failed_mock):
        """
        Test if the user can authenticate using an email that does not match with the allowed patterns
        """
        edx_auth_backend_mock.return_value = object
        edx_auth_failed_mock.return_value = Exception

        from eox_tenant.auth import TenantAwareAuthBackend

        request = self.request_factory.get('/login')

        http_host = 'valid.domain.org'
        request.META['HTTP_HOST'] = http_host

        auth_backend = TenantAwareAuthBackend()
        auth_backend.request = request

        with self.assertRaises(Exception):
            auth_backend.user_can_authenticate_on_tenant(self.user)

    @override_settings(
        REGISTRATION_EMAIL_PATTERNS_ALLOWED=None,
        FEATURES={
            'EDNX_ENABLE_STRICT_LOGIN': True
        })
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_failed')
    @mock.patch('eox_tenant.edxapp_wrapper.auth.get_edx_auth_backend')
    def test_authentication_with_signupsource_is_case_insensitive(self, edx_auth_backend_mock, edx_auth_failed_mock):
        """
        Test if the backend to authenticate a user with signupsource is ignoring case
        """
        edx_auth_backend_mock.return_value = object
        edx_auth_failed_mock.return_value = Exception

        from eox_tenant.auth import TenantAwareAuthBackend

        request = self.request_factory.get('/login')

        http_host = 'VALID.domain.org'
        request.META['HTTP_HOST'] = http_host

        auth_backend = TenantAwareAuthBackend()
        auth_backend.request = request

        user_can_authenticate_on_tenant = auth_backend.user_can_authenticate_on_tenant(self.user)

        self.assertTrue(user_can_authenticate_on_tenant)
