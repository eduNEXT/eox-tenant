"""
Test microsites API v1.
"""

from mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import Microsite


class MicrositeAPITest(APITestCase):
    """
    Microsite API TestCase.
    """
    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """
        setup.
        """
        super(MicrositeAPITest, self).setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = '/api/v1/microsites/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.microsite_example = Microsite.objects.create(
            key='test_key',
            subdomain='test.host',
            values={'key': 'value'}
        )

    @patch_permissions
    def test_get_microsites(self, _):
        """
        Must be get all Microsites.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_microsite(self, _):
        """
        Must be get a single Microsite.
        """
        response = self.client.get('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_microsite(self, _):
        """
        Must be create new Microsite.
        """
        data = {
            'key': 'test_fake_key',
            'subdomain': 'subdomain.localhost',
            'values': {'key': 'value'}
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Microsite.objects.count(), 2)
        self.assertEqual(Microsite.objects.get(pk=2).key, 'test_fake_key')
        self.assertEqual(Microsite.objects.get(pk=2).subdomain, 'subdomain.localhost')
        self.assertEqual(Microsite.objects.get(pk=2).values, {'key': 'value'})

    @patch_permissions
    def test_post_input(self, _):
        """
        Must be fail with wrong data.
        """
        # Test empty request
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test request with only values
        data = {'values': {'key': 'value'}}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_update_microsite(self, _):
        """
        Must be update Microsite.
        """
        data = {
            "key": "new_key",
            "subdomain": "subdomain.new",
            "values": {"key": "updated"}
        }
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_invalid_update_microsite(self, _):
        """
        Must be fail when try update a Microsite.
        """
        # Test empty request
        data = {}
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test with invalid request (all fields are required)
        data = {
            "key": "new_key",
            "subdomain": "subdomain.new"
        }
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_patch_microsite(self, _):
        """
        Must be update using patch method a Microsite.
        """
        data = {"key": "new_patch_key"}
        response = self.client.patch('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk),
                                     data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_delete_microsite(self, _):
        """
        Must be delete a Microsite.
        """
        response = self.client.delete('{url}{id}/'.format(url=self.url, id=self.microsite_example.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
