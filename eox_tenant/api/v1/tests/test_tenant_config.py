"""
Test TenantConfig API v1.
"""

from mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import TenantConfig


class TenantConfigAPITest(APITestCase):
    """
    TenantConfig API TestCase.
    """
    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """
        setup.
        """
        super(TenantConfigAPITest, self).setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = '/api/v1/tenant-config/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.tenant_config_example = TenantConfig.objects.create(
            external_key='test_key',
            lms_configs={'key': 'value'},
            studio_configs={'key': 'value'},
            theming_configs={'key': 'value'},
            meta={'key': 'value'}
        )

    @patch_permissions
    def test_get_tenant_configs(self, _):
        """
        Must be get all TenantConfigs.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_tenant_config(self, _):
        """
        Must be get a single TenantConfig.
        """
        response = self.client.get('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_tenant_config(self, _):
        """
        Must be create new TenantConfig.
        """
        data = {
            'external_key': 'test_key',
            'lms_configs': {'key': 'value'},
            'studio_configs': {'key': 'value'},
            'theming_configs': {'key': 'value'},
            'meta': {'key': 'value'}
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TenantConfig.objects.count(), 2)
        self.assertEqual(TenantConfig.objects.get(pk=2).external_key, 'test_key')
        self.assertEqual(TenantConfig.objects.get(pk=2).lms_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(pk=2).studio_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(pk=2).theming_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(pk=2).meta, {'key': 'value'})

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
    def test_valid_update_tenant_config(self, _):
        """
        Must be update TenantConfig.
        """
        data = {
            'external_key': 'test_key_updated',
            'lms_configs': {'key': 'value_updated'},
            'studio_configs': {'key': 'value_updated'},
            'theming_configs': {'key': 'value_updated'},
            'meta': {'key': 'value_updated'}
        }
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_invalid_update_tenant_config(self, _):
        """
        Must be fail when try update a TenantConfig.
        """
        # Test empty request
        data = {}
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test with invalid request (all fields are required)
        data = {
            "key": "new_key",
            "subdomain": "subdomain.new"
        }
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_patch_tenant_config(self, _):
        """
        Must be update using patch method a TenantConfig.
        """
        data = {'external_key': 'test_key_updated'}
        response = self.client.patch('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk),
                                     data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_delete_tenant_config(self, _):
        """
        Must be delete a TenantConfig.
        """
        response = self.client.delete('{url}{id}/'.format(url=self.url, id=self.tenant_config_example.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
