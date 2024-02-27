#!/usr/bin/python
"""
Tests for the async_utils module.
"""
from django.contrib.sites.models import Site
from django.test import TestCase
from mock import patch

from eox_tenant.async_utils import AsyncTaskHandler


class AsyncTaskHandlerTests(TestCase):
    """
    Testing the AsyncTaskHandler class.
    """

    def setUp(self):
        """ setup """
        for number in range(3):
            Site.objects.create(
                domain=f"tenant{number}.com",
                name=f"tenant{number}.com"
            )

    def test_get_host_from_siteid(self):
        """
        Test method used to get host from siteid
        """
        func = AsyncTaskHandler().get_host_from_siteid()
        site = Site.objects.get(domain="tenant2.com")
        body = {}
        body['args'] = (site.id, None, None)
        hostname = func(body)
        self.assertEqual(hostname, "tenant2.com")

    @patch('eox_tenant.signals._perform_reset')
    @patch('eox_tenant.signals._update_settings')
    def test_get_host_from_invalid_siteid(self, _update_mock, _reset_mock):
        """
        In case of invalid tenant the hostname should be None.
        """
        func = AsyncTaskHandler().get_host_from_siteid()
        body = {}
        body['args'] = (10, None, None)
        hostname = func(body)

        self.assertIsNone(hostname)
