#!/usr/bin/python
"""
Test utils functions.
"""
from __future__ import absolute_import

import ddt
import mock
from django.test import TestCase

from eox_tenant.utils import is_valid_domain, move_signupsource


@ddt.ddt
class DomainValidationTest(TestCase):
    """
    Test domain validator.
    """
    @ddt.data('example.com', 'example1.com', 'example-2.com')
    def test_valid_domains(self, domain):
        """
        Test the cases where a domain is valid.
        """
        self.assertTrue(is_valid_domain(domain))

    @ddt.data('example.com/', 'https://example.com', '12231', 'localhost')
    def test_invalid_domains(self, domain):
        """
        Test invalid domains validation.
        """
        self.assertFalse(is_valid_domain(domain))


class MoveSignupSource(TestCase):
    """ Test for move_signupsource function"""

    @mock.patch('eox_tenant.utils.UserSignupSource')
    def test_change_signupsource(self, signupsource_mock):
        """Test signup source model manager is called with the proper arguments"""
        signupsource_filtered = mock.MagicMock()
        signupsource_mock.objects.filter.return_value = signupsource_filtered

        move_signupsource("example1.edunext.co", "example2.edunext.co")
        signupsource_mock.objects.filter.assert_called_with(site="example1.edunext.co")
        signupsource_filtered.update.assert_called_with(site="example2.edunext.co")
