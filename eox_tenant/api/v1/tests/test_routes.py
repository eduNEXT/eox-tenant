"""
Test routes API v1.
"""

from mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from eox_tenant.models import Route, TenantConfig


class RouteAPITest(APITestCase):
    """
    Route API TestCase.
    """
    patch_permissions = patch('eox_tenant.api.v1.permissions.EoxTenantAPIPermission.has_permission', return_value=True)

    def setUp(self):
        """
        setup.
        """
        super(RouteAPITest, self).setUp()
        self.api_user = User(1, 'test@example.com', 'test')
        self.url = '/api/v1/routes/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.api_user)
        self.tenant_config = TenantConfig.objects.create(
            external_key='',
            lms_configs={'key': 'lms_value'},
            studio_configs={'key': 'studio_value'},
            theming_configs={'key': 'theming_value'},
            meta={'key': 'meta_value'})
        self.route_example = Route.objects.create(domain='domain.host', config=self.tenant_config)

    @patch_permissions
    def test_get_routes(self, _):
        """
        Must be get all Routes.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_get_valid_single_route(self, _):
        """
        Must be get a single Route.
        """
        response = self.client.get('{url}{id}/'.format(url=self.url, id=self.route_example.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_create_route(self, _):
        """
        Must be create new Route.
        """
        data = {
            'domain': 'created.domain',
            'config': self.tenant_config.pk
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 2)
        self.assertEqual(Route.objects.get(pk=2).domain, 'created.domain')
        self.assertEqual(Route.objects.get(pk=2).config.pk, 1)

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
        data = {'domain': 'created.domain'}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch_permissions
    def test_valid_update_route(self, _):
        """
        Must be update Route.
        """
        data = {'domain': 'created.domain', 'config': 1}
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.route_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch_permissions
    def test_invalid_update_route(self, _):
        """
        Must be fail when try update a Route.
        """
        # Test empty request
        data = {}
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.route_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test with invalid request (all fields are required)
        data = {"domain": "domain.updated"}
        response = self.client.put('{url}{id}/'.format(url=self.url, id=self.route_example.pk),
                                   data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
