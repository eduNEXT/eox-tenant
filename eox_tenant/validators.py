"""
This overwrites the EdxOAuth2Validator behavior
"""
from eox_tenant.edxapp_wrapper.auth import get_edx_oauth2_validator_class

EdxOAuth2Validator = get_edx_oauth2_validator_class()


class EoxTenantOAuth2Validator(EdxOAuth2Validator):
    """
    Class that validates the token usage:
        * The token can only be used in the site it was created
    """
