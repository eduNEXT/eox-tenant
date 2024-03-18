"""
Test file to store the tenant_wise test module.
"""
from __future__ import absolute_import

import json

from django.core.management import call_command
from django.test import TransactionTestCase, override_settings

from eox_tenant.models import Microsite, TenantConfig
from eox_tenant.tenant_wise.proxies import TenantSiteConfigProxy


class TenantSiteConfigProxyTest(TransactionTestCase):
    """
    Test TenantSiteConfigProxy.
    """

    def setUp(self):
        """
        This method creates Microsite, TenantConfig and Route objects and in database.
        """
        Microsite.objects.create(
            subdomain="first.test.prod.edunext",
            key="test_fake_key",
            values={
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            }
        )

        Microsite.objects.create(
            subdomain="second.test.prod.edunext",
            values={
                "course_org_filter": ["test2-org", "test3-org"],
                "value-test": "Hello-World2",
            }
        )

        TenantConfig.objects.create(
            external_key="tenant-key1",
            lms_configs={
                "course_org_filter": ["common-org", "test4-org"],
                "lms_base": "tenant-1-base",
            },
            studio_configs={},
            theming_configs={},
            meta={},
        )

        TenantConfig.objects.create(
            external_key="tenant-key2",
            lms_configs={
                "course_org_filter": ["common-org", "test5-org", "test1-org"],
                "value-test": "Hello-World3",
                "lms_base": "tenant-2-base",
            },
            studio_configs={},
            theming_configs={},
            meta={},
        )
        call_command("synchronize_organizations")

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
            "common-org",
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

        # Prioritise current tenant's value if org is present
        with override_settings(EDNX_TENANT_KEY="tenant-key1"):
            self.assertEqual(
                TenantSiteConfigProxy.get_value_for_org(
                    org="common-org",
                    val_name="lms_base",
                    default="tenant-1-base",
                ),
                "tenant-1-base",
            )

        with override_settings(EDNX_TENANT_KEY="tenant-key2"):
            self.assertEqual(
                TenantSiteConfigProxy.get_value_for_org(
                    org="common-org",
                    val_name="lms_base",
                    default="tenant-2-base",
                ),
                "tenant-2-base",
            )

        # should return the first valid value if org is not present in current tenant
        with override_settings(EDNX_TENANT_KEY="tenant-key1"):
            self.assertEqual(
                TenantSiteConfigProxy.get_value_for_org(
                    org="common-org",
                    val_name="value-test",
                    default="some-value",
                ),
                "Hello-World3",
            )

        # should return the first valid value if tenant config is not used by
        # current site
        self.assertEqual(
            TenantSiteConfigProxy.get_value_for_org(
                org="common-org",
                val_name="value-test",
                default="some-value",
            ),
            "Hello-World3",
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

    def test_get_site_values_with_serializable_settings(self):
        """
        Test that if the settings are json serializable `site_values`
        returns a dict with the same values and json.dumps doesn't fail.
        """
        settings = {
            "EDNX_TENANT_KEY": True,
            "EDNX_USE_SIGNAL": True,
            "serializable_settings": {
                "integer": 1,
                "float": 1.0,
                "string": "str",
                "bool": False,
                "null": None,
                "list": [1, True, 1.0, None],
                "tuple": (2, False, 0.5, None),
                "dict": {"string": "str", "12": None},
            }
        }

        with self.settings(**settings):
            site_configuration = TenantSiteConfigProxy()
            serializable_settings = settings['serializable_settings']

            site_values = site_configuration.site_values['serializable_settings']

            self.assertDictEqual(
                serializable_settings,
                site_values
            )
            self.assertEqual(
                json.dumps(serializable_settings, sort_keys=True),
                json.dumps(site_values, sort_keys=True)
            )

    def test_get_site_values_with_unserializable_settings(self):
        """
        Test that if the settings are **not** json serializable `site_values`
        returns a subset of the original settings.
        """
        settings = {
            "EDNX_TENANT_KEY": True,
            "EDNX_USE_SIGNAL": True,
            "unserializable_settings": {
                "integer": 1,
                "float": 1.0,
                "string": "str",
                "bool": False,
                "null": None,
                "list": [1, True, 1.0, None],
                "tuple": (2, False, 0.5, None),
                "dict": {"string": "str", "12": None},
                "exception": Exception,
            }
        }

        with self.settings(**settings):
            site_configuration = TenantSiteConfigProxy()
            unserializable_settings = settings['unserializable_settings']

            site_values = site_configuration.site_values['unserializable_settings']

            with self.assertRaises(TypeError):
                json.dumps(unserializable_settings)
            self.assertDictContainsSubset(site_values, unserializable_settings)
