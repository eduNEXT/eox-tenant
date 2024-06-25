"""
Test integration file.
"""
from django.test import TestCase, override_settings


@override_settings(ALLOWED_HOSTS=['testserver'], SITE_ID=2)
class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with openedx
    """

    def setUp(self):
        """
        Set up the base URL for the tests
        """
        self.base_url = 'http://local.edly.io'

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.branding_api_l_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.users_l_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.bearer_authentication_l_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.edxmako_l_v1  # isort:skip
        import eox_tenant.edxapp_wrapper.backends.edx_auth_n_v1  # isort:skip

    def test_info_view(self):
        """
        Tests the info view endpoint in Tutor
        """
        info_view_url = f'{self.base_url}/eox-tenant/eox-info'

        response = self.client.get(info_view_url)

        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertIn('version', response_data)
        self.assertIn('name', response_data)
        self.assertIn('git', response_data)
