#!/usr/bin/python
"""
Tests the separation layer between edxapp and the plugin
"""
from django.test import TestCase
from mock import patch, Mock

from eox_tenant.edxapp_wrapper import (
    auth,
    branding_api,
    certificates_module,
    edxmako_module,
    get_common_util,
    site_configuration_module,
    users,
)


class AuthTest(TestCase):
    """
    Making sure that the auth backend works
    """

    @patch('eox_tenant.edxapp_wrapper.auth.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        auth.get_edx_auth_backend()

        import_mock.assert_called()
        backend.assert_called()


class BrandingApiTest(TestCase):
    """
    Making sure that the branding API backend works
    """

    @patch('eox_tenant.edxapp_wrapper.branding_api.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        branding_api.get_branding_api()

        import_mock.assert_called()
        backend.assert_called()


class CertificatesTest(TestCase):
    """
    Making sure that the certificates backend works
    """

    @patch('eox_tenant.edxapp_wrapper.certificates_module.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        certificates_module.get_certificates_models()

        import_mock.assert_called()
        backend.assert_called()


class ConfigurationHelpersTest(TestCase):
    """
    Making sure that the configuration_helpers backend works
    """

    @patch('eox_tenant.edxapp_wrapper.site_configuration_module.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        site_configuration_module.get_configuration_helpers()

        import_mock.assert_called()
        backend.assert_called()


class EdxMakoTest(TestCase):
    """
    Making sure that the edxMako backend works
    """

    @patch('eox_tenant.edxapp_wrapper.edxmako_module.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        edxmako_module.get_edxmako_module()

        import_mock.assert_called()
        backend.assert_called()


class UtilsTest(TestCase):
    """
    Making sure that the utils do as they should
    """

    def test_strip_port_from_host(self):
        """
        The function should remove the port
        """
        self.assertEqual(
            get_common_util.strip_port_from_host('host:8000'),
            'host'
        )


class UsersTest(TestCase):
    """
    Making sure that the branding API backend works
    """

    @patch('eox_tenant.edxapp_wrapper.users.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        users.get_user_signup_source()

        import_mock.assert_called()
        backend.assert_called()
