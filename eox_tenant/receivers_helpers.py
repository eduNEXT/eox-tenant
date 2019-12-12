"""
Common utilities for use along signals file.
"""

from eox_tenant.models import TenantConfig, Microsite


def get_tenant_config_by_domain(domain):
    """
    Reach for the configuration for a given domain.

    **Arguments**
        domain: String parameter.

    **Returns**
        configurations: dict
        external_key: String

        **Example**

            configuration = {
                "EDNX_USE_SIGNAL":True,
                "ENABLE_MKTG_SITE":True,
                "LMS_ROOT_URL":"http://courses.www.localhost:18000/",
                "SESSION_COOKIE_DOMAIN":".www.localhost",
                "SITE_NAME":"courses.www.localhost:18000",
                "MKTG_URLS":{
                    "ABOUT":"about",
                    "BLOG":"",
                }
                ...
            }

            external_key = "this_is_my_key"
    """
    configurations, external_key = TenantConfig.get_configs_for_domain(domain)

    if not (configurations and external_key):

        microsite = Microsite.get_microsite_for_domain(domain)

        if microsite:
            configurations = microsite.values
            external_key = microsite.key
        else:
            configurations = {}
            external_key = None

    return configurations, external_key
