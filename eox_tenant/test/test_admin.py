"""
Tests for Admin module
"""
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from eox_tenant.admin import MicrositeAdmin, TenantConfigAdmin
from eox_tenant.models import Microsite, TenantConfig


class MicrositeAdminTest(TestCase):
    """
    Test Microsite admin class
    """

    def setUp(self):
        """
        Test set up Microsite admin class
        """
        self.microsite = Microsite()
        self.microsite.key = "test_fake_key"
        self.microsite.subdomain = "subdomain.localhost"
        self.microsite.values = {
            "SITE_NAME": "test_sitename",
            "template_dir": "test/dir",
            "course_org_filter": "test_filter",
            "EDNX_USE_SIGNAL": True,
        }
        self.microsite.full_clean()

        self.microsite_admin = MicrositeAdmin(model=Microsite, admin_site=AdminSite())

    def test_sitename(self):
        """
        Test get sitename using Microsite Admin
        """
        sitename = self.microsite_admin.sitename(self.microsite)
        self.assertEqual(sitename, "test_sitename")

    def test_template_dir(self):
        """
        Test get template_dir using Microsite Admin
        """
        template_dir = self.microsite_admin.template_dir(self.microsite)
        self.assertEqual(template_dir, "test/dir")

    def test_course_org_filter(self):
        """
        Test get course_org_filter using Microsite Admin
        """
        course_org_filter = self.microsite_admin.course_org_filter(self.microsite)
        self.assertEqual(course_org_filter, "test_filter")

    def test_ednx_signal(self):
        """
        Test get EDNX_USE_SIGNAL using Microsite Admin
        """
        ednx_signal = self.microsite_admin.ednx_signal(self.microsite)
        self.assertTrue(ednx_signal)


class TenantConfigAdminTest(TestCase):
    """
    Test TenantConfig admin class
    """

    def setUp(self):
        """
        Test set up for TenantConfig test class
        """
        self.tenant_config = TenantConfig()
        self.tenant_config.external_key = "external_fake_key"
        self.tenant_config.lms_configs = {
            "SITE_NAME": "test_sitename",
            "template_dir": "test/dir",
            "course_org_filter": "test_filter",
            "EDNX_USE_SIGNAL": True,
        }
        self.tenant_config.studio_configs = {}
        self.tenant_config.meta = {}

        self.tenant_config_admin = TenantConfigAdmin(model=TenantConfig, admin_site=AdminSite())

    def test_sitename(self):
        """
        Test get sitename using TenantConfig Admin
        """
        sitename = self.tenant_config_admin.sitename(self.tenant_config)
        self.assertEqual(sitename, "test_sitename")

    def test_template_dir(self):
        """
        Test get template_dir using TenantConfig Admin
        """
        template_dir = self.tenant_config_admin.template_dir(self.tenant_config)
        self.assertEqual(template_dir, "test/dir")

    def test_course_org_filter(self):
        """
        Test get course_org_filter using TenantConfig Admin
        """
        course_org_filter = self.tenant_config_admin.course_org_filter(self.tenant_config)
        self.assertEqual(course_org_filter, "test_filter")

    def test_ednx_signal(self):
        """
        Test get EDNX_USE_SIGNAL using TenantConfig Admin
        """
        ednx_signal = self.tenant_config_admin.ednx_signal(self.tenant_config)
        self.assertTrue(ednx_signal)
