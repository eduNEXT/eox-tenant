"""
Tenant wise proxies that allows to override the platform models.
"""
import json
import logging
from itertools import chain

import six
from django.conf import settings
from django.core.cache import cache
from django.db import models

from eox_tenant.edxapp_wrapper.certificates_module import get_certificates_models
from eox_tenant.edxapp_wrapper.site_configuration_module import get_site_configuration_models
from eox_tenant.models import Microsite, TenantConfig, TenantOrganization
from eox_tenant.organizations import get_organizations
from eox_tenant.tenant_wise.context_managers import proxy_regression

SiteConfigurationModels = get_site_configuration_models()
CertificatesModels = get_certificates_models()
# The following line is necessary because we want to keep the previous Model GeneratedCertificate after the overrides.
GeneratedCertificate = CertificatesModels.GeneratedCertificate
TENANT_ALL_ORGS_CACHE_KEY = "tenant.all_orgs_list"
EOX_TENANT_CACHE_KEY_TIMEOUT = getattr(
    settings,
    "EOX_TENANT_CACHE_KEY_TIMEOUT",
    300
)
TENANT_MICROSITES_ITERATOR_KEY = "tenant-microsites-iterator"
logger = logging.getLogger(__name__)


class TenantSiteConfigProxy(SiteConfigurationModels.SiteConfiguration):
    """
    This a is Proxy model for SiteConfiguration from <openedx.core.djangoapps.site_configuration.models>.
    This allows to add or override methods using as base the SiteConfiguration model.
    More information in https://docs.djangoproject.com/en/3.0/topics/db/models/#proxy-models
    """

    class Meta:
        """ Set as a proxy model. """
        proxy = True

    def __str__(self):
        key = getattr(settings, "EDNX_TENANT_KEY", "No tenant is active at the moment")
        return "<Tenant proxy as site_configuration: {}>".format(key)

    @property
    def enabled(self):
        """
        Return True if EDNX_TENANT_KEY is in the current settings.
        """
        if getattr(settings, 'EDNX_TENANT_KEY', None):
            return True
        return False

    @enabled.setter
    def enabled(self, value):
        """
        We ignore the setter since this is a read proxy.
        """
        pass

    def get_value(self, name, default=None):
        """
        Return Configuration value from the Tenant loaded in the settings object
        as if this was a SiteConfiguration class.
        """
        try:
            return getattr(settings, name, default)
        except AttributeError as error:
            logger.exception("Invalid data at the TenantConfigProxy get_value. \n [%s]", error)

        return default

    @property
    def values(self):
        """
        Returns the raw values of the loaded settings.
        """
        if self.enabled:
            return vars(settings._wrapped)  # pylint: disable=protected-access
        return {}

    @values.setter
    def values(self, value):
        """
        We ignore the setter since this is a read proxy.
        """
        pass

    @property
    def site_values(self):
        """
        Returns the raw values of the loaded settings. This version works with juniper releases.
        """
        return self.values

    @site_values.setter
    def site_values(self, value):
        """
        We ignore the setter since this is a read proxy. This version works with juniper releases.
        """

    def save(self, *args, **kwargs):
        """
        Don't allow to save TenantSiteConfigProxy model in database.
        """
        pass

    @classmethod
    def get_all_orgs(cls):
        """
        This returns a set of orgs that are considered within all microsites and TenantConfig.
        This can be used, for example, to do filtering
        """
        # Check the cache first
        org_filter_set = cache.get(TENANT_ALL_ORGS_CACHE_KEY)

        if org_filter_set:
            return org_filter_set

        org_filter_set = set(TenantOrganization.objects.all().values_list("name", flat=True))
        cls.set_key_to_cache(TENANT_ALL_ORGS_CACHE_KEY, org_filter_set)

        return org_filter_set

    @classmethod
    def get_value_for_org(cls, org, val_name, default=None):
        """
        Returns a configuration value for a microsite or TenantConfig which has an org_filter that matches
        what is passed in.
        """
        return cls.__get_value_for_org(org, val_name, default)

    @classmethod
    def set_key_to_cache(cls, key, value):
        """
        Stores a key value pair in a cache scoped to the thread
        """
        cache.set(
            key,
            value,
            EOX_TENANT_CACHE_KEY_TIMEOUT
        )

    @classmethod
    def __get_value_for_org(cls, org, val_name, default=None):
        """
        Optimized method, that returns a value for the given org and val_name, from the
        TenantConfig or Microsite model.
        """
        cache_key = "org-value-{}-{}".format(org, val_name)
        cached_value = cache.get(cache_key)

        if cached_value:
            return cached_value

        result = TenantConfig.get_value_for_org(org, val_name)

        if result:
            cls.set_key_to_cache(cache_key, result)
            return result

        result = Microsite.get_value_for_org(org, val_name)
        result = result if result else default
        cls.set_key_to_cache(cache_key, result)

        return result

    @classmethod
    def pre_load_values_by_org(cls, val_name):
        """
        Save in cache the values for all the organizations in TenantConfig and Microsite models.
        """
        pre_load_value_key = "eox-tenant-pre-load-{}-key".format(val_name)

        if cache.get(pre_load_value_key):
            return

        tenant_config = TenantConfig.objects.values_list("lms_configs", flat=True)
        microsite_config = Microsite.objects.values_list("values", flat=True)

        for config in chain(microsite_config, tenant_config):
            try:
                if isinstance(config, six.string_types):
                    config = json.loads(config)

                org_filter = config.get("course_org_filter", [])
                result = config.get(val_name)
            except AttributeError:
                continue

            if isinstance(org_filter, six.string_types):
                org_filter = [org_filter]

            for org in org_filter:
                key = "org-value-{}-{}".format(org, val_name)
                cls.set_key_to_cache(key, result)

        cls.set_key_to_cache(pre_load_value_key, True)


class TenantCertificateManager(models.Manager):
    """
    Custom Manager Class that allows to override the get_queryset
    method in order to filter the results by org.
    """

    def get_queryset(self):
        """
        Call parent method and filter the certificates by org.
        """
        generated_certificates = super(TenantCertificateManager, self).get_queryset()
        org_filter = get_organizations()

        if org_filter:
            q_objects = models.Q()  # Create an empty Q object to start with.

            for org in org_filter:
                q_objects |= models.Q(course_id__startswith="course-v1:{org}+".format(org=org))

            return generated_certificates.filter(q_objects)

        return generated_certificates.none()


class TenantEligibleCertificateManager(TenantCertificateManager):
    """
    A manager for `GeneratedCertificate` models that automatically
    filters out ineligible certs.

    This class is very similar to <lms.djangoapps.certificates.models.EligibleCertificateManager>
    and the purpose is the same but the parent class is different.
    """

    def get_queryset(self):
        """
        Return a queryset for `GeneratedCertificate` models, filtering out
        ineligible certificates.
        """
        certificates_statuses = CertificatesModels.CertificateStatuses
        return super(TenantEligibleCertificateManager, self).get_queryset().exclude(
            status__in=(certificates_statuses.audit_passing, certificates_statuses.audit_notpassing)
        )


class TenantGeneratedCertificateProxy(GeneratedCertificate):
    """
    Proxy model for <lms.djangoapps.certificates.models.GeneratedCertificate>.

    The purpose of this is to override the GeneratedCertificate managers.
    More information in https://docs.djangoproject.com/en/3.0/topics/db/models/#proxy-models
    """

    eligible_certificates = TenantEligibleCertificateManager()
    objects = TenantCertificateManager()

    class Meta:
        """ Set as a proxy model. """
        proxy = True

    def __str__(self):
        key = getattr(settings, "EDNX_TENANT_KEY", "No tenant is active at the moment")
        return "<Tenant proxy as GeneratedCertificate: {}>".format(key)

    def save(self, *args, **kwargs):
        """
        Override the save method such that we use the non proxy cert during the save.
        """
        with proxy_regression(get_certificates_models(), "GeneratedCertificate", GeneratedCertificate):
            super(TenantGeneratedCertificateProxy, self).save(*args, **kwargs)
