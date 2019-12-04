#!/usr/bin/python
"""
Tests the separation layer between edxapp and the plugin
"""
from django.test import TestCase
from mock import patch, Mock

from eox_tenant.edxapp_wrapper import (
    configuration_helpers,
    get_common_util,
    get_microsite_configuration,
)


class ConfigurationHelpersTest(TestCase):
    """
    Making sure that the configuration_helpers backend works
    """

    @patch('eox_tenant.edxapp_wrapper.configuration_helpers.import_module')
    def test_imported_module_is_used(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        configuration_helpers.get_configuration_helpers()

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


class MicrositeConfiguratonTest(TestCase):
    """
    Making sure that the utils do as they should
    """

    @patch('eox_tenant.edxapp_wrapper.get_microsite_configuration.import_module')
    def test_imported_module_is_used_at_microsite_backend(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        get_microsite_configuration.get_base_microsite_backend()

        import_mock.assert_called()
        backend.assert_called()

    @patch('eox_tenant.edxapp_wrapper.get_microsite_configuration.import_module')
    def test_imported_module_is_used_at_microsite_get_value(self, import_mock):
        """
        Testing the backend is imported and used
        """
        backend = Mock()
        import_mock.side_effect = backend

        get_microsite_configuration.get_microsite_get_value()

        import_mock.assert_called()
        backend.assert_called()
