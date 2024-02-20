"""
Test TenantConfig API v1.
"""
from django.contrib.auth.models import User
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import TenantConfig


class TenantConfigAPITest(APITestCase):
    """TenantConfig API TestCase."""

    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """
        setup.
        """
        super().setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = reverse('api:v1:tenant-api:tenantconfig-list')
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.tenant_config_example = TenantConfig.objects.create(
            external_key='test_key',
            lms_configs={'key': 'value'},
            studio_configs={'key': 'value'},
            theming_configs={'key': 'value'},
            meta={'key': 'value'},
        )
        self.url_detail = f'{self.url}{self.tenant_config_example.pk}/'

    @patch_permissions
    def test_get_tenant_configs(self, _):
        """Must get all TenantConfigs."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_tenant_config(self, _):
        """Must get a single TenantConfig."""
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_tenant_config(self, _):
        """Must create new TenantConfig."""
        data = {
            'external_key': 'test_key',
            'lms_configs': {'key': 'value'},
            'studio_configs': {'key': 'value'},
            'theming_configs': {'key': 'value'},
            'meta': {'key': 'value'},
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
    def test_post_input_empty_data(self, _):
        """Must fail with wrong data."""
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
    def test_valid_update_tenant_config(self, _):
        """Must update TenantConfig."""
        data = {
            'external_key': 'test_key_updated',
            'lms_configs': {'key': 'value_updated'},
            'studio_configs': {'key': 'value_updated'},
            'theming_configs': {'key': 'value_updated'},
            'meta': {'key': 'value_updated'},
        }

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_empty_put_tenant_config(self, _):
        """Must fail when try update a TenantConfig with empty data."""
        data = {}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_partial_put_tenant_config(self, _):
        """Must fail when try update a TenantConfig with partial data."""
        data = {'external_key': 'test_key_updated'}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_patch_tenant_config(self, _):
        """Must update a TenantConfig using patch method."""
        data = {'external_key': 'test_key_updated'}

        response = self.client.patch(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_delete_tenant_config(self, _):
        """Must delete a TenantConfig."""
        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
