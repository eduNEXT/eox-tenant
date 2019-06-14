"""
Site configuration backend that reads the configuration from the database
"""


class CompatibleDatabaseSiteConfigBackend(object):
    """
    Backend that reads the configurations definitions from the database
    using the custom models from edunext
    """

    def get_config_by_domain(self, domain):
        """
        Get the correct set of site configurations.
        """
        from eox_tenant.models import TenantConfig
        configurations, external_key = TenantConfig.get_configs_for_domain(domain)

        if not (configurations and external_key):
            configurations, external_key = self._get_microsite_config_by_domain(domain)

        return configurations, external_key

    def _get_microsite_config_by_domain(self, domain):
        """
        Return the configuration and key available for a given domain.
        """
        from eox_tenant.models import Microsite
        microsite = Microsite.get_microsite_for_domain(domain)

        if microsite:
            return microsite.values, microsite.key
        else:
            return {}, None
