"""This module include a class that checks the command change_domain.py"""

from django.test import TestCase
from django.core.management import call_command

from eox_tenant.models import Microsite


class ChangeDomainTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):  # pylint: disable=invalid-name
        """This method creates Microsite objects in database"""

        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co")

    def test_domain_can_change(self):
        """Subdomain has been changed by the command"""
        call_command('change_domain')
        prod = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co").first()
        stage = Microsite.objects.filter(  # pylint: disable=no-member
            subdomain="first-test-prod-edunext-co-stage.edunext.co").first()
        self.assertIsNone(prod)
        self.assertIsNotNone(stage)
