""".
Utils used in eox-tenant.
"""
import logging
import re

import six

from eox_tenant.edxapp_wrapper.users import get_user_signup_source
from eox_tenant.models import TenantOrganization

UserSignupSource = get_user_signup_source()
log = logging.getLogger(__name__)

# Taken from: https://github.com/kvesteri/validators/blob/master/validators/domain.py
domain_pattern = re.compile(
    r'^(?:[a-zA-Z0-9]'  # First character of the domain
    r'(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)'  # Sub domain + hostname
    r'+[A-Za-z0-9][A-Za-z0-9-_]{0,61}'  # First 61 characters of the gTLD
    r'[A-Za-z]$'  # Last character of the gTLD
)
NON_SERIALIZABLE = object()


def clean_serializable_values(obj):
    """
    Returns only serializable values

    If an object is not json serializable returns NON_SERIALIZABLE.
    In case of a list or dict ignore the NON_SERIALIZABLE values.
    """
    if isinstance(obj, (str, int, float, float, bool, type(None))):
        return obj

    if isinstance(obj, list):
        return [
            cleaned_item
            for cleaned_item in (clean_serializable_values(item) for item in obj)
            if cleaned_item is not NON_SERIALIZABLE
        ]

    if isinstance(obj, tuple):
        return tuple(
            cleaned_item
            for cleaned_item in (clean_serializable_values(item) for item in obj)
            if cleaned_item is not NON_SERIALIZABLE
        )

    if isinstance(obj, dict):
        return {
            key: cleaned_value
            for key, cleaned_value in ((k, clean_serializable_values(v)) for k, v in obj.items())
            if cleaned_value is not NON_SERIALIZABLE
        }

    return NON_SERIALIZABLE


def is_valid_domain(domain):
    """
    Return whether or not given value is a valid domain.
    """
    try:
        return domain_pattern.match(domain)
    except (UnicodeError, AttributeError):
        log.error("{} is not a valid domain.".format(domain))
    return False


def move_signupsource(old_domain, new_domain):
    """
    Move SignupSources from a domain to another domain.
    """

    if is_valid_domain(old_domain) and is_valid_domain(new_domain):

        log.info("Changing SignupSources from {} to {}.".format(old_domain, new_domain))
        count = UserSignupSource.objects.filter(site=old_domain).update(site=new_domain)

        log.info("Updated {} SignupSources from {} to {}.".format(count, old_domain, new_domain))


def synchronize_tenant_organizations(instance):
    """
    Synchronize the course_org_filter value with
    the instance.organizations field.

    Args:
        instance: This could be a TenantConfig or Microsite model instance.
    """
    try:
        config = instance.lms_configs
    except AttributeError:
        # Microsites support.
        config = instance.values

    course_org_filter = config.get("course_org_filter", [])

    if isinstance(course_org_filter, six.string_types):
        course_org_filter = [course_org_filter]

    instance.organizations.clear()

    for org in course_org_filter:
        organization, _ = TenantOrganization.objects.get_or_create(name=org)
        instance.organizations.add(organization)
