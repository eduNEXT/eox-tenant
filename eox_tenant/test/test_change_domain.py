"""This module include a class that checks the command change_domain.py"""

import mock

from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.management import call_command

from eox_tenant.models import Microsite


class ChangeDomainTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):
        """This method creates Microsite objects in database"""

        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co")
        Site.objects.create(  # pylint: disable=no-member
            domain="second.test.prod.edunext.co",
            name="second.test.prod.edunext.co")

        usersignup_source = mock.MagicMock()
        usersignup_source.site = 'first.test.prod.edunext.co'

        self.usersignupsource = usersignup_source

    @mock.patch('eox_tenant.edxapp_wrapper.users.get_user_signup_source')
    def test_domain_can_change(self, signupsource_mock):
        """Subdomain has been changed by the command"""
        signupsource = mock.MagicMock()
        signupsource.objects.all.return_value = [self.usersignupsource]
        signupsource_mock.return_value = signupsource

        call_command('change_domain', signupsources=True)
        prod = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co").first()
        stage = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first-test-prod-edunext-co-stage.edunext.co").first()
        self.assertIsNone(prod)
        self.assertIsNotNone(stage)
        prod_site = Site.objects.filter(  # pylint: disable=no-member
            domain="second.test.prod.edunext.co").first()
        stage_site = Site.objects.filter(  # pylint: disable=no-member
            domain="second-test-prod-edunext-co-stage.edunext.co").first()
        self.assertIsNone(prod_site)
        self.assertIsNotNone(stage_site)

        self.assertEqual(self.usersignupsource.site, 'first-test-prod-edunext-co-stage.edunext.co')

    def test_domain_can_change_with_point(self):
        """Subdomain has been changed by the command"""
        call_command('change_domain', suffix_domain=".stage.edunext.co")
        prod = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co").first()
        stage = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first-test-prod-edunext-co.stage.edunext.co").first()
        self.assertIsNone(prod)
        self.assertIsNotNone(stage)
        prod_site = Site.objects.filter(  # pylint: disable=no-member
            domain="second.test.prod.edunext.co").first()
        stage_site = Site.objects.filter(  # pylint: disable=no-member
            domain="second-test-prod-edunext-co.stage.edunext.co").first()
        self.assertIsNone(prod_site)
        self.assertIsNotNone(stage_site)
