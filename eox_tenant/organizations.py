"""
General methods for eox-tenant organizations.
"""
import six
from django.conf import settings


def get_organizations():
    """
    Return a set of organizations from the general django settings.
    """
    org_filter = getattr(settings, 'course_org_filter', set([]))

    if isinstance(org_filter, six.string_types):
        org_filter = set([org_filter])

    return org_filter
