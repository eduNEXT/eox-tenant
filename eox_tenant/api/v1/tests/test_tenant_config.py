"""
Test TenantConfig API v1.
"""
from django.contrib.auth.models import User
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import Route, TenantConfig


class TenantConfigAPITest(APITestCase):  # pylint: disable=too-many-instance-attributes
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
        self.tenant_config_with_route = TenantConfig.objects.create(
            external_key='test_key_with_route',
            lms_configs={'PLATFORM_NAME': 'Old Name'},
            studio_configs={'key': 'value'},
            theming_configs={'key': 'value'},
            meta={'key': 'value'},
        )
        self.domain = 'site3.localhost'
        self.route = Route.objects.create(domain=self.domain, config=self.tenant_config_with_route)
        self.update_by_domain_url = f'{self.url}update-by-domain/'
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
        tenant_config_objects_count = TenantConfig.objects.count()
        external_key = 'test_key_3'
        data = {
            'external_key': external_key,
            'lms_configs': {'key': 'value'},
            'studio_configs': {'key': 'value'},
            'theming_configs': {'key': 'value'},
            'meta': {'key': 'value'},
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TenantConfig.objects.count(), tenant_config_objects_count + 1)
        self.assertEqual(TenantConfig.objects.get(external_key=external_key).lms_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(external_key=external_key).studio_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(external_key=external_key).theming_configs, {'key': 'value'})
        self.assertEqual(TenantConfig.objects.get(external_key=external_key).meta, {'key': 'value'})

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

    @patch_permissions
    def test_update_tenant_config_by_domain_success(self, _):
        """Must successfully update a TenantConfig using `route__domain`."""
        data = {
            "lms_configs": {
                "PLATFORM_NAME": "Updated Name"
            }
        }
        response = self.client.patch(f"{self.update_by_domain_url}?domain={self.domain}", data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lms_configs"]["PLATFORM_NAME"], "Updated Name")

    @patch_permissions
    def test_update_tenant_config_by_domain_missing_query_param(self, _):
        """Must return 400 when domain query parameter is missing."""
        data = {
            "lms_configs": {
                "PLATFORM_NAME": "Updated Name"
            }
        }
        response = self.client.patch(self.update_by_domain_url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "The 'domain' query parameter is required.")

    @patch_permissions
    def test_update_tenant_config_by_domain_not_found(self, _):
        """Must return 404 when no TenantConfig is found for the given domain."""
        data = {
            "lms_configs": {
                "PLATFORM_NAME": "Updated Name"
            }
        }
        response = self.client.patch(f"{self.update_by_domain_url}?domain=unknown.localhost", data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "No TenantConfig found for domain 'unknown.localhost'.")

    @patch_permissions
    def test_update_tenant_config_by_domain_empty_payload(self, _):
        """Must ensure that if an empty payload is sent, nothing gets changed."""
        external_key = self.tenant_config_with_route.external_key
        lms_configs = self.tenant_config_with_route.lms_configs
        studio_configs = self.tenant_config_with_route.studio_configs
        theming_configs = self.tenant_config_with_route.theming_configs
        meta = self.tenant_config_with_route.meta

        response = self.client.patch(f"{self.update_by_domain_url}?domain={self.domain}", data={}, format='json')
        self.tenant_config_with_route.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.tenant_config_with_route.external_key, external_key)
        self.assertEqual(self.tenant_config_with_route.lms_configs, lms_configs)
        self.assertEqual(self.tenant_config_with_route.studio_configs, studio_configs)
        self.assertEqual(self.tenant_config_with_route.theming_configs, theming_configs)
        self.assertEqual(self.tenant_config_with_route.meta, meta)

    @patch_permissions
    def test_update_tenant_config_by_domain_invalid_data(self, _):
        """Must return 400 when the payload contains invalid data."""
        data = {
            "lms_configs": "Invalid structure"  # Should be a dictionary
        }
        response = self.client.patch(f"{self.update_by_domain_url}?domain={self.domain}", data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_partial_update_tenant_config_by_domain(self, _):
        """Must allow partial updates without modifying other fields."""
        data = {
            "lms_configs": {
                "PLATFORM_NAME": "New Partial Update"
            }
        }
        response = self.client.patch(f"{self.update_by_domain_url}?domain={self.domain}", data=data, format='json')
        print(100 * "#")
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tenant_config_with_route.refresh_from_db()
        self.assertEqual(self.tenant_config_with_route.lms_configs["PLATFORM_NAME"], "New Partial Update")

    @patch_permissions
    def test_update_tenant_config_by_domain_preserves_other_fields(self, _):
        """Ensure updating one field does not erase other fields."""
        data = {
            "lms_configs": {
                "PLATFORM_NAME": "Updated Platform Name"
            }
        }
        response = self.client.patch(f"{self.update_by_domain_url}?domain={self.domain}", data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tenant_config_with_route.refresh_from_db()
        self.assertEqual(self.tenant_config_with_route.lms_configs["PLATFORM_NAME"], "Updated Platform Name")
        self.assertEqual(self.tenant_config_with_route.studio_configs, {"key": "value"})
