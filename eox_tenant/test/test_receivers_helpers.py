"""
Module for receivers_helpers tests.
"""

from __future__ import absolute_import

from django.test import TestCase

from eox_tenant.models import Microsite, Route, TenantConfig
from eox_tenant.receivers_helpers import get_tenant_config_by_domain


class ReceiversHelpersTests(TestCase):
    """
    Test class for the methods inside the receivers_helpers file.
    """

    def setUp(self):
        """
        Setup database.
        """
        Microsite.objects.create(
            subdomain="first.test.prod.edunext",
            key="test_fake_key",
            values={
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            }
        )

        TenantConfig.objects.create(
            external_key="tenant-key1",
            lms_configs={
                "course_org_filter": ["test5-org", "test1-org"],
                "value-test": "Hello-World3",
            },
            studio_configs={},
            theming_configs={},
            meta={},
        )

        Route.objects.create(
            domain="domain1",
            config=TenantConfig.objects.get(external_key="tenant-key1"),
        )

    def test_tenant_get_config_by_domain(self):
        """
        Test to get the configuration and external key for a given domain.
        """
        configurations, external_key = get_tenant_config_by_domain("domain1")

        self.assertEqual(external_key, "tenant-key1")
        self.assertDictEqual(
            configurations,
            {
                "course_org_filter": ["test5-org", "test1-org"],
                "value-test": "Hello-World3",
            },
        )

        configurations, external_key = get_tenant_config_by_domain("domain2")

        self.assertEqual(external_key, None)
        self.assertDictEqual(configurations, {})

        configurations, external_key = get_tenant_config_by_domain("first.test.prod.edunext")

        self.assertEqual(external_key, "test_fake_key")
        self.assertDictEqual(
            configurations,
            {
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            },
        )
