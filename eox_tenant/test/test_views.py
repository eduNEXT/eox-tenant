"""
Test views file.
"""
from os.path import dirname
from subprocess import CalledProcessError, check_output

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

            working_dir = dirname(__file__)
            version = check_output(["git", "describe", "--tags", "--abbrev=0"], cwd=working_dir)
            version = version.decode().replace('\n', '')[1:]
            name = 'eox-tenant'
            commit_id = check_output(["git", "rev-parse", "HEAD"], cwd=working_dir)
            commit_id = commit_id.decode().replace('\n', '')

            self.assertEqual(version, content['version'])
            self.assertEqual(name, content['name'])
            self.assertEqual(commit_id, content['git'])
            self.assertEqual(response.status_code, 200)

        with self.assertRaises(CalledProcessError):
            commit_id = check_output(["git", "rev", "HEAD"], cwd=working_dir)
