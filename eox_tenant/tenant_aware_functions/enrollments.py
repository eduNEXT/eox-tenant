"""
Microsite aware enrollments filter.
"""
from django.conf import settings

from eox_tenant.edxapp_wrapper.site_configuration_module import get_configuration_helpers
from eox_tenant.edxapp_wrapper.theming_helpers import get_theming_helpers


def filter_enrollments(enrollments):
    """
    Given a list of enrollment objects, we filter out the enrollments to orgs that
    do not belong to the current microsite
    """

    theming_helpers = get_theming_helpers()
    test_skip = getattr(settings, "EOX_TENANT_SKIP_FILTER_FOR_TESTS", False)
    # If test setting is true, returns the same enrollments,
    # or if we do not have a microsite context, there is nothing we can do.
    if test_skip or not theming_helpers.is_request_in_themed_site():
        for enrollment in enrollments:
            yield enrollment
        return

    configuration_helpers = get_configuration_helpers()
    orgs_to_include = configuration_helpers.get_value('course_org_filter', None)
    orgs_to_exclude = []

    # Make sure we have a list
    if orgs_to_include and not isinstance(orgs_to_include, list):
        orgs_to_include = [orgs_to_include]

    if not orgs_to_include:
        # Making orgs_to_include an empty iterable
        orgs_to_include = []
        orgs_to_exclude = configuration_helpers.get_all_orgs()

    for enrollment in enrollments:

        org = enrollment.course_id.org

        # Filter out anything that is not attributed to the inclusion rule.
        if org not in orgs_to_include:
            continue

        # Conversely, filter out any enrollments with courses attributed to exclusion rule.
        if org in orgs_to_exclude:
            continue

        # Else, include the enrollment.
        yield enrollment
