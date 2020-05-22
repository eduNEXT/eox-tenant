"""This module include a class that checks the command change_domain.py"""

import mock
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase

from eox_tenant.models import Microsite


class ChangeDomainTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):
        """This method creates Microsite objects in database"""
        Microsite.objects.create(
            subdomain="first.test.prod.edunext.co")
        Site.objects.create(
            domain="second.test.prod.edunext.co",
            name="second.test.prod.edunext.co")

        usersignup_source = mock.MagicMock()
        usersignup_source.site = 'first.test.prod.edunext.co:8000'

        self.usersignupsource = usersignup_source

    @mock.patch('eox_tenant.edxapp_wrapper.users.get_user_signup_source')
    def test_domain_can_change(self, signupsource_mock):
        """Subdomain has been changed by the command"""
        signupsource = mock.MagicMock()
        signupsource.objects.all.return_value = [self.usersignupsource]
        signupsource_mock.return_value = signupsource

        call_command('change_domain', signupsources=True)
        prod = Microsite.objects.filter(
            subdomain="first.test.prod.edunext.co").first()
        stage = Microsite.objects.filter(
            subdomain="first-test-prod-edunext-co-stage.edunext.co").first()
        self.assertIsNone(prod)
        self.assertIsNotNone(stage)
        prod_site = Site.objects.filter(
            domain="second.test.prod.edunext.co").first()
        stage_site = Site.objects.filter(
            domain="second-test-prod-edunext-co-stage.edunext.co").first()
        self.assertIsNone(prod_site)
        self.assertIsNotNone(stage_site)

        self.assertEqual(self.usersignupsource.site, 'first-test-prod-edunext-co-stage.edunext.co:8000')

    def test_domain_can_change_with_point(self):
        """Subdomain has been changed by the command"""
        call_command('change_domain', suffix_domain=".stage.edunext.co")
        prod = Microsite.objects.filter(
            subdomain="first.test.prod.edunext.co").first()
        stage = Microsite.objects.filter(
            subdomain="first-test-prod-edunext-co.stage.edunext.co").first()
        self.assertIsNone(prod)
        self.assertIsNotNone(stage)
        prod_site = Site.objects.filter(
            domain="second.test.prod.edunext.co").first()
        stage_site = Site.objects.filter(
            domain="second-test-prod-edunext-co.stage.edunext.co").first()
        self.assertIsNone(prod_site)
        self.assertIsNotNone(stage_site)

    def test_ecommerce_urls_can_change(self):
        """Ecommerce urls has been changed by the command"""
        values = {
            "ECOMMERCE_PUBLIC_URL_ROOT": "https://ecommerce.url/",
            "ECOMMERCE_API_URL": "https://ecommerce.url/api/v1/",
        }
        prod = Microsite.objects.filter(
            subdomain="first.test.prod.edunext.co").first()
        prod.values = values
        prod.save()
        call_command(
            'change_domain',
            suffix_domain=".stage.edunext.co",
            suffix_ecommerce_domain=".stage-compl1.edunext.co"
        )
        stage = Microsite.objects.filter(
            subdomain="first-test-prod-edunext-co.stage.edunext.co").first()
        ecommerce_public_url_root = stage.values['ECOMMERCE_PUBLIC_URL_ROOT']
        ecommerce_api_url = stage.values['ECOMMERCE_API_URL']

        self.assertEqual(ecommerce_public_url_root, 'https://ecommerce-url.stage-compl1.edunext.co/')
        self.assertEqual(ecommerce_api_url, 'https://ecommerce-url.stage-compl1.edunext.co/api/v1/')
