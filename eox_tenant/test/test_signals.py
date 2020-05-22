#!/usr/bin/python
"""
Tests for the signals module
"""
from __future__ import print_function, unicode_literals

from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.test import TestCase
from mock import MagicMock, patch

from eox_tenant.signals import (
    _analyze_current_settings,
    _repopulate_apps,
    _ttl_reached,
    _update_settings,
    start_async_tenant,
    start_tenant,
    tenant_context_addition,
)


class StartTenantSignalTest(TestCase):
    """
    Testing the signal sent at the start of every request
    """

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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
    @patch('eox_tenant.signals._repopulate_apps')
    def test__repopulate_apps_called(self, _repopulate_mock, _get_config_mock):
        """
        A tenant that defines the EDNX_TENANT_INSTALLED_APPS calls the function
        """
        environ = MagicMock()
        environ.get.return_value = 'tenant.com'
        config = {
            "EDNX_USE_SIGNAL": True,
        }
        _get_config_mock.return_value = config, "tenant-key"

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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
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

    @patch('eox_tenant.signals.get_tenant_config_by_domain')
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


class CeleryReceiverCLISyncTests(TestCase):
    """
    Testing the celery signals generated outside of a request in a sync process.
    """

    def setUp(self):
        """ setup """
        for number in range(3):
            Site.objects.create(
                domain="tenant{number}.com".format(number=number),
                name="tenant{number}.com".format(number=number)
            )

    def test_unknown_task(self):
        """
        When the task is unknown the hostname should be None.
        """
        headers = {}
        body = {}
        tenant_context_addition("uknown_task", headers=headers, body=body)

        self.assertIsNone(headers['eox_tenant_sender'])

    @patch('eox_tenant.async_utils.AsyncTaskHandler.get_host_from_siteid')
    def test_send_recurring_nudge(self, _get_host_mock):
        """
        When the task is called the method get_host_from_siteid should be called.
        """
        headers = {}
        body = {}

        with self.settings():
            tenant_context_addition(
                "openedx.core.djangoapps.schedules.tasks.ScheduleRecurringNudge",
                headers=headers,
                body=body,
            )

        _get_host_mock.assert_called()


class CeleryReceiverSyncTests(TestCase):
    """
    Testing the celery receivers that run in a sync process
    """

    def setUp(self):
        """ setup """
        for number in range(3):
            Site.objects.create(
                domain="tenant{number}.com".format(number=number),
                name="tenant{number}.com".format(number=number)
            )

    def test_sync_process_with_tenant(self):
        """
        When the task is called from a sync proccess it is used the value of the 'host' key in the request dict.
        """
        headers = {}
        body = {}
        with self.settings(EDNX_TENANT_DOMAIN="some.tenant.com"):
            tenant_context_addition("some.task", headers=headers, body=body)

        self.assertEqual(headers['eox_tenant_sender'], 'some.tenant.com')


class CeleryReceiverAsyncTests(TestCase):
    """
    Testing the signal handling in the async process.
    """

    @patch('eox_tenant.signals._update_settings')
    def test_start_async_tenant(self, _update_mock):
        """
        Test function used to handle signal in the async process
        """
        sender = MagicMock()
        headers = {"eox_tenant_sender": "some.tenant.com"}
        sender.request = {"headers": headers}
        start_async_tenant(sender)

        _update_mock.assert_called_with("some.tenant.com")

    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    def test_start_async_tenant_with_null_header(self, _update_mock, _reset_mock):
        """
        Test function used to handle signal in the async process.
        """
        sender = MagicMock()
        headers = None
        sender.request = {"headers": headers}
        start_async_tenant(sender)

        _reset_mock.assert_called()
        _update_mock.assert_not_called()
