"""This module include a class that checks the command change_domain.py"""

import mock

from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.management import call_command

from eox_tenant.models import Microsite, Route, TenantConfig


class ChangeDomainTestCase(TestCase):
    """ This class checks the command use_tenantconfig.py"""

    def setUp(self):
        """This created the objects used in  the tests"""

        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co")
        Site.objects.create(
            domain="second.test.prod.edunext.co",
            name="second.test.prod.edunext.co")

    def test_route_created(self):
        """Route has been created by the command"""
        call_command('use_tenantconfig', microsites=True)

        route = Route.objects.filter(domain="first.test.prod.edunext.co").first()  # pylint: disable=no-member
        self.assertIsNotNone(route)

    def test_call_command_twice(self):
        """There is created only one TenantConfig by the command"""
        call_command('use_tenantconfig', microsites=True)
        call_command('use_tenantconfig', microsites=True)

        tenants = TenantConfig.objects.all().count()

        self.assertEqual(1, tenants)

    def test_site_without_siteconfig(self):
        """Test that the command does not create nothing when there is not site configuration"""
        call_command('use_tenantconfig', siteconfigurations=True)
        route = Route.objects.filter(domain="second.test.prod.edunext.co").first()  # pylint: disable=no-member

        self.assertIsNone(route)

    @mock.patch('django.contrib.sites.models.Site.objects.all')
    def test_route_created_siteconfig(self, siteconfig_mock):
        """TRoute has been created by the command using site configurations"""
        site = mock.Mock(spec=Site)
        site.domain = "second.test.prod.edunext.co"
        site.configuration = mock.Mock()
        site.configuration.enabled = True
        site.configuration.values = {}
        siteconfig_mock.return_value = [site]

        call_command('use_tenantconfig', siteconfigurations=True)

        route = Route.objects.filter(domain="second.test.prod.edunext.co").first()  # pylint: disable=no-member
        self.assertIsNotNone(route)
