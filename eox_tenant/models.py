"""
Model to store a microsite in the database.
The object is stored as a json representation of the python dict
that would have been used in the settings.
"""
import collections
import json

from django.db import connection, models
from django.utils.translation import ugettext_lazy as _
from jsonfield.fields import JSONField


class MicrositeManager(models.Manager):
    """
    Custom managaer for Microsite model.
    """

    def get_value_for_org(self, org, key):
        """
        Execute a query over all registers and filter the value by the org in the values field.

        Args:
            org: String.
            key: String.
        Returns:
            The value for the given key and org.
        """
        query = """
            SELECT
                JSON_EXTRACT(`values`, '$.{key}')
            FROM
                ednx_microsites_microsite
            WHERE
                  JSON_EXTRACT(`values`, "$.course_org_filter") like '%"{org}"%';
            """.format(key=key, org=org)

        return _execute_simple_query(query)

    def get_value_for_all_orgs(self, key):
        """
        Execute a query over all resgisters and return the value and org for the given key.

        Args:
            key: String.
        Returns:
            The value for the given key and org.
        """
        result = []
        query = """
            SELECT
                JSON_EXTRACT(`values`, '$.course_org_filter'),
                JSON_EXTRACT(`values`, '$.{key}')
            FROM
                ednx_microsites_microsite
            WHERE
                  JSON_EXTRACT(`values`, "$.course_org_filter") IS NOT NULL AND
                  JSON_EXTRACT(`values`, "$.{key}") IS NOT NULL;
            """.format(key=key)

        with connection.cursor() as cursor:
            cursor.execute(query)

            for row in cursor.fetchall():
                result.append({
                    "course_org_filter": json.loads(row[0]),
                    key: json.loads(row[1])
                })

        return result


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
    values = JSONField(null=False, blank=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    objects = MicrositeManager()

    class Meta:
        """
        Model meta class.
        """
        # Note to ops: The table already exists under a different name due to the migration from EOE.
        db_table = 'ednx_microsites_microsite'
        app_label = "eox_tenant"

    def __unicode__(self):
        return self.key

    def get_organizations(self):
        """
        Helper method to return a list of organizations associated with our particular Microsite
        """
        # has to return the same type as:
        # MicrositeOrganizationMapping.get_organizations_for_microsite_by_pk(self.id)
        org_filter = self.values.get('course_org_filter')  # pylint: disable=no-member

        if isinstance(org_filter, str):
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
        microsites = cls.objects.filter(subdomain=domain)  # pylint: disable=no-member

        return microsites[0] if microsites else None


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

    def get_value_for_org(self, org, key):
        """
        Execute a query over the registers and filter the value by the org in the lms_config field.

        Args:
            org: String.
            key: String.
        Returns:
            The value for the given key and org.
        """
        query = """
            SELECT
                JSON_EXTRACT(`lms_configs`, '$.{key}')
            FROM
                eox_tenant_tenantconfig
            WHERE
                JSON_EXTRACT(`lms_configs`, "$.course_org_filter") like '%"{org}"%';
            """.format(key=key, org=org)

        return _execute_simple_query(query)

    def get_value_for_all_orgs(self, key):
        """
        Execute a query over all resgisters and return the value and org for the given key.

        Args:
            key: String.
        Returns:
            The value for the given key and org.
        """
        result = []
        query = """
            SELECT
                JSON_EXTRACT(`lms_configs`, '$.course_org_filter'),
                JSON_EXTRACT(`lms_configs`, '$.{key}')
            FROM
                eox_tenant_tenantconfig
            WHERE
                JSON_EXTRACT(`lms_configs`, "$.course_org_filter") IS NOT NULL AND
                JSON_EXTRACT(`lms_configs`, "$.{key}") IS NOT NULL;
            """.format(key=key)

        with connection.cursor() as cursor:
            cursor.execute(query)

            for row in cursor.fetchall():
                result.append({
                    "course_org_filter": json.loads(row[0]),
                    key: json.loads(row[1])
                })

        return result


class TenantConfig(models.Model):
    """
    Model to persist edxapp configurations.
    """

    external_key = models.CharField(max_length=63, db_index=True)
    lms_configs = JSONField(null=False, blank=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    studio_configs = JSONField(null=False, blank=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    theming_configs = JSONField(null=False, blank=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})
    meta = JSONField(null=False, blank=True, load_kwargs={'object_pairs_hook': collections.OrderedDict})

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

        if isinstance(org_filter, str):
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
        TenantConfig
    )

    class Meta:
        """
        Model meta class.
        """
        app_label = "eox_tenant"


def _execute_simple_query(query):
    """
    Execute the given query a return the first value for the first row.
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()

        if row and row[0]:
            try:
                return json.loads(row[0])
            except Exception:  # pylint: disable=broad-except
                return row[0]

    return None
