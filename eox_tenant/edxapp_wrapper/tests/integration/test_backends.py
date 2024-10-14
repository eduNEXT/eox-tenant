"""
This module tests the backends of the edxapp_wrapper
"""


# pylint: disable=import-outside-toplevel,unused-import
def test_current_settings_code_imports():
    """
    Running this imports means that our backends import the right signature
    """
    import eox_tenant.edxapp_wrapper.backends.bearer_authentication_l_v1
    import eox_tenant.edxapp_wrapper.backends.branding_api_l_v1
    import eox_tenant.edxapp_wrapper.backends.edx_auth_n_v1
    import eox_tenant.edxapp_wrapper.backends.edxmako_l_v1
    import eox_tenant.edxapp_wrapper.backends.oauth_dispatch_j_v1
    import eox_tenant.edxapp_wrapper.backends.site_configuration_module_i_v1
    import eox_tenant.edxapp_wrapper.backends.theming_helpers_h_v1
    import eox_tenant.edxapp_wrapper.backends.users_p_v1
