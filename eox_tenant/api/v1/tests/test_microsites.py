"""
Test microsites API v1.
"""
from django.contrib.auth.models import User
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import Microsite


class MicrositeAPITest(APITestCase):
    """Microsite API TestCase."""

    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """setup."""
        super(MicrositeAPITest, self).setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = reverse('api:v1:tenant-api:microsite-list')
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.microsite_example = Microsite.objects.create(
            key='test_key',
            subdomain='test.host',
            values={'key': 'value'},
        )
        self.url_detail = '{url}{id}/'.format(url=self.url, id=self.microsite_example.pk)

    @patch_permissions
    def test_get_microsites(self, _):
        """Must get all Microsites."""
        response = self.client.get(self.url)

        self.assertEqual(response.accepted_media_type, 'application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_microsite(self, _):
        """Must get a single Microsite."""
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_microsite(self, _):
        """Must create new Microsite."""
        data = {
            'key': 'test_fake_key',
            'subdomain': 'subdomain.localhost',
            'values': {'key': 'value'},
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Microsite.objects.count(), 2)
        self.assertEqual(Microsite.objects.get(pk=2).key, 'test_fake_key')
        self.assertEqual(Microsite.objects.get(pk=2).subdomain, 'subdomain.localhost')
        self.assertEqual(Microsite.objects.get(pk=2).values, {'key': 'value'})

    @patch_permissions
    def test_post_input_empty_data(self, _):
        """Must fail with empty data."""
        data = {}

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_post_input_wrong_data(self, _):
        """Must fail with incomplete data."""
        data = {'values': {'key': 'value'}}

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_put_microsite(self, _):
        """Must update Microsite."""
        data = {
            "key": "new_key",
            "subdomain": "subdomain.new",
            "values": {"key": "updated"},
        }

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_empty_put_microsite(self, _):
        """Must fail when try update a Microsite with empty data."""
        data = {}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_partial_put_microsite(self, _):
        """Must fail when try update a Microsite with partial data."""
        data = {
            "key": "new_key",
            "subdomain": "subdomain.new",
        }

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_patch_microsite(self, _):
        """Must update a Microsite using patch method."""
        data = {"key": "new_patch_key"}

        response = self.client.patch(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_delete_microsite(self, _):
        """Must delete a Microsite."""
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_permissions_microsite(self):
        """Must return 403, only allows superuser."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
