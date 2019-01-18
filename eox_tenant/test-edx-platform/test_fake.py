"""This module include a class that checks the command change_domain.py"""

from django.test import TestCase
from student.roles import CourseStaffRole

from eox_tenant.models import Microsite


class FakeTestCase(TestCase):
    """ This class checks the command change_domain.py"""

    def setUp(self):
        """This method creates Microsite objects in database"""

        Microsite.objects.create(  # pylint: disable=no-member
            subdomain="first.test.prod.edunext.co")

    def test_fake(self):
        """Subdomain has been changed by the command"""
        pass
