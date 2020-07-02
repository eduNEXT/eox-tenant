"""This module include a class that checks the command change_signup_source"""

import mock
from django.core.management import call_command
from django.test import TestCase


class ChangeDomainTestCase(TestCase):
    """ Test for change_signup_source command"""

    @mock.patch('eox_tenant.utils.move_signupsource')
    def test_change_signupsource(self, move_singupsource_mock):
        """Test signup source model manager is called with the proper arguments"""

        call_command('change_signup_sources', "--from", "example1.edunext.co", "--to", "example2.edunext.co")
        move_singupsource_mock.assert_called_with("example1.edunext.co", "example2.edunext.co")
