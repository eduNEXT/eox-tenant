"""
Test integration file.
"""
import requests
from django.conf import settings as ds
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

settings = ds.INTEGRATION_TEST_SETTINGS


class TestInfoView(TestCase):
    """
    Integration test suite for the info view.
    """

    def setUp(self):
        """
        Set up the test suite.
        """
        self.url = f"{settings['EOX_TENANT_BASE_URL']}{reverse('eox-info')}"
        super().setUp()

    def test_info_view_success(self) -> None:
        """Test the info view.

        Expected result:
        - The status code is 200.
        - The response contains the version, name and git commit hash.
        """
        response = requests.get(self.url, timeout=settings["API_TIMEOUT"])

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("version", response_data)
        self.assertIn("name", response_data)
        self.assertIn("git", response_data)
