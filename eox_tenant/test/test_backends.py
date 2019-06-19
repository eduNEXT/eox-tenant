#!/usr/bin/python
"""
Module for backends tests.
"""
from django.test import TestCase

from eox_tenant.backends.database import EdunextCompatibleDatabaseMicrositeBackend
from eox_tenant.backends.persistent import CompatibleDatabaseSiteConfigBackend


class BackendsTest(TestCase):
    """
    Test backends methods.
    """

    def test_get_config_for_tenant(self):
        """
        Test get configurations.
        """
        backend = CompatibleDatabaseSiteConfigBackend()
        backend.get_config_by_domain("example.domain")

    def test_get_config_for_microsite(self):
        """
        Test get configurations.
        """
        backend = EdunextCompatibleDatabaseMicrositeBackend()
        backend.get_config_by_domain("example.domain")
