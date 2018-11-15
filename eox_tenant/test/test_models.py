#!/usr/bin/python
"""
TODO: add me
"""
from django.test import TestCase
from django.core.exceptions import ValidationError

from eox_tenant.ednx_microsites.models import Microsite


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
