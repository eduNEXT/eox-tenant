"""
Model to store a microsite in the database.
The object is stored as a json representation of the python dict
that would have been used in the settings.
"""
import collections

from django.db import models

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
        db_table = 'ednx_microsites_microsites'
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
