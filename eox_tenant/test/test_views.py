"""
Test views file.
"""
from django.test import TestCase
from django.urls import reverse


class EOXInfoTestCase(TestCase):
    """
    Test for eox-info view.
    """

    def test_view_info_accesible(self):
        """
        Should get a successful answer
        """
        with self.settings(ALLOWED_HOSTS=['testserver']):
            response = self.client.get(reverse('eox-info'), HTTP_HOST='testserver')
            self.assertEqual(response.status_code, 200)

    def test_view_info_response_data(self):
        """
        Check the content of the response.
        """
        with self.settings(ALLOWED_HOSTS=['testserver']):
            response = self.client.get(reverse('eox-info'), HTTP_HOST='testserver')
            content = response.json()

            name = 'eox-tenant'

            self.assertEqual(name, content['name'])
            self.assertEqual(response.status_code, 200)
