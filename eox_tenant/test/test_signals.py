#!/usr/bin/python
"""
Tests for the signals module
"""
from __future__ import print_function, unicode_literals

from datetime import datetime, timedelta

from django.test import TestCase
from mock import MagicMock, patch

from eox_tenant.signals import (
    start_tenant,
    _ttl_reached,
    _update_settings,
    _analyze_current_settings,
    _repopulate_apps,
)


class StartTenantSignalTest(TestCase):
    """
    Testing the signal sent at the start of every request
    """

    def test_nothing_changes_studio(self):
        """
        The cms should return immediately, just one call must be made it,
        in order to get the HTTP_HOST from environ variable.
        """
        environ = MagicMock()
        with self.settings(SERVICE_VARIANT='cms'):
            start_tenant(None, environ)
            environ.get.assert_called_once()

    @patch('eox_tenant.signals._analyze_current_settings')
    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    def test_must_reset_because_domain(self, _, _reset_mock, _analyze_mock):
        """
        If the analysis determines that a reset is required. It has to be done
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        _analyze_mock.return_value = (True, None)

        with self.settings(SERVICE_VARIANT='lms'):
            start_tenant(None, environ)

        _reset_mock.assert_called()

    @patch('eox_tenant.signals._analyze_current_settings')
    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    @patch('eox_tenant.signals._ttl_reached')
    def test_must_reset_ttl(self, _ttl_mock, _, _reset_mock, _analyze_mock):
        """
        If the ttl determines that a reset is required. It has to be done
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        _analyze_mock.return_value = (False, None)
        _ttl_mock.return_value = True

        with self.settings(SERVICE_VARIANT='lms'):
            start_tenant(None, environ)

        _reset_mock.assert_called()

    @patch('eox_tenant.signals._analyze_current_settings')
    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    def test_can_not_keep_because_analysis(self, _update_mock, _reset_mock, _analyze_mock):
        """
        Unless the domain and current config match, the analysis will always
        determine we can not keep the current settings
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        _analyze_mock.return_value = (False, False)

        with self.settings(SERVICE_VARIANT='lms'):
            start_tenant(None, environ)

        _reset_mock.assert_not_called()
        _update_mock.assert_called()

    @patch('eox_tenant.signals._analyze_current_settings')
    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    def test_can_keep(self, _update_mock, _reset_mock, _analyze_mock):
        """
        When the domain and current config match, the analysis will
        determine that we can keep the current settings
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        _analyze_mock.return_value = (False, True)

        with self.settings(SERVICE_VARIANT='lms'):
            start_tenant(None, environ)

        _reset_mock.assert_not_called()
        _update_mock.assert_not_called()

    def test__ttl_reached(self):
        """
        By default we set 5 minutes as the max time a particular settings override can live
        """
        with self.settings(EDNX_TENANT_SETUP_TIME=(datetime.now() - timedelta(minutes=6))):
            self.assertTrue(_ttl_reached())

        with self.settings(EDNX_TENANT_SETUP_TIME=(datetime.now() - timedelta(minutes=4))):
            self.assertFalse(_ttl_reached())

        self.assertFalse(_ttl_reached())

    def test__analyze_current_settings_no_domain(self):
        """
        The settings for a blank incoming request can not be kept and must not be restarted
        """
        reset, keep = _analyze_current_settings("tenant.com")
        self.assertFalse(reset)
        self.assertFalse(keep)

    def test__analyze_current_settings_incorrect_domain(self):
        """
        The settings a domain with a different domain to the one currently in
        """
        with self.settings(EDNX_TENANT_KEY="different-key",
                           EDNX_TENANT_DOMAIN="different.com"):
            reset, keep = _analyze_current_settings("tenant.com")

        self.assertTrue(reset)
        self.assertFalse(keep)

    def test__analyze_current_settings_correct_domain(self):
        """
        The settings a domain with a matching domain to the one currently in
        """
        with self.settings(EDNX_TENANT_KEY="tenant-key",
                           EDNX_TENANT_DOMAIN="tenant.com"):
            reset, keep = _analyze_current_settings("tenant.com")

        self.assertFalse(reset)
        self.assertTrue(keep)

    @patch('eox_tenant.signals._repopulate_apps')
    def test__repopulate_apps_not_called(self, _repopulate_mock):
        """
        In a tenant that does nothing to define the apps that must be reloaded nothing happens
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        with self.settings(SERVICE_VARIANT='lms'):
            start_tenant(None, environ)

        _repopulate_mock.assert_not_called()

    @patch('eox_tenant.signals._repopulate_apps')
    def test__repopulate_apps_called(self, _repopulate_mock):
        """
        A tenant that defines the EDNX_TENANT_INSTALLED_APPS calls the function
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'

        with self.settings(SERVICE_VARIANT='lms', EDNX_TENANT_INSTALLED_APPS=['fake_app']):
            start_tenant(None, environ)

        _repopulate_mock.assert_called()

    @patch('eox_tenant.signals.AppConfig')
    def test__repopulate_app(self, config_mock):
        """
        Calling _repopulate_apps does the calls mimicking the django registry
        """
        app_config_mock = MagicMock()
        config_mock.create.return_value = app_config_mock

        _repopulate_apps(["fake_app"])

        config_mock.create.assert_called_with("fake_app")
        app_config_mock.ready.assert_called()


class SettingsOverridesTest(TestCase):
    """
    Special test case that modifies the settings object from the testing process
    """

    def tearDown(self):
        """
        Must reset after every test
        """
        from django.conf import settings
        settings._setup()  # pylint: disable=protected-access

    @patch('eox_tenant.signals._get_tenant_config')
    def test_udpate_settings_mark(self, _get_config_mock):
        """
        Settings must only be updated if EDNX_USE_SIGNAL is present
        """
        from django.conf import settings
        config = {
        }
        _get_config_mock.return_value = config, "tenant-key"

        _update_settings("tenant.com")

        with self.assertRaises(AttributeError):
            settings.EDNX_TENANT_KEY  # pylint: disable=pointless-statement

    @patch('eox_tenant.signals._get_tenant_config')
    def test_udpate_settings(self, _get_config_mock):
        """
        Settings must only be updated if EDNX_USE_SIGNAL is present
        """
        from django.conf import settings
        config = {
            "EDNX_USE_SIGNAL": True,
        }
        _get_config_mock.return_value = config, "tenant-key"

        _update_settings("tenant.com")

        settings.EDNX_TENANT_KEY  # pylint: disable=pointless-statement

    @patch('eox_tenant.signals._get_tenant_config')
    def test_udpate_settings_with_property(self, _get_config_mock):
        """
        Settings must only be updated if EDNX_USE_SIGNAL is present
        """
        from django.conf import settings
        config = {
            "EDNX_USE_SIGNAL": True,
            "TEST_PROPERTY": "My value",
        }
        _get_config_mock.return_value = config, "tenant-key"

        _update_settings("tenant.com")

        self.assertEqual(settings.TEST_PROPERTY, "My value")

    @patch('eox_tenant.signals._get_tenant_config')
    def test_udpate_settings_with_dict(self, _get_config_mock):
        """
        Settings must only be updated if EDNX_USE_SIGNAL is present
        """
        from django.conf import settings
        config = {
            "EDNX_USE_SIGNAL": True,
            "TEST_DICT": {
                "TEST_PROPERTY": "My value",
            }
        }
        _get_config_mock.return_value = config, "tenant-key"

        _update_settings("tenant.com")

        self.assertEqual(settings.TEST_DICT.get("TEST_PROPERTY"), "My value")

    @patch('eox_tenant.signals._get_tenant_config')
    def test_udpate_settings_with_existing_dict(self, _get_config_mock):
        """
        Settings must only be updated if EDNX_USE_SIGNAL is present
        """
        from django.conf import settings
        config = {
            "EDNX_USE_SIGNAL": True,
            "TEST_DICT_OVERRIDE_TEST": {
                "key2": "My value",
            }
        }
        _get_config_mock.return_value = config, "tenant-key"

        _update_settings("tenant.com")

        self.assertEqual(settings.TEST_DICT_OVERRIDE_TEST.get("key1"), "Some Value")
        self.assertEqual(settings.TEST_DICT_OVERRIDE_TEST.get("key2"), "My value")
