"""
Test views file.
"""
from django.test import TestCase
from django.urls import reverse
# from django.conf import settings


class TutorIntegrationTestCase(TestCase):
    """
    """

    def test_runs_code(self):
        """
        """
        "this test should just pass"

    def test_current_settings_code_imports(self):
        """
        """
        import eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1
        import eox_tenant.edxapp_wrapper.backends.branding_api_l_v1
        import eox_tenant.edxapp_wrapper.backends.certificates_module_i_v1
        import eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1
        import eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1
        import eox_tenant.edxapp_wrapper.backends.edx_auth_i_v1
        import eox_tenant.edxapp_wrapper.backends.users_l_v1
        import eox_tenant.edxapp_wrapper.backends.bearer_authentication_l_v1
        import eox_tenant.edxapp_wrapper.backends.edxmako_l_v1
        import eox_tenant.edxapp_wrapper.backends.util_h_v1
