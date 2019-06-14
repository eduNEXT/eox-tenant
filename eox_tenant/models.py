"""
Model to store a microsite in the database.
The object is stored as a json representation of the python dict
that would have been used in the settings.
"""
import collections

from django.db import models
from django.utils.translation import ugettext_lazy as _

from jsonfield.fields import JSONField


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
        from django.db import connection

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT eox_c.id, eox_c.external_key, eox_c.lms_configs, eox_c.studio_configs, eox_c.theming_configs, eox_c.meta
                FROM eox_tenant_tenantconfig eox_c
                WHERE eox_c.id = (SELECT eox_tenant_route.config_id from eox_tenant_route
                WHERE eox_tenant_route.domain=%s)""", [domain])
            result_list = []
            for row in cursor.fetchall():
                result_list.append(row)
        return result_list


class TenantConfig(models.Model):
    """
    Model to persist edxapp configurations
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
        TODO
        """

        org_filter = self.lms_configs.get('course_org_filter')  # pylint: disable=no-member

        if isinstance(org_filter, str):
            org_filter = [org_filter]

        return org_filter

    @classmethod
    def get_configs_for_domain(cls, domain):
        """
        TODO
        """

        # remove any port number from the hostname
        domain = domain.split(':')[0]
        config = TenantConfig.objects.filter(route__domain=domain).last()  # pylint: disable=no-member

        if config:
            return config.lms_configs, config.external_key
        else:
            return {}, None

    objects = TenantConfigManager()


class Route(models.Model):
    """
    Model to persist site routes
    """
    domain = models.CharField(
        _('domain name'),
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


class Redirection(models.Model):
    """This object stores the redirects for a domain
    """

    HTTP = 'http'
    HTTPS = 'https'

    SCHEME = (
        (HTTP, 'http'),
        (HTTPS, 'https'),
    )

    STATUS = (
        (301, 'Temporary'),
        (302, 'Permanent'),
    )

    domain = models.CharField(max_length=253, db_index=True,
                              help_text='use only the domain name, e.g. cursos.edunext.co')
    target = models.CharField(max_length=253)
    scheme = models.CharField(max_length=5, choices=SCHEME, default=HTTP)
    status = models.IntegerField(choices=STATUS, default=301)

    class Meta:
        """
        Model meta class.
        """
        # Note to ops: The table already exists under a different name due to the migration from EOE.
        db_table = 'edunext_redirection'

    def __unicode__(self):
        return u"Redirection from {} to {}. Protocol {}. Status {}".format(
            self.domain,
            self.target,
            self.scheme,
            self.status,
        )
