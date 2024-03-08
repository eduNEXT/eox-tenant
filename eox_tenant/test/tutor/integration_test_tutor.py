"""
Test views file.
"""
from django.test import TestCase


class TutorIntegrationTestCase(TestCase):
    """
    POC code to run tests that cover the integration with openedx
    """

    def test_runs_code(self):
        """
        Just to make sure our test infrastructure is behaving
        """
        assert True

    # pylint: disable=import-outside-toplevel,unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        import eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1
        import eox_tenant.edxapp_wrapper.backends.branding_api_l_v1
        # fixme: needs to be properly removed if unused at the latest version  # pylint: disable=fixme
        # import eox_tenant.edxapp_wrapper.backends.certificates_module_i_v1
        import eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1
        import eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1
        # fixme: needs to be properly removed if unused at the latest version  # pylint: disable=fixme
        # import eox_tenant.edxapp_wrapper.backends.edx_auth_i_v1
        import eox_tenant.edxapp_wrapper.backends.users_l_v1
        import eox_tenant.edxapp_wrapper.backends.bearer_authentication_l_v1
        import eox_tenant.edxapp_wrapper.backends.edxmako_l_v1
        # fixme: needs to be properly removed if unused at the latest version  # pylint: disable=fixme
        # import eox_tenant.edxapp_wrapper.backends.util_h_v1 # fixme
