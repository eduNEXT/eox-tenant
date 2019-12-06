#!/usr/bin/python
"""
TODO: add me
"""
from __future__ import absolute_import
from django.test import TestCase
from django.core.exceptions import ValidationError

from eox_tenant.models import (
    Microsite,
    Route,
    TenantConfig,
    TenantConfigCompatibleSiteConfigurationProxyModel
)


class MicrositeModelTest(TestCase):
    """
    Test the model where most of the logic is
    """

    def test_model_creation(self):
        """
        Answers the question: Can we create a model?
        """
        obj = Microsite()
        obj.key = "test_fake_key"
        obj.subdomain = "subdomain.localhost"
        obj.values = r"{}"
        obj.full_clean()

    def test_model_creation_fail(self):
        """
        Answers the question: If we make a wrong object, does it complain?
        """
        obj = Microsite()
        obj.key = "test_fake_key"
        with self.assertRaises(ValidationError):
            obj.full_clean()


class TenantConfigCompatibleSiteConfigurationProxyModelTest(TestCase):
    """
    Test TenantConfigCompatibleSiteConfigurationProxyModel.
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

        Route.objects.create(  # pylint: disable=no-member
            domain="domain1",
            config=TenantConfig.objects.get(external_key="tenant-key2"),
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

        self.assertTrue(org_list == TenantConfigCompatibleSiteConfigurationProxyModel.get_all_orgs())

    def test_get_value_for_org(self):
        """
        Test to get an specific value for a given org.
        """
        self.assertEqual(
            TenantConfigCompatibleSiteConfigurationProxyModel.get_value_for_org(
                org="test1-org",
                val_name="value-test",
                default=None,
            ),
            "Hello-World3",
        )

        self.assertEqual(
            TenantConfigCompatibleSiteConfigurationProxyModel.get_value_for_org(
                org="test3-org",
                val_name="value-test",
                default=None,
            ),
            "Hello-World2",
        )

        self.assertEqual(
            TenantConfigCompatibleSiteConfigurationProxyModel.get_value_for_org(
                org="test4-org",
                val_name="value-test",
                default="Default",
            ),
            "Default",
        )

    def test_get_config_by_domain(self):
        """
        Test to get the configuration and external key for a given domain.
        """
        configurations, external_key = TenantConfigCompatibleSiteConfigurationProxyModel.get_config_by_domain("domain1")

        self.assertEqual(external_key, "tenant-key2")
        self.assertDictEqual(
            configurations,
            {
                "course_org_filter": ["test5-org", "test1-org"],
                "value-test": "Hello-World3",
            },
        )

        configurations, external_key = TenantConfigCompatibleSiteConfigurationProxyModel.get_config_by_domain("domain2")

        self.assertEqual(external_key, None)
        self.assertDictEqual(configurations, {})

        configurations, external_key = \
            TenantConfigCompatibleSiteConfigurationProxyModel.get_config_by_domain("first.test.prod.edunext")

        self.assertEqual(external_key, "test_fake_key")
        self.assertDictEqual(
            configurations,
            {
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            },
        )

    def test_get_microsite_config_by_domain(self):
        """
        Test to get the configuration and external key for a given domain for microsites.
        """
        configurations, external_key = \
            TenantConfigCompatibleSiteConfigurationProxyModel.get_microsite_config_by_domain("first.test.prod.edunext")

        self.assertEqual(external_key, "test_fake_key")
        self.assertDictEqual(
            configurations,
            {
                "course_org_filter": "test1-org",
                "value-test": "Hello-World1",
            },
        )

        configurations, external_key = \
            TenantConfigCompatibleSiteConfigurationProxyModel.get_microsite_config_by_domain("fake-domain")

        self.assertEqual(external_key, None)
        self.assertDictEqual(configurations, {})
