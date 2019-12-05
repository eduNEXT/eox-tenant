#!/usr/bin/python
"""
Tests the separation layer between edxapp and the plugin
"""
from django.test import TestCase
from mock import patch, Mock

from eox_tenant.edxapp_wrapper import (
    configuration_helpers,
    get_common_util,
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
