"""
Test routes API v1.
"""
from django.contrib.auth.models import User
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import Route, TenantConfig


class RouteAPITest(APITestCase):
    """Route API TestCase."""

    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """setup."""
        super().setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = reverse('api:v1:tenant-api:route-list')
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.tenant_config = TenantConfig.objects.create(
            external_key='',
            lms_configs={'key': 'lms_value'},
            studio_configs={'key': 'studio_value'},
            theming_configs={'key': 'theming_value'},
            meta={'key': 'meta_value'},
        )
        self.route_example = Route.objects.create(
            domain='domain.host',
            config=self.tenant_config,
        )
        self.url_detail = f'{self.url}{self.route_example.pk}/'

    @patch_permissions
    def test_get_routes(self, _):
        """Must get all Routes."""
        response = self.client.get(self.url)

        self.assertEqual(response.accepted_media_type, 'application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_route(self, _):
        """Must get a single Route."""
        response = self.client.get(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_route(self, _):
        """Must create new Route."""
        data = {
            'domain': 'created.domain',
            'config': self.tenant_config.pk,
        }

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 2)
        self.assertEqual(Route.objects.get(pk=2).domain, 'created.domain')
        self.assertEqual(Route.objects.get(pk=2).config.pk, 1)

    @patch_permissions
    def test_post_input_empty_data(self, _):
        """Must fail with wrong data."""
        data = {}

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_post_input_wrong_data(self, _):
        """Must fail with incomplete data."""
        data = {'domain': 'created.domain'}

        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_update_route(self, _):
        """Must update Route."""
        data = {'domain': 'created.domain', 'config': 1}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_empty_put_route(self, _):
        """Must fail when try update a Route with empty data."""
        data = {}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_partial_put_route(self, _):
        """Must fail when try update a Route with partial data."""
        data = {"domain": "domain.updated"}

        response = self.client.put(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_patch_tenant_config(self, _):
        """Must update a Route using patch method."""
        data = {"domain": "domain.updated"}

        response = self.client.patch(self.url_detail, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
