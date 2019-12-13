"""
Test file to store the tenant_wise test module.
"""
from __future__ import absolute_import
from django.test import TestCase

from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy
from eox_tenant.models import Microsite, TenantConfig


class TenantSiteConfigProxyTest(TestCase):
    """
    Test TenantSiteConfigProxy.
    """

    def setUp(self):
        """
        This method creates Microsite, TenantConfig and Route objects and in database.
        """
        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext",
            key="test_fake_key",
            values={
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            }
        )

        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="second.test.prod.edunext",
            values={
                "course_org_filter": ["test2-org", "test3-org"],
                "value-test": "Hello-World2",
            }
        )

        TenantConfig.objects.create(
            external_key="tenant-key1",
            lms_configs={
                "course_org_filter": "test4-org"
            },
            studio_configs={},
            theming_configs={},
            meta={},
        )

        TenantConfig.objects.create(
            external_key="tenant-key2",
            lms_configs={
                "course_org_filter": ["test5-org", "test1-org"],
                "value-test": "Hello-World3",
            },
            studio_configs={},
            theming_configs={},
            meta={},
        )

    def test_get_all_orgs(self):
        """
        Test to get all the orgs for Microsite and TenantConfig objects.
        """
        org_list = set([
            "test1-org",
            "test2-org",
            "test3-org",
            "test4-org",
            "test5-org",
        ])

        self.assertTrue(org_list == TenantSiteConfigProxy.get_all_orgs())

    def test_get_value_for_org(self):
        """
        Test to get an specific value for a given org.
        """
        self.assertEqual(
            TenantSiteConfigProxy.get_value_for_org(
                org="test1-org",
                val_name="value-test",
                default=None,
            ),
            "Hello-World3",
        )

        self.assertEqual(
            TenantSiteConfigProxy.get_value_for_org(
                org="test3-org",
                val_name="value-test",
                default=None,
            ),
            "Hello-World2",
        )

        self.assertEqual(
            TenantSiteConfigProxy.get_value_for_org(
                org="test4-org",
                val_name="value-test",
                default="Default",
            ),
            "Default",
        )

    def test_create_site_configuration(self):
        """
        Test that a new TenantSiteConfigProxy instance is created with
        the current settings.
        """
        with self.settings(EDNX_USE_SIGNAL=False):
            site_configuration = TenantSiteConfigProxy()
            self.assertFalse(site_configuration.enabled)
            self.assertFalse(site_configuration.get_value("EDNX_TENANT_KEY"))
            self.assertFalse(site_configuration.get_value("EDNX_USE_SIGNAL"))

        with self.settings(EDNX_TENANT_KEY="test-key", EDNX_USE_SIGNAL=True):
            site_configuration = TenantSiteConfigProxy()
            self.assertTrue(site_configuration.enabled)
            self.assertTrue(site_configuration.get_value("EDNX_TENANT_KEY"))
            self.assertTrue(site_configuration.get_value("EDNX_USE_SIGNAL"))
