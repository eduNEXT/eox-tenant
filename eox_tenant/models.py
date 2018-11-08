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
        db_table = 'ednx_microsites_microsites'

    def __unicode__(self):
        return self.key

    def get_organizations(self):
        """
        Helper method to return a list of organizations associated with our particular Microsite
        """
        # has to return the same type as:
        # MicrositeOrganizationMapping.get_organizations_for_microsite_by_pk(self.id)
        org_filter = self.values.get('course_org_filter')  # pylint: disable=no-member

        if isinstance(org_filter, basestring):
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
