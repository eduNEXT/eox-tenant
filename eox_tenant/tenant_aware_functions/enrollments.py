"""
Microsite aware enrollments filter.
"""
from eox_tenant.edxapp_wrapper.get_microsite_configuration import get_microsite


def filter_enrollments(enrollments):
    """
    Given a list of enrollment objects, we filter out the enrollments to orgs that
    do not belong to the current microsite
    """

    # If we do not have a microsite context, there is nothing we can do
    if not get_microsite().is_request_in_microsite():
        for enrollment in enrollments:
            yield enrollment
        return

    orgs_to_include = get_microsite().get_value('course_org_filter')
    orgs_to_exclude = get_microsite().get_all_orgs()

    if orgs_to_include:
        # Make sure we dont exclude one of the included orgs, when the data is contradictory
        orgs_to_exclude = [x for x in orgs_to_exclude if x not in orgs_to_include]

    for enrollment in enrollments:

        org = enrollment.course_id.org

        # Filter out anything that is not attributed to the inclusion rule.
        if orgs_to_include and org not in orgs_to_include:
            continue

        # Conversely, filter out any enrollments with courses attributed to exclusion rule.
        elif org in orgs_to_exclude:
            continue

        # Else, include the enrollment.
        else:
            yield enrollment
