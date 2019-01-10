"""
Microsite backend that reads the configuration from the database
"""
import os

from django.conf import settings
from django.utils import six
from eox_tenant.backends.base import BaseMicrositeBackend
from eox_tenant.edxapp_wrapper.get_common_util import strip_port_from_host


class EdunextCompatibleDatabaseMicrositeBackend(BaseMicrositeBackend):
    """
    Microsite backend that reads the microsites definitions from the database
    using the custom models from edunext
    """
    _microsite_manager = None

    @property
    def microsite_manager(self):
        """
        Return eox_tenant microsite manager.
        """
        if not self._microsite_manager:
            from eox_tenant.models import Microsite
            self._microsite_manager = Microsite
        return self._microsite_manager

    def has_configuration_set(self):
        """
        We always require a configuration to function, so we can skip the query
        """
        return settings.FEATURES.get('USE_MICROSITES', False)

    def iterate_sites(self):
        """
        Return all the microsites from the database storing the results in the current request to avoid
        quering the DB multiple times in the same request
        """

        cache_key = "all-microsites-iterator"
        cached_list = self.get_key_from_cache(cache_key)

        if cached_list:
            candidates = cached_list
        else:
            candidates = self.microsite_manager.objects.all()  # pylint: disable=no-member
            self.set_key_to_cache(cache_key, candidates)

        for microsite in candidates:
            yield microsite

    def get_config_by_domain(self, domain):
        """
        Return the configuration and key available for a given domain without applying it
        to the local thread
        """
        microsite = self.microsite_manager.get_microsite_for_domain(domain)
        if microsite:
            return microsite.values, microsite.key
        else:
            return {}, None

    def set_config_by_domain(self, domain):
        """
        For a given request domain, find a match in our microsite configuration
        and then assign it to the thread local in order to make it available
        to the complete Django request processing
        """
        if not self.has_configuration_set() or not domain:
            return
        microsite = self.microsite_manager.get_microsite_for_domain(domain)
        if microsite:
            self._set_microsite_config_from_obj(microsite.subdomain, domain, microsite)
            return

        # if no match on subdomain then see if there is a 'default' microsite
        # defined in the db. If so, then use it
        try:
            microsite = self.microsite_manager.objects.get(key='default')  # pylint: disable=no-member
            self._set_microsite_config_from_obj(microsite.subdomain, domain, microsite)
            return
        except self.microsite_manager.DoesNotExist:  # pylint: disable=no-member
            return

    def get_all_config(self):
        """
        This returns all configuration for all microsites
        """
        config = {}

        candidates = self.microsite_manager.objects.all()  # pylint: disable=no-member
        for microsite in candidates:
            values = microsite.values
            config[microsite.key] = values

        return config

    def get_value_for_org(self, org, val_name, default=None):
        """
        Returns a configuration value for a microsite which has an org_filter that matches
        what is passed in
        """
        if not self.has_configuration_set():
            return default

        cache_key = "org-value-{}-{}".format(org, val_name)
        cached_value = self.get_key_from_cache(cache_key)
        if cached_value:
            return cached_value

        # Filter at the db
        for microsite in self.iterate_sites():
            current = microsite.values
            org_filter = current.get('course_org_filter')
            if org_filter:
                if isinstance(org_filter, six.string_types):
                    org_filter = set([org_filter])
                if org in org_filter:
                    result = current.get(val_name, default)
                    self.set_key_to_cache(cache_key, result)
                    return result

        self.set_key_to_cache(cache_key, default)
        return default

    def get_all_orgs(self):
        """
        This returns a set of orgs that are considered within all microsites.
        This can be used, for example, to do filtering
        """
        org_filter_set = set()
        if not self.has_configuration_set():
            return org_filter_set

        # Get the orgs in the db
        for microsite in self.iterate_sites():
            current = microsite.values
            org_filter = current.get('course_org_filter')
            if org_filter and isinstance(org_filter, list):
                for org in org_filter:
                    org_filter_set.add(org)
            elif org_filter:
                org_filter_set.add(org_filter)

        return org_filter_set

    def _set_microsite_config_from_obj(self, subdomain, domain, microsite_object):
        """
        Helper internal method to actually find the microsite configuration
        """
        config = microsite_object.values
        config['subdomain'] = strip_port_from_host(subdomain)
        config['site_domain'] = strip_port_from_host(domain)
        config['microsite_config_key'] = microsite_object.key
        self.current_request_configuration.data = config

    def enable_microsites(self, log):
        """
        Configure the paths for the microsites feature
        """
        microsites_root = settings.MICROSITE_ROOT_DIR

        if os.path.isdir(microsites_root):
            settings.STATICFILES_DIRS.insert(0, microsites_root)
            settings.LOCALE_PATHS = [microsites_root / 'conf/locale'] + settings.LOCALE_PATHS

            log.info('Eox-tenant is loading microsite path at %s', microsites_root)
        else:
            log.error(
                'Eox-tenant had an error loading %s. Directory does not exist',
                microsites_root
            )

    def set_key_to_cache(self, key, value):
        """
        Stores a key value pair in a cache scoped to the thread
        """
        if not hasattr(self.current_request_configuration, 'cache'):
            self.current_request_configuration.cache = {}

        self.current_request_configuration.cache[key] = value
