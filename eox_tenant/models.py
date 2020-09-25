"""
Model to store a microsite in the database.
The object is stored as a json representation of the python dict
that would have been used in the settings.
"""
import collections
import json

import six
from django.db import connection, models
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField


class TenantOrganization(models.Model):
    """
    Model to persist organizations.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    class Meta:
        """
        Model meta class.
        """
        app_label = "eox_tenant"

    def __str__(self):
        return "<Org: {}>".format(self.name)


class Microsite(models.Model):
    """
    This is where the information about the microsite gets stored to the db.
    To achieve the maximum flexibility, most of the fields are stored inside
    a json field.
    Notes:
        - The key field was required for the dict definition at the settings, and it
        is used in some of the microsite_configuration methods.
        - The subdomain is outside of the json so that it is posible to use a db query
        to improve performance.
        - The values field must be validated on save to prevent the platform from crashing
        badly in the case the string is not able to be loaded as json.
    """
    key = models.CharField(max_length=63, db_index=True)
    subdomain = models.CharField(max_length=127, db_index=True)
    values = JSONField(blank=True, default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    organizations = models.ManyToManyField(TenantOrganization, blank=True)

    class Meta:
        """
        Model meta class.
        """
        # Note to ops: The table already exists under a different name due to the migration from EOE.
        db_table = 'ednx_microsites_microsite'
        app_label = "eox_tenant"

    def __str__(self):
        return self.key

    def get_organizations(self):
        """
        Helper method to return a list of organizations associated with our particular Microsite
        """
        # has to return the same type as:
        # MicrositeOrganizationMapping.get_organizations_for_microsite_by_pk(self.id)
        org_filter = self.values.get('course_org_filter')  # pylint: disable=no-member

        if isinstance(org_filter, six.string_types):
            org_filter = [org_filter]

        return org_filter

    @classmethod
    def get_microsite_for_domain(cls, domain):
        """
        Returns the microsite associated with this domain. Note that we always convert to lowercase, or
        None if no match
        """

        # remove any port number from the hostname
        domain = domain.split(':')[0]
        microsites = cls.objects.filter(subdomain=domain)

        return microsites[0] if microsites else None

    @classmethod
    def get_value_for_org(cls, org, val_name):
        """
        Filter the value by the org in the values field.

        Args:
            org: String.
            key: String.
        Returns:
            The value for the given key and org.
        """
        results = cls.objects.filter(organizations__name=org)

        for result in results:
            value = result.values.get(val_name)

            if value:
                return value

        return None


class TenantConfigManager(models.Manager):
    """
    Custom managaer for Tenant Config model.
    """

    def get_configurations(self, domain):
        """
        Execute optimized query to get site configurations.
        """
        configurations = {}

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    eox_config.id,
                    eox_config.external_key,
                    eox_config.lms_configs,
                    eox_config.studio_configs,
                    eox_config.theming_configs,
                    eox_config.meta
                FROM eox_tenant_tenantconfig eox_config
                WHERE eox_config.id = (SELECT eox_tenant_route.config_id from eox_tenant_route
                WHERE eox_tenant_route.domain=%s)""", [domain])

            # Using fetchone since the query will return one configuration per domain at the most.
            row = cursor.fetchone()
            if row:
                configurations = {
                    "id": row[0],
                    "external_key": row[1],
                    "lms_configs": json.loads(row[2]),
                    "studio_configs": json.loads(row[3]),
                    "theming_configs": json.loads(row[4]),
                    "meta": json.loads(row[5]),
                }

        return configurations


class TenantConfig(models.Model):
    """
    Model to persist edxapp configurations.
    """

    external_key = models.CharField(max_length=63, db_index=True)
    lms_configs = JSONField(blank=True, default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    studio_configs = JSONField(blank=True, default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    theming_configs = JSONField(blank=True, default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    meta = JSONField(blank=True, default={}, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    organizations = models.ManyToManyField(TenantOrganization, blank=True)

    class Meta:
        """
        Model meta class.
        """
        app_label = "eox_tenant"

    def __unicode__(self):
        return self.external_key

    def get_organizations(self):
        """
        Helper method to get organizations.
        """

        org_filter = self.lms_configs.get("course_org_filter")  # pylint: disable=no-member

        if isinstance(org_filter, six.string_types):
            org_filter = [org_filter]

        return org_filter

    @classmethod
    def get_configs_for_domain(cls, domain):
        """
        Get edxapp configuration using a domain. There is a compat layer to support microsite until
        deprecation.
        """

        # remove any port number from the hostname
        domain = domain.split(':')[0]
        config = TenantConfig.objects.get_configurations(domain=domain)

        if config:
            return config["lms_configs"], config["external_key"]

        return {}, None

    objects = TenantConfigManager()

    @classmethod
    def get_value_for_org(cls, org, val_name):
        """
        Filter the value by the org in the lms_config field.

        Args:
            org: String.
            key: String.
        Returns:
            The value for the given key and org.
        """
        results = cls.objects.filter(organizations__name=org)

        for result in results:
            value = result.lms_configs.get(val_name)

            if value:
                return value

        return None


class Route(models.Model):
    """
    Model to persist site routes.
    """

    domain = models.CharField(
        _("domain name"),
        max_length=100,
        unique=True,
    )

    config = models.ForeignKey(
        TenantConfig,
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        Model meta class.
        """
        app_label = "eox_tenant"
